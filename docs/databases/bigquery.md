# BigQuery

```{note}
BigQuery does not need to specify protocol.
```

### BigQuery Connection

**Authentication File:** BigQuery connection need an authentication json file from Google Cloud Platform. If you do not have an authentication json file, you can create your BigQuery authentication [here](https://cloud.google.com/docs/authentication/getting-started).

```py
import connectorx as cx
authentication_file_path = '/home/user/path/auth.json'      # path to your authentication json file
conn = 'bigquery://' + authentication_file_path             # connection token
query = 'SELECT * FROM `database.dataset.table`'            # query string
cx.read_sql(conn, query)                                    # read data from BigQuery
```

### BigQuery-Pandas Type Mapping
| BigQuery Type             |      Pandas Type            |  Comment                           |
|:-------------------------:|:---------------------------:|:----------------------------------:|
| Bool, Boolean             | bool, boolean(nullable)     |                                    |
| Int64, Integer            | int64, Int64(nullable)      |                                    |
| Float64, Float            | float64                     |                                    |
| Numeric                   | float64                     |                                    |
| String                    | object                      |                                    |
| BYTES                     | object                      |                                    |
| Time                      | object                      |                                    |
| DATE                      | datetime64[ns]              |                                    |
| Datetime                  | datetime64[ns]              |                                    |
| TIMESTAMP                 | datetime64[ns]              | UTC                                |