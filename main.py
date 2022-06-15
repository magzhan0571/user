import mysql.connector

db = mysql.connector.connect(
    host="srv-pleskdb49.ps.kz",
    port="3306",
    user="izderkz_magzhan",
    password="@Magzhan1201199445",
    database="izderkz_database"
)

cursor=db.cursor()

query="INSERT INTO db_f_1 VALUES(2, 12312, 'maga', 'man', 'username')"
cursor.execute(query)
db.commit()
print(cursor.lastrowid)
