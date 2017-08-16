#!/usr/bin/python
import sys
import Adafruit_DHT

import MySQLdb

print 'Truncating: TempHumid'

db = MySQLdb.connect(host= "localhost", user="root", passwd="password", db="monitoring")
cursor = db.cursor()

try:
   cursor.execute("""TRUNCATE TempHumid""")
   db.commit()
except:
   db.rollback()

db.close()

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %' .format(temperature, humidity)

    db = MySQLdb.connect(host= "localhost", user="root", passwd="password", db="monitoring")
    cursor = db.cursor()

    try:
       cursor.execute("""INSERT INTO TempHumid VALUES (unix_timestamp(now()),%s,%s)""",(temperature,humidity))
       db.commit()
    except:
       db.rollback()

    db.close()
