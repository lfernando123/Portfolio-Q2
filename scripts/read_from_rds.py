# scripts/read_from_rds.py
import pymysql
import pandas as pd

def read_from_rds():
    # RDS MySQL connection details
    host = "mysql-db.xxxxxx.us-east-1.rds.amazonaws.com"  # Replace with your endpoint
    port = 3306
    user = "admin"  # Replace with your master username
    password = "your-password"  # Replace with your master password
    database = "booksdb"  # Replace with your database name

    # Establish connection
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    # Query to fetch data
    query = "SELECT * FROM Books"
    df = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    # Return the data
    return df

if __name__ == "__main__":
    df = read_from_rds()
    print(df.head())