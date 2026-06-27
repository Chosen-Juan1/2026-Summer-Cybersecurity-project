import os
import psycopg2 as pg
from dotenv import load_dotenv
load_dotenv()



    # cb stop commenting this no quiero explotar el db de render
# pg_config = {
#         "user" : "user",
#         "password" : "1234",
#         "dbname" : "demo",
#         "port" : "8991",
#         "host" : "localhost"
#     }

#for intercontainer coms 
pg_config = {
        "user" : "user",
        "password" : "1234",
        "dbname" : "demo",
        "port" : "5432",
        # "port" : "8991",

        "host" : "localhost"
    }


def connect_string():

    string = []
    for key, value in pg_config.items():
        string.append(f"{key}={value}")
    return " ".join(string)

if __name__ == "__main__":
    print("\n",connect_string(),"\n")
    conn = pg.connect(connect_string())
    query = """SELECT * 
    FROM user;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        print(row, "\n")
    # print(conn)
    print("Connected\n")
