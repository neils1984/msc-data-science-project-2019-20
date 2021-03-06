import config
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# MySQL connection
engine = config.engine

# Retrieve data - filter land registry data to non-commercial, price paid sales in Wycombe district only
epc_dep_qry = 'SELECT epc.*, dep.* ' \
              'FROM epc_cert epc LEFT JOIN postcode_lsoa_lookup pclsoa ON epc.postcode = pclsoa.pcds ' \
              'LEFT JOIN multiple_deprivation_2019 dep ON pclsoa.lsoa11cd = dep.lsoa_code ' \
              'WHERE left(postcode, 4) in ("HP10", "HP11", "HP12", "HP13", "HP15");'

epc_dep_data = pd.read_sql(sql=epc_dep_qry, con=engine)

lrp_qry = 'SELECT * FROM lr_price WHERE left(postcode, 4) in ("HP10", "HP11", "HP12", "HP13", "HP15") ' \
          'AND category = "A" and ptype != "O";'

lrp_data = pd.read_sql(sql=lrp_qry, con=engine)

# Create address_match fields with regular expression
# expr = '((flat\s\w*)|(([0-9]+)([a-z])?))'

# lrp_data['building_number'] = (lrp_data['saon'] + ' ' + lrp_data['paon']) \
#     .str.lower().apply(lambda x: extract_number(x, expr).strip())
# epc_data['building_number'] = epc_data['ADDRESS1'].str.lower().apply(lambda x: extract_number(x, expr))
epc_dep_data.columns = epc_dep_data.columns.str.lower()

lrp_data['address_match'] = (lrp_data['saon'].str.lower() + ' ' \
                             + lrp_data['paon'].str.lower().replace(',', '') + ' ' \
                             + lrp_data['street'].str.lower() + ' ' \
                             + lrp_data['locality'].str.lower()).str.strip()
epc_dep_data['address'] = epc_dep_data['address'].str.lower()

columns_to_add = list(epc_dep_data.columns[~epc_dep_data.columns.str.lower().isin(lrp_data.columns)])
# Merge datasets
merged_data = lrp_data.merge(epc_dep_data[columns_to_add], how='inner', left_on='address_match', right_on='address')

# Keep most recent EPC certificate and transaction, remove duplicated records
merged_data.sort_values(['inspection_date', 'transaction_date'], ascending=[False, False], inplace=True)
merged_data.drop_duplicates(subset=['address_match'], keep='first', inplace=True)
merged_data.reset_index(inplace=True, drop=True)

# Split data set into train and test sets and write each back to SQL database

y = merged_data['price']
X = merged_data.drop('price', axis=1)

np.random.seed(5)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

merged_data.to_sql('lrp_epc_merged', con=engine, index=False, chunksize=5000, if_exists='replace')

train = pd.concat([X_train, y_train], axis=1)
test = pd.concat([X_test, y_test], axis=1)

train.to_sql('train_data', con=engine, index=False, chunksize=5000, if_exists='replace')
test.to_sql('test_data', con=engine, index=False, chunksize=5000, if_exists='replace')
