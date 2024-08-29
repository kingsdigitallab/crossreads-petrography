from . import *

class MgsConverter(CrossreadsPetrographyTool):
    name = "mgs"

    @property
    def df_input(self):
        logger.info(f"Loading MGS data from: {self.path_input}")
        df = read_path(self.path_input)
        logger.info(f"Loaded {len(df)} rows of MGS data")
        logger.debug(f"DataFrame head: {df.head()}")
        return df

    @property
    def df_output(self):
        logger.info("Processing MGS intersections")
        df_mgs = self.df_input
        logger.debug(f"Initial df_mgs shape: {df_mgs.shape}")

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

        range_wh = defaultdict(dict)
        range_box = defaultdict(dict)

        for i, row in df_mgs.iterrows():
            logger.debug(f"Processing row {i}: {dict(row)}")
            if row.value_type == 'min wh':
                range_wh[row.subtype]['min'] = row.value_mm
            elif row.value_type == 'max wh':
                range_wh[row.subtype]['max'] = row.value_mm
            elif row.value_type == 'min box':
                range_box[row.subtype]['min'] = row.value_mm
            elif row.value_type == 'max box':
                range_box[row.subtype]['max'] = row.value_mm

        logger.debug(f"Whisker ranges: {dict(range_wh)}")
        logger.debug(f"Box ranges: {dict(range_box)}")

        df_big = read_metadata(metamorphic=True)
        logger.debug(f"Metadata shape: {df_big.shape}")

        col_optical = 'optical microscopy MGS (mm)'
        col_digital = 'digital microscopy MGS (mm)'
        cols = [('optical', col_optical), ('digital', col_digital)]
        
        all_intersections = defaultdict(dict)
        for coltype, col in cols:
            logger.debug(f"Processing {coltype} microscopy")
            values = df_big[col]
            values = pd.to_numeric(values[values!=""], errors='coerce')
            logger.debug(f"{coltype} values: {values.describe()}")
            
            for rangetype, ranges in [('whisker', range_wh), ('box', range_box)]:
                logger.debug(f"Processing {rangetype} range")
                intersections = all_intersections[coltype][rangetype] = defaultdict(list)
                for isic, value in zip(values.index, values):
                    for subtype, subtyperange in ranges.items():
                        logger.debug(f"Checking intersection: ISIC={isic}, value={value}, subtype={subtype}, range={subtyperange}")
                        if value >= subtyperange['min'] and value <= subtyperange['max']:
                            if subtype not in intersections[isic]:
                                intersections[isic].append(subtype)
                                logger.debug(f"Intersection found: ISIC={isic}, subtype={subtype}")

        df = IsotopeConverter().df_intersections.copy()
        logger.debug(f"Initial intersections DataFrame shape: {df.shape}")

        for i in df.index:
            df.loc[i] = [''] * len(df.columns)
        logger.debug(f"Cleared intersections DataFrame. New shape: {df.shape}")

        all_subtypes = df_mgs.subtype.unique()
        for subtype in all_subtypes:
            if subtype not in set(df.columns):
                df[subtype] = ''
                logger.debug(f"Added new column for subtype: {subtype}")

        symbols = {'optical':'🔬', 'digital':'🔍'}
        intersections_mgs = all_intersections
        for coltype in intersections_mgs:
            for wh_or_box in intersections_mgs[coltype]:
                for isic in set(intersections_mgs[coltype][wh_or_box]):
                    if isic not in set(df.index):
                        df.loc[isic] = [''] * len(df.columns)
                        logger.debug(f"Added new row for ISIC: {isic}")
                    for subtype in intersections_mgs[coltype][wh_or_box][isic]:
                        df.loc[isic][subtype] += symbols[coltype]
                        logger.debug(f"Added symbol for ISIC={isic}, subtype={subtype}, coltype={coltype}")
        
        df['has_optical'] = [
            symbols['optical'] in ''.join(d.values())
            for d in df.to_dict('records')
        ]
        logger.debug(f"Added 'has_optical' column. True count: {df['has_optical'].sum()}")

        df = df.rename_axis('ISic').reset_index()
        df = df.sort_values(['has_optical','ISic'], ascending=[False, True])
        logger.info(f"Processed MGS intersections for {len(df)} samples")
        logger.debug(f"Final DataFrame shape: {df.shape}")
        return df.drop('has_optical', axis=1).set_index('ISic')

    def save(self):
        logger.info("Saving MGS intersections")
        ofn = Path(self.path_output) / 'mgs_intersections.xlsx'
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