#getprice.py

import requests
import json
from datetime import datetime
import mysql.connector

#SQL Database Connectiona
sql_host="localhost"
sql_user="root"
sql_password="jPQ3iTc5d$geN6bG"
sql_database="pricetrack"
mydb = mysql.connector.connect(host=sql_host,user=sql_user,password=sql_password,database=sql_database)
mycursor = mydb.cursor()

sqlquery = mycursor.execute("SELECT ID,ProductURL FROM products;")
urls = mycursor.fetchall()

for url in urls:
    #print (url)
    split_url = url[1].split('/')
    #print (split_url)
    product_id = split_url[-1].rstrip()
    #print (product_id)
    apiurl = 'https://api.takealot.com/rest/v-1-10-0/product-details/' + product_id + '?platform=desktop'
    #print (apiurl)
    #Get JSON file from TakeAlot API as response
    s = requests.get (apiurl) 
    #Convert response to text to enable conversion to json/dictionary
    t = (s.text) 
    #Convert t to json/dictionary
    u = json.loads(t)
    #Get current price of item (returns a list with only one item)
    v = (u['buybox']['prices'])
    #Convert current price to string
    product_price = str((v[0]))
    #Get the supposed list price of the item
    listing_price = str((u['buybox']['listing_price']))a
    if listing_price == "None":
        listing_price = product_price
    #Get the items product name
    product_name = (u['title'])
    #Get current date and time
    time = str(datetime.now())
    altprice=[]
    if 'other_offers' in u:
            for n in range(len(u['other_offers']['conditions'][0]['items'])):
                altprice.append(u['other_offers']['conditions'][0]['items'][n]['price']) 
    if altprice:
        bestprice = min(altprice)
        sql = "INSERT INTO prices (ProductID, ProductPrice, ProductRRP, timestamp, BestAltPrice) VALUES (%s, %s, %s, %s, %s)"
        val = (url[0], product_price, listing_price, time, bestprice)
        mycursor.execute(sql,val)
        mydb.commit()
    else:
        sql = "INSERT INTO prices (ProductID, ProductPrice, ProductRRP, timestamp) VALUES (%s, %s, %s, %s)"
        val = (url[0], product_price, listing_price, time)
        mycursor.execute(sql,val)
        mydb.commit()