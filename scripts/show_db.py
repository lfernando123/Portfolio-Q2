import pymysql

connection = pymysql.connect(
    host="database-1.cvaim2ssqz52.ap-south-1.rds.amazonaws.com",
    user="admin",
    password="m7gYSSJdL0Vk0bW",
    port=3306
)

cursor = connection.cursor()
cursor.execute("SHOW DATABASES;")
databases = cursor.fetchall()
for db in databases:
    print(db[0])

connection.close()