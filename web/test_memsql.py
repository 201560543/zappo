import mysql.connector
conn = mysql.connector.connect(host='172.31.18.191', port='3306', user='root', database='information_schema')
cursor = conn.cursor()
cursor.execute('show tables')
print([r for r in cursor])
cursor.close()
conn.close()
