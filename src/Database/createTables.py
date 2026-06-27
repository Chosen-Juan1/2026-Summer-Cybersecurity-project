import subprocess
from pgconfig import pg_config, connect_string
import os


if __name__ == "__main__":
    #cleaning db


    env = os.environ.copy()
    env["PGPASSWORD"] = pg_config["password"]

    command = f"psql -h {pg_config['host']} -d {pg_config['dbname']} -U {pg_config['user']} -p {pg_config['port']} -a -f wipe_db.sql"
    #now fill it up
    subprocess.run(command.split(), env=env, check=True)

    command = f"psql -h {pg_config['host']} -d {pg_config['dbname']} -U {pg_config['user']} -p {pg_config['port']} -a -f create_tables.sql"

    # command = f"psql postgresql://{pg_config['user']}:{pg_config['password']}@{pg_config['host']}:{pg_config['port']}/{pg_config['dbname']} -a -f ETL/create_tables.sql"
    print("\n bout to run the command")
    subprocess.run(command.split(), env=env, check=True)
    print("\n ran the command")