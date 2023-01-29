import argparse
import pandas as pd
import os
from sqlalchemy import create_engine
from time import time
import pyarrow.parquet as pq


def main(params):
    user = params.user
    password =params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    parquet_name = 'output.parquet'

    #download the csv
    os.system(f"wget {url} -O {parquet_name}")

    _file = pq.ParquetFile(parquet_name)

    batches = _file.iter_batches(batch_size = 10000) #batches will be a generator

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # pd.io.sql.get_schema(df, name = "yellow_taxi_data", con=engine)

    for data_chunk in batches:

        t_start = time()

        df_chunk = data_chunk.to_pandas()
        df_chunk['tpep_pickup_datetime'] = pd.to_datetime(df_chunk.tpep_pickup_datetime)
        df_chunk['tpep_dropoff_datetime'] = pd.to_datetime(df_chunk.tpep_dropoff_datetime)

        t_end = time()
        df_chunk.to_sql(name=table_name, con=engine, if_exists='append')

        print('inserted another chunk..., tool %.3f second' % (t_end - t_start))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user',help='username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database for postgres')
    parser.add_argument('--table_name',help='table name where we will write the results to')
    parser.add_argument('--url',help='csv url')

    args = parser.parse_args()

    main(args)

