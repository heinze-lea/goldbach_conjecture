import pandas as pd
import numpy as np

def calculate_mod_features(data_df, n_distance, mod_df = pd.DataFrame, mod_feature_col=[], primes=[], n_modular_features=20):
        
    """
    Calculates modular features for every number (n + n_distance) in data_df.
    Modular features are binary features, showing whether a number n + n_distance dividable by the lowest x prime numbers.

    data_df: DataFrame containing columns n to which modular features refer
    n_distance: Distance from n to which the modular feature refers to. Can be 0.
    mod_df: DataFrame containing modular features for n. Only necessary if n!=0. If not given, modular features will be looked up in data_df, and if not existing there, be computed for the lowest x prime numbers. 
    primes: Array of prime numbers. Necessary to compute modular features if n==0, or not given in either mod_df or data_df.
    n_modular_features: x for lowest prime numbers for which modular features are computed

    Returns:
    data_df extended by modular features for lowest x prime numbers for n + n_distance.
    """

    
    # if we look at neighbours: lets make sure we have the names of modular feature columns & mod_df if not given
    # both not needed if n_distance == 0
    if n_distance != 0:

        # we can pass only 1 dataframe which is used for n modular features & rest of data
        if len(mod_df) == 0:
            mod_df = data_df.copy()

        # we can read out the column names for n modular features if they are not passed
        if mod_feature_col == []:
            mod_feature_col = [col for col in mod_df.columns if col.startswith("n_mod_")]

    # we either want to calculate the modular features for n
    # or we want to calculate the modular features for n + x, and havent calculated them for n yet
    # lets try to avoid the latter case though, super inefficient
    if n_distance == 0 or (n_distance!=0 and len(mod_feature_col)==0):

        if len(primes)==0:
            raise Exception('Modular features for n cannot be computed without prime number list')
            
        mod_features = [data_df['n'].apply(lambda x: 1 if (x%prime==0 and x!=prime) else 0).values for prime in primes[:n_modular_features]]
        mod_features = np.array(mod_features).T
        mod_feature_col = [f"n_mod_{str(prime)}" for prime in primes[:n_modular_features]]

        if n_distance == 0:
            return pd.concat([data_df, pd.DataFrame(mod_features, columns=mod_feature_col)], axis=1)

        else:
            mod_df = pd.concat([data_df, pd.DataFrame(mod_features, columns=mod_feature_col)], axis=1)

    if n_distance > 0:
        mod_values_nplusx = np.roll(mod_df[mod_feature_col].values, - n_distance)
        # TODO extend boundary con
        for i in range(n_distance):
            mod_values_nplusx[-(i+1)] = np.ones(mod_values_nplusx.shape[1]) * 99 # artificial value 
            
        mod_nplusx_feature_col = [f"n+{n_distance}_{mod_feature_name[2:]}" for mod_feature_name in mod_feature_col]
        return pd.concat([data_df, pd.DataFrame(mod_values_nplusx, columns=mod_nplusx_feature_col)], axis=1)

    elif n_distance < 0:
        mod_values_nminusx = np.roll(mod_df[mod_feature_col].values, - n_distance)
        
        # TODO extend boundary con
        for i in range(-n_distance):
            mod_values_nminusx[i] = np.zeros(mod_values_nminusx.shape[1])
        
        mod_nminusx_feature_col = [f"n{n_distance}_{mod_feature_name[2:]}" for mod_feature_name in mod_feature_col]
        return pd.concat([data_df, pd.DataFrame(mod_values_nminusx, columns=mod_nminusx_feature_col)], axis=1)
