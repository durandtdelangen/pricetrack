#addproduct.py
import mysql.connector

sql_host="localhost"
sql_user="app_pricetrack"
sql_password="aS$Ysg5AepBKP#t3"
sql_database="pricetrack"
mydb = mysql.connector.connect(host=sql_host,user=sql_user,password=sql_password,database=sql_database)
mycursor = mydb.cursor()

try:
    while True:
        url = input("Please enter the URL to add to: ")
        split_url = url.split('/')
        sql = ("INSERT IGNORE INTO products (ProductID, ProductName, ProductURL) VALUES (%s,%s,%s);")
        val = (split_url[-1],split_url[-2],url)
        mycursor.execute(sql,val)
        mydb.commit()
        print ("Product " + split_url[-2] + " added.")
except KeyboardInterrupt:
    print ("\nCheers")

