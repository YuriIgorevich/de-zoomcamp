#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import pandas as pd
import sqlalchemy as sa
from textwrap import dedent
from time import perf_counter


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url

    csv_name = 'output.csv'
    data_dir = 'ny_taxi_data'
    csv_relpath = f'{data_dir}/{csv_name}'

    if url:
        import pathlib 
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
        os_command = dedent(f"""\
        wget -qO- {url} | \
        zcat > {csv_relpath}
        """)
        os.system(command=os_command)

    engine = sa.create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    iter_df = pd.read_csv(f'{csv_relpath}', iterator=True, chunksize=100_000)

    for i, df in enumerate(iter_df):
        t_start = perf_counter()
        
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        
        if i == 0:
            df.head(n=0).to_sql(name=table, con=engine, if_exists='replace')
        df.to_sql(name=table, con=engine, if_exists='append', index=False)
        t_end = perf_counter()
        print(f'inserted chunk #{i + 1} # recs = {len(df)} in {t_end - t_start:.3} sec.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db name for postgres')
    parser.add_argument('--table', help='table name to save results')
    parser.add_argument('--url', help='url of the csv file')
    args = parser.parse_args()

    main(args)
