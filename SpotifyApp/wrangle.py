import pandas as pd
from category_encoders import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors


raw_df = pd.read_csv('SpotifyFeatures.zip')

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


# # load a model:
# # loading a pickled model
# with lzma.open("lmza_test.xz", "rb") as f:
#     # pickle.dump(model, f)
#     loaded_model = pickle.load(f)

def generate_output(song, artist, orig_df, scaled_df, model):
    """Take user input, locate it in our datasets,
    reshape it and run through the model.
    Return track names and artist names of 5 most similar songs"""

    # locate user input in our datasets and reshape it
    orig_input = orig_df.loc[(orig_df['track_name'] == song) & (orig_df['artist_name'] == artist)]
    scaled_input = scaled_df.loc[orig_input.index[0]]
    reshaped_input = scaled_input.values.reshape(1, -1)

    # run reshaped input through the model
    n_dist_, n_ind_ = model.kneighbors(reshaped_input)

    # get 5 most similar songs as the output
    output = orig_df[['track_name','artist_name']].loc[list(n_ind_[0][1:])]

    return output
