import pandas as pd
from pgconfig import pg_config, connect_string
import psycopg2 as pg
from psycopg2.extras import execute_batch


df = pd.read_csv('dummy_data.csv')
# print(df)

tupOfVals = []
for index, row in df.iterrows():
    val = tuple([row['Username'], row['Password']])
    tupOfVals.append(val)
tupOfVals = tuple(tupOfVals)


#Insert into location_ping (ping_id, vehicle_id, ts, geom, speed_kph, heading_deg)
    #Values (%s, %s, %s, ST_GeomFromEWKB(decode(%s,'hex')), %s, %s)
query = """Insert into users (username, password_hash)
            Values (%s, %s);"""

conn = pg.connect(connect_string())
cursor = conn.cursor()
data = tupOfVals
execute_batch(cursor, query, data)
conn.commit()
print("users data loaded.")
cursor.close()
conn.close()