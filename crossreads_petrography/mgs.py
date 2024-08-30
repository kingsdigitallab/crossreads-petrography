from . import *

class MgsConverter(CrossreadsPetrographyTool):
    col_optical = 'optical microscopy MGS (mm)'
    col_digital = 'digital microscopy MGS (mm)'

    name = "mgs"

    @property
    def df_input(self):
        logger.info(f"Loading MGS data from: {self.path_input}")
        df = read_path(self.path_input)
        logger.info(f"Loaded {len(df)} rows of MGS data")
        logger.debug(f"DataFrame head: {df.head()}")
        return df

    @property
    def df_ranges(self):
        logger.info("Calculating MGS ranges from input data")
        df_mgs = self.df_input
        
        df_mgs['value_mm'] = pd.to_numeric(df_mgs['value_mm'], errors='coerce')
        logger.debug(f"Converted 'value_mm' to numeric. Null values: {df_mgs['value_mm'].isnull().sum()}")

        subtype_renamed = {
            'Goktepe':'Göktepe',
            'Docimian':'Docimium',
            'Dokymeion':'Docimium',
            'Penteli':'Pentelikon',
            'Hymettos':'Hymettus',
            'Proconnesos':'Proconnesos-1',
            'Thasos-(1) 2':'Thasos-1 (2)'
        }
        df_mgs['subtype'] = df_mgs['subtype'].apply(lambda x: subtype_renamed.get(x,x))
        logger.debug(f"Renamed subtypes. Unique subtypes: {df_mgs['subtype'].unique()}")

        # Create a pivot table
        df_ranges = df_mgs.pivot(index='subtype', columns='value_type', values='value_mm')
        
        # Rename columns
        def rename_column(col):
            parts = col.split()
            if len(parts) >= 2:
                return f'{parts[-1]}_{parts[0]}'
            return col

        df_ranges.columns = [rename_column(col) for col in df_ranges.columns]
        
        # Reorder columns
        column_order = ['wh_min', 'wh_max', 'box_min', 'box_max']
        df_ranges = df_ranges.reindex(columns=column_order)

        logger.debug(f"Created df_ranges with {len(df_ranges)} rows: {df_ranges}")
        return df_ranges

    @property
    def df_microscopy(self):
        logger.info("Creating microscopy DataFrame from Metamorphic metadata")
        df_big = read_metadata(metamorphic=True)
        logger.debug(f"Metadata shape: {df_big.shape}")

        
        
        df_microscopy = df_big[[self.col_optical, self.col_digital]].dropna(how='all')
        df_microscopy = df_microscopy.apply(pd.to_numeric, errors='coerce')
        logger.info(f'{len(df_microscopy)} samples with microscopy data')
        logger.debug(f"Created df_microscopy with {len(df_microscopy)} rows")
        return df_microscopy

    @property
    def df_output(self):
        logger.info("Processing MGS intersections")
        
        df_ranges = self.df_ranges
        df_microscopy = self.df_microscopy

        col_optical = self.col_optical
        col_digital = self.col_digital
        cols = [('optical', col_optical), ('digital', col_digital)]
        
        df = pd.DataFrame(index=df_microscopy.index, columns=df_ranges.index)
        logger.debug(f"Initial intersections DataFrame shape: {df.shape}")

        df[:] = ''  # Clear all values
        
        symbols = {'optical':'🔬', 'digital':'🔍'}
        
        for coltype, col in cols:
            for isic, value in df_microscopy[col].items():
                for subtype, row in df_ranges.iterrows():
                    if row['wh_min'] <= value <= row['wh_max'] or row['box_min'] <= value <= row['box_max']:
                        if isic not in df.index:
                            df.loc[isic] = [''] * len(df.columns)
                        if subtype not in df.columns:
                            df[subtype] = ''
                        df.loc[isic, subtype] += symbols[coltype]
                        logger.debug(f"Intersection found: ISIC={isic}, subtype={subtype}, coltype={coltype}")

        df['has_optical'] = df.apply(lambda row: symbols['optical'] in ''.join(row), axis=1)
        logger.debug(f"Added 'has_optical' column. True count: {df['has_optical'].sum()}")

        df = df.rename_axis('ISic').reset_index()
        df = df.sort_values(['has_optical', 'ISic'], ascending=[False, True])
        logger.info(f"Processed MGS intersections for {len(df)} samples")
        logger.debug(f"Final DataFrame shape: {df.shape}")
        return df.drop('has_optical', axis=1).set_index('ISic')

    def save(self, output_folder=None):
        logger.info("Saving MGS intersections")
        output_folder = output_folder or self.output_path_now
        ofn = Path(output_folder) / 'mgs_intersections.xlsx'
        ofn.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Saving to file: {ofn}")
        self.df_output.to_excel(ofn)
        logger.info(f"Saved MGS intersections to {ofn}")
        logger.debug(f"File size: {ofn.stat().st_size} bytes")

    def run(self):
        logger.info("Running MGS intersections")
        self.save()
        logger.info("MGS intersections processing completed")
        logger.debug("Run method completed successfully")