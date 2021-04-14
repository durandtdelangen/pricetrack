#getprice.py
import requests
import json
from datetime import datetime
import mysql.connector

#SQL Database Connectiona
sql_host="10.1.110.21"
sql_user="crypto"
sql_password="yT6?ESBAP@nq!C7B"
sql_database="takealotprices"
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
    listing_price = str((u['buybox']['listing_price']))
    if listing_price == "None":
        listing_price = product_price
    #Get the items product name
    product_name = (u['title'])
    altprice=[]
    currencycode = (u['enhanced_ecommerce_add_to_cart']['ecommerce']['currencyCode'])   
    if 'other_offers' in u:
            for n in range(len(u['other_offers']['conditions'][0]['items'])):
                altprice.append(u['other_offers']['conditions'][0]['items'][n]['price']) 
    if altprice:
        bestprice = min(altprice)
        sql = "INSERT INTO prices (ProductID, ProductPrice, ProductRRP, BestAltPrice, CurrencyCode) VALUES (%s, %s, %s, %s, %s)"
        val = (url[0], product_price, listing_price, bestprice, currencycode)
        mycursor.execute(sql,val)
        mydb.commit()
    else:
        sql = "INSERT INTO prices (ProductID, ProductPrice, ProductRRP, CurrencyCode) VALUES (%s, %s, %s, %s)"
        val = (url[0], product_price, listing_price, currencycode)
        mycursor.execute(sql,val)
        mydb.commit()