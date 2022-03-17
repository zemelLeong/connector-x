"""
Usage:
  tpch-pandas.py [--conn=<conn>] [--driver=<driver>]

Options:
  --conn=<conn>             The connection url to use [default: POSTGRES_URL].
  --driver=<driver>         The driver to use using sqlalchemy: https://docs.sqlalchemy.org/en/14/core/engines.html.
  -h --help                 Show this screen.
  --version                 Show version.

Drivers:
  PostgreSQL: postgresql, postgresql+psycopg2
  MySQL: mysql, mysql+mysqldb, mysql+pymysql
  Redshift: postgresql, redshift, redshift+psycopg2

"""

import os

from contexttimer import Timer
from sqlalchemy import create_engine
from docopt import docopt
import pandas as pd
import sqlite3
from clickhouse_driver import connect
from sqlalchemy.engine.url import make_url
from google.oauth2 import service_account

if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    table = os.environ["TPCH_TABLE"]
    driver = args.get("--driver", None)
    conn = os.environ[args["--conn"]]
    conn = make_url(conn)

    if conn.drivername == "sqlite":
        conn = sqlite3.connect(str(conn)[9:])
    elif conn.drivername == "bigquery":
        pass
    elif driver == "clickhouse":
        # clickhouse-driver uses native protocol: 9000
        conn = conn.set(drivername=driver, port=9000)
        conn = connect(str(conn))
    else:  # go with sqlalchemy
        if driver is not None:
            conn = conn.set(drivername=driver)
        print(f"conn url: {str(conn)}")
        engine = create_engine(conn)
        conn = engine.connect()


    with Timer() as timer:
        if conn.drivername == "bigquery":
            credentials = service_account.Credentials.from_service_account_file('/'+conn.database)
            df = pd.read_gbq(
                query=f"SELECT * FROM {table} limit 100",
                project_id="dataprep-bigquery",
                credentials=credentials
            )
            print(df)
        else:
            df = pd.read_sql(
                f"SELECT * FROM {table}",
                conn,
                parse_dates=[
                    "l_shipdate",
                    "l_commitdate",
                    "l_receiptdate",
                    "L_SHIPDATE",
                    "L_COMMITDATE",
                    "L_RECEIPTDATE",
                ],
            )
            conn.close()
    print(f"[Total] {timer.elapsed:.2f}s")
    
