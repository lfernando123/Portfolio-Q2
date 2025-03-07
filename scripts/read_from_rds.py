# scripts/read_from_rds.py
import pymysql
import pandas as pd

def read_data():
    # RDS MySQL connection details
    host = "database-1.cvaim2ssqz52.ap-south-1.rds.amazonaws.com"
    port = 3306
    user = "admin"
    password = "m7gYSSJdL0Vk0bW"
    database = "dbBOOKS"

    # Establish connection
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    # Query to fetch data
    query = "SELECT * FROM tBooks where Rating = 'Five'"
    df = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    # Return the data
    return df

if __name__ == "__main__":
    df = read_data()
    print(df.head())