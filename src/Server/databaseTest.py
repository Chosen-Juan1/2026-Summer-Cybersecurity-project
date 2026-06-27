# import sys
# print(sys.path)

from psycopg2.extras import DictCursor
from Database.pgconfig import pg_config, connect_string
import psycopg2 as pg
def dbTest(query):

    # query = 
    conn = pg.connect(connect_string())
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query)

    rows = cursor.fetchall()
    print(rows, flush = True)
    cursor.close()
    conn.close()
    return rows



if __name__ == "__main__":

    dbTest("""select *
             from users;""")