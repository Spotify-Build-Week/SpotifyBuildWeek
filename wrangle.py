import pandas as pd
from category_encoders import OneHotEncoder, OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler

raw_df = pd.read_csv('SpotifyFeatures.csv')

# Applying the necessary data cleaning and feature engineering
# in one wrangle function.

class Wrangler():

    def wrangle(self, df):

        # drop duplicate entries
        df = df.drop_duplicates(subset='track_id')
            
        # drop identifier column
        df = df.drop(columns='track_id')

        # remove '#' from the 'key'column
        df['key'] = df['key'].str.replace('#', '')

        # reindex dataframe (some indexes were lost due to dropping duplicate rows)
        df = df.reset_index()
        # drop the additional 'index' column which was created when reindexing
        df.drop(columns='index', inplace=True)

        return df


    def transform(self, df):

        # encode the entire dataset
        df1 = df.drop(columns=['artist_name', 'track_name'])
        enc = OrdinalEncoder()
        df_encoded = enc.fit_transform(df1)
        
        # scale the entire dataset
        scaler = MinMaxScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_encoded.values), columns=df1.columns)
        
        return df_scaled


# df = wrangle(raw_df)
# user_input = df_scaled.iloc[0].values.reshape(1,-1)
