import pandas as pd
import numpy as np

import sys
sys.path.insert(0, '../../data/pipeline/run/10_sbdb/')
import scoring

asteroid_null= pd.read_csv("../data/interim/asteroid_null_spec_B.csv",
                           index_col='id',
                           usecols=['id','albedo','diameter','H','GM','dv','moid','ad','a','q'],
                           nrows=1000

                           )
print(asteroid_null.shape)

asteroid_null_predictions= pd.read_csv("../data/interim/asteroid_null_spec_B_predictions.csv", nrows=1000)
print(asteroid_null_predictions.shape)

asteroid_null_predictions.index = asteroid_null.index

def nan_to_empty(row):
    return {x : '' if np.isreal(y) and np.isnan(y) else y for x,y in row.to_dict().items()}

for spec_col in ['spec_b.B','spec_b.C']:
    spec = spec_col.split('.')[1]
    print(spec)
    null_copy_df = asteroid_null.head(10000).copy()
    null_copy_df['spec'] = spec

    null_copy_df['closeness'] = null_copy_df.apply(lambda row: scoring.closeness_weight(nan_to_empty(row)), axis=1)

    null_copy_df['price'] = null_copy_df.apply(lambda row: scoring.price(nan_to_empty(row))[0], axis=1)

    print(null_copy_df[~np.isnan(null_copy_df['price'])].head(5))
    print(null_copy_df[~np.isnan(null_copy_df['closeness'])].head(5))

    null_copy_df['profit'] = null_copy_df.apply(lambda row: scoring.profit(nan_to_empty(row)), axis=1)

    print(null_copy_df[~np.isnan(null_copy_df['price']) & ~np.isnan(null_copy_df['closeness'])].head(5))

