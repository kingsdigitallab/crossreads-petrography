from . import *

PATCHES = [
    ('Pb', 'Hg'), # Pb copied to new Hg
    ('Zn', 'As'), # Zn copied to new As
]
DISCARD_ELEMENTS = {'Ba','Cr','La','Ni','V','Ce'}

class PXRFConverter(CrossreadsPetrographyTool)  :
    name = "pxrf"

    @cached_property
    def df_standards(self):
        logger.info("Loading pXRF standard values")
        df = read_path('pxrf.standards')
        df = df.set_index(df.columns[0])
        df = df.T.rename_axis('Element')
        return df[list(reversed(df.columns))]

    @cached_property
    def df_descriptions(self):
        logger.info("Loading pXRF descriptions")
        odf = read_path('pxrf.descriptions').fillna('')

        def fix_isic(x):
            if type(x) is str and x.isdigit():
                x=int(x)
            if isinstance(x, (int,float)):
                x=f'Isic{int(x):06d}'
            return x
        odf['Isic'] = odf['Isic'].apply(fix_isic)
        # odf = odf.set_index(odf.columns[0])
        # odf=odf.T

        odf = odf.set_index(odf.columns[0])
        cols = [c for c in odf]
        cols = [c.split("=")[0].strip() for c in cols]
        odf.columns = cols
        return odf
    
    @cached_property
    def txt_input(self):
        return read_path('pxrf.input', as_list=True)
    
    @cached_property
    def df_input(self):
        return pd.DataFrame([
            {
                'filename':fn, 
                'text':txt
            }
            for fn,txt in self.txt_input
        ])

    @cached_property
    def df_standards_parsed(self, verbose=False):
        # logger.info("Parsing pXRF standards data")
        txts = self.txt_input
        df_standards = self.df_standards
        
        o = []
        for filename,txt in txts:
            if verbose: print(filename)
            for srctxt in txt.strip().split('\n\n'):
                is_mk = filename.startswith('MK')
                # if is_mk: continue
                lines = srctxt.split('\n')
                src = lines[0].split(':')[-1].split('.csv')[0].strip()
                
                if is_mk:
                    is_standard = src.replace('-', '').isdigit()
                else:
                    is_standard = src.startswith('t0-')
                if not is_standard:
                    continue
                if is_mk:
                    standard_key = src.split('-')[0] + 'CC'
                else:
                    standard_key = src.split('-')[1]
                
                if standard_key and not standard_key[0].isdigit():
                    continue
                
                if verbose: print([filename,src,is_standard,standard_key])
                

                # if standard_key!='100CC': continue


                key = lines[1].split(':')[-1].strip()
                header = lines[2].split()
                data = [ln.split() for ln in lines[3:]]
                df = pd.DataFrame(data, columns=header)

                if is_mk:
                    df=df[df.Element.isin({'Si','K','Ca','Fe'})]
                    def rename(x):
                        if x=='Si': return 'SiO2'
                        if x=='K': return 'K2O'
                        if x=='Ca': return 'CaO'
                        if x=='Fe': return 'Fe2O3'
                    
                    df['Element']=df['Element'].apply(rename)

                # ignoring elements that don't regress well
                df=df[~df.Element.isin(DISCARD_ELEMENTS)]
                df=df.set_index('Element')

                if verbose: 
                    print('Standard data from MK file')
                    print()
                    
                
                df_this_standard = df_standards[[standard_key]].copy()
                df_this_standard.columns = ['standard_val']
                df_this_standard['standard_key'] = standard_key
                df_this_standard['source_name'] = src
                df_this_standard['source_text'] = srctxt
                df_this_standard['is_standard'] = is_standard
                df_this_standard['filename'] = filename
                
                if verbose:
                    print('Matching standards data (x)CC')
                    display(df_this_standard)
                    print()

                dfx=df.join(df_this_standard, how='outer')
                dfx['filename']=filename
                
                if verbose:
                    print('Joined data')
                    display(dfx)

                o.append(dfx)

        df = pd.concat(o)
        df['Mass_fraction'] = pd.to_numeric(df['Mass_fraction'], errors='coerce')
        df['standard_val'] = pd.to_numeric(df['standard_val'], errors='coerce')

        def get_standard_group(element,row):
            if element in {'SiO2','K2O','CaO','Fe2O3'}:
                x=row.standard_key
                if not x:
                    return ''
                
                return '10-50' if int(x.replace('CC', '')) < 60 else '50-100'
            else:
                return '(all)'
            
        df['standard_group'] = [get_standard_group(element,row) for element,row in df.fillna('').iterrows()]
        return df[df.standard_key != '0CC']
    
    @cached_property
    def df_linreg(self):
        logger.info("Calculating linear regressions for standard values")
        df = self.df_standards_parsed
        df = df[~df.Mass_fraction.isna()]
        df = df[~df.standard_val.isna()]
        ld = []
        gby = ['Element', 'standard_group']
        for g, gdf in df.groupby(gby):
            X = gdf[['Mass_fraction']].values
            y = gdf['standard_val'].values

            model = LinearRegression()
            fit = model.fit(X, y)
            m = model.coef_[0]
            q = model.intercept_
            d = dict(zip(gby, g))
            d['m'] = m
            d['q'] = q
            ld.append(d)

        ## mercury/zinc patch
        for old,new in PATCHES:
            old_l = [d for d in ld if d['Element']==old]
            if old_l:
                new_l = {**old_l[0]}
                new_l['Element'] = new
                ld.append(new_l)

        return pd.DataFrame(ld)
    
    @cached_property
    def valid_elements(self):
        return set(self.df_linreg.Element.unique())

    # @cached_property
    def get_df_adjusted(self, verbose=False, agg_stdev=False):
        logger.info("Parsing pXRF measurements and calculating new fractions")
        sdf = self.df_linreg
        df_desc = self.df_descriptions
        txts = self.txt_input
        
        o = []
        for filename,txt in txts:
            if verbose: print(filename)
            for srctxt in txt.strip().split('\n\n'):
                is_mk = filename.startswith('MK')
                # if is_mk: continue
                lines = srctxt.split('\n')
                src = lines[0].split(':')[-1].split('.csv')[0].strip()
                
                if is_mk:
                    is_standard = src.replace('-', '').isdigit()
                else:
                    is_standard = src.startswith('t0-')

                if is_mk:
                    standard_key = src.split('-')[0] + 'CC'
                else:
                    standard_key = src.split('-')[1]
                
                if verbose: print([filename,src,is_standard,standard_key])

                if is_standard:
                    continue
                # if standard_key!='100CC': continue


                key = lines[1].split(':')[-1].strip()
                header = lines[2].split()
                data = [ln.split() for ln in lines[3:]]
                df = pd.DataFrame(data, columns=header)

                if is_mk:
                    df=df[df.Element.isin({'Si','K','Ca','Fe'})]
                    def rename(x):
                        if x=='Si': return 'SiO2'
                        if x=='K': return 'K2O'
                        if x=='Ca': return 'CaO'
                        if x=='Fe' and is_mk: return 'Fe2O3'
                    
                    df['Element']=df['Element'].apply(rename)

                # ignoring elements that don't regress well
                df=df[~df.Element.isin({'Ba','Cr','La','Ni','V','Ce'})]
                df=df.set_index('Element')

                for cx in ['Mass_fraction', 'Fit_Area','Sigma_Area']:
                    df[cx] = pd.to_numeric(df[cx], errors='coerce')

                if is_mk:
                    ca_si = df.loc['CaO']['Mass_fraction'] / df.loc['SiO2']['Mass_fraction']
                    standard_group = '50-100' if ca_si >= 10 else '10-50'
                else:
                    # print(filename)
                    # display(df)
                    standard_group = '(all)'
                
                df['standard_group'] = standard_group
                df = df.merge(sdf, on=['Element', 'standard_group'], how='outer')
                df['y'] = (df['m'] * df['Mass_fraction']) + df['q']
                if is_mk:
                    df['Calc_fraction'] = df['y'] / df['y'].sum() * 100
                else:
                    df['Calc_fraction'] = df['y']
                
                df['Calc_fraction'] = df['Calc_fraction'].apply(lambda x: x if x>0 else 0)
                
                df['source_name'] = src

                try:
                    isics = [subsrc for subsrc in src.split('-')
                            if subsrc.startswith('ISic') or subsrc.startswith('Isic')
                            ]
                    isic = isics[0].strip().replace('ISic','Isic') if isics else src.split('-')[0].strip()
                    if not 'Isic' in isic:
                        isic = '-'.join(src.split('-')[:-1]) if '-' in src else src
                    
                    isic_letter = src.split('-')[-1].strip()
                    if isic_letter[0].isdigit() and isic_letter[-1].lower()=='t':
                        isic_letter = isic_letter[:-1]
                        # print([filename,src,isic,isic_letter,ascii_lowercase[int(isic_letter[:-1])-1]])
                    if isic_letter.isdigit():
                        isic_letter = ascii_lowercase[int(isic_letter)-1]
                    # if not is_mk:
                    #     print('src to parse into logbook column name',src)
                    #     print('isic',isic)
                    #     print('isic_letter',isic_letter)
                    df['Isic'] = isic

                    desc_rows = df_desc[df_desc.Isic == isic]
                    # print('desc_rows',desc_rows)
                    desc_col = desc_rows[isic_letter]
                    # print('desc_cols',desc_col)

                    desc = '; '.join(desc_col)
                    # if not is_mk: 
                    #     print(desc)
                    #     print()
                    # if not desc and not 'ISic' in src:
                        # print('\t'.join(str(x) for x in [src,isic,isic_letter,len(desc_rows), desc]))
                except KeyError as e:
                    logger.warning(f'[{filename}] Could not find {repr(isic_letter)} in logbook columns ({list(desc_rows.columns)})')
                    desc = '?'

                df['desc'] = desc
                df['desc_category'] = desc.split(',')[0] if ',' in desc else ''
                # df['filename'] = filename
                o.append(df)
        
        odf = pd.concat(o) if o else pd.DataFrame()
        odf = odf[odf.Element.isin(self.valid_elements)]
        
        gby=['Isic', 'Element', 'desc_category']
        odf = odf.set_index(gby)
        for c in odf: odf[c] = pd.to_numeric(odf[c], errors='coerce')
        odf = odf.groupby(gby).agg('mean' if not agg_stdev else 'std').reset_index()
        
        ld=[]
        els={'SiO2','K2O','CaO','Fe2O3'}
        for g,gdf in odf.groupby(['Isic','desc_category']):
            gld = gdf.to_dict(orient='records')
            sumval = sum(d.get('Calc_fraction',0) for d in gld if d.get('Element') in els)
            for d in gld:
                if d.get('Element') in els: 
                    d['Calc_fraction'] = d['Calc_fraction'] / sumval * 100 if sumval else 0
                ld.append(d)
        odf = pd.DataFrame(ld)
        return odf
    
    @cached_property
    def df_adjusted(self):
        return self.get_df_adjusted()
    



    def plot(self):
        # @title Plot linear regressions
        import plotnine as p9
        p9.options.figure_size = (12, 8)
        df_standards_parsed = self.df_standards_parsed
        df=df_standards_parsed[~df_standards_parsed.Mass_fraction.isna()]
        df=df[~df.standard_val.isna()]
        fig=p9.ggplot(df.reset_index(), p9.aes(x='Mass_fraction', y='standard_val', color='standard_group'))
        fig+=p9.geom_point()
        fig+=p9.geom_smooth(method='lm')
        fig+=p9.facet_wrap('Element', scales='free')
        return fig

    def save(self, output_folder=None, pivot_table=True):
        logger.info("Saving pXRF processed data")
        output_folder = output_folder or self.output_path_now
        df_mean = self.get_df_adjusted(agg_stdev=False).reset_index()
        df_std = self.get_df_adjusted(agg_stdev=True).reset_index()
        if pivot_table:
            df_mean = df_mean.pivot(index=['Isic', 'desc_category'], columns='Element', values='Calc_fraction').reset_index()
            df_std = df_std.pivot(index=['Isic', 'desc_category'], columns='Element', values='Calc_fraction').reset_index()

            df_mean = df_mean.replace({0:''})
            df_std = df_std.replace({0:''})
            prefcols = ['Isic','desc_category','SiO2','K2O','CaO','Fe2O3']
            df_mean = df_mean[[c for c in prefcols if c in df_mean] + [c for c in df_mean if c not in prefcols]]
            df_std = df_std[[c for c in prefcols if c in df_std] + [c for c in df_std if c not in prefcols]]
        
        output_file_mean = Path(output_folder) / 'pXRF_calculated_fractions_mean.xlsx'
        output_file_std = Path(output_folder) / 'pXRF_calculated_fractions_std.xlsx'
        # Ensure the parent directory of the output file exists
        output_file_mean.parent.mkdir(parents=True, exist_ok=True)
        df_mean.to_excel(output_file_mean)
        df_std.to_excel(output_file_std)
        logger.info(f"Saved: {output_file_mean}")
        logger.info(f"Saved: {output_file_std}")

    def run(self, output_folder=None, pivot_table=True):
        logger.info("Processing pXRF data")
        self.save(output_folder, pivot_table=pivot_table)

