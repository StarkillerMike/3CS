import discord
import json

import mysql.connector
import asyncio

from discord.ext import commands

#insert your discord bot token here
#I've removed my own token because if you use it it would give you full control over my bot
TOKEN = ''

#You can add a customised description for the bot
description = '''3CS Bot, for all your database connections'''
#You can change the prefix that you use to call the bot
client = commands.Bot(command_prefix = '.', description=description)

#You can also customise the status that the bot has when it's online
#This even is mostly to let me know that the bot has come online succesful and that it's ready for usage
@client.event
async def on_ready():
   await client.change_presence(game=discord.Game(name='Filling the Databases'))
   print('Bot is ready')

#This is where the different commands start
#I've written little explenations of what the commands do and how you can use then
#This is mostly so a user knows what variables the bot expects with the different commands
#The database that i have it connected to is a local database that i have on my raspberry Pi, this is also where I launch my bot
#hince the 120.0.0.1 host ip
#The second ip (192.168.1.211) is the IP that the back-up database is
#This database also has a different version that allows us to request JSON Queries from the database

#This is all interchangeable to your own databases
#The database that it's connected to is only an example of some of the things that you can do with this bot

@client.command(pass_context=True)
async def krijgData(ctx, arg1):
   """Gebruik: .krijgData (naam tabel) | Krijgt alle data uit een genoemde tabel"""

   db = mysql.connector.connect(host="127.0.0.1", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   cur.execute("SHOW columns FROM "+ arg1)

   await client.say("Dit is de uitkomst: ") 
   await client.say("Dit zijn de columns: ")

   for row in cur.fetchall():
      column = str(row[0])
      await client.say(column)

   cur.execute("SELECT * FROM " + arg1)

   await client.say("Dit is de data: ")

   for row in cur.fetchall():
      rij1 = str(row[0])
      rij2 = str(row[1])
      rij3 = str(row[2])

      await client.say(rij1 + " -  " + rij2 + " -  " + rij3) 

   await client.say("----------")

   cur.close()
   db.close()

@client.command(pass_context=True)
async def zieTables(): 
   """Begruik: .zieTables | Laat alle tables zien uit de database"""
   db = mysql.connector.connect(host="127.0.0.1", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   myshow = "SHOW TABLES"
   cur.execute(myshow)

   await client.say("Hier zijn alle tables: ")

   for row in cur.fetchall():
      naam = str(row[0])
      await client.say("Naam: " + naam)


   await client.say("----------")

   cur.close()
   db.close() 

@client.command(pass_context=True)
async def maakNaam(arg1, arg2, arg3, arg4):
   """Gebruik: .maakNaam (firstname, lastname, active, married)"""
   db = mysql.connector.connect(host="127.0.0.1", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()
  
    
   myinsert = "INSERT INTO staff (firstname, lastname, active, married) VALUES (%s, %s, %s, %s)" 
   myvalues = (arg1, arg2, arg3, arg4)

   cur.execute(myinsert) 

   db.commit()

   await client.say("De naam " + arg1 + arg2 + " met de waarden " + arg3 + arg4 + " is toegevoegd")


   await client.say("----------")

   cur.close()
   db.close()


   db = mysql.connector.connect(host="192.168.1.211", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   myinsert2 = "INSERT INTO staff (firstname, lastname, active, married) VALUES (%s, %s, %s, %s)"
   myvalues2 = (arg1, arg2, arg3, arg4)

   cur.execute(myinsert2)

   db.commit()

   cur.close()
   db.close() 


@client.command(pass_context=True)
async def maakTable(ctx, arg1):
   """Gebruik: .maakTable (naam) | Voegt een tabel toe in de database"""
   db = mysql.connector.connect(host="127.0.0.1", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()
   
   myvalue = (arg1)
   myinsert = "CREATE TABLE " + myvalue + " (`id` INT NOT NULL AUTO_INCREMENT, `firstname` VARCHAR(45) NOT NULL, `lastname` VARCHAR(45) NOT NULL, PRIMARY KEY (`id`, `firstname`, `lastname`))"

   cur.execute(myinsert)

   db.commit()

   await client.say("De table " + arg1 + " is toegevoegd")


   await client.say("----------")

   cur.close()
   db.close() 

   db = mysql.connector.connect(host="192.168.1.211", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   myinsert2 = "CREATE TABLE " + myvalue + " (`id` INT NOT NULL AUTO_INCREMENT, `firstname` VARCHAR(45) NOT NULL, `lastname` VARCHAR(45) NOT NULL, PRIMARY KEY (`id`, `firstname`, `lastname`))" 

   cur.execute(myinsert2)

   db.commit()

   cur.close()
   db.close() 


@client.command(pass_context=True)
async def maakTabel2Extra(ctx, arg1, arg2, arg3):
   """Gebruik: .maakTable2Extra (naam) (naam voor id) (naam voor 2e waarde)"""
   db = mysql.connector.connect(host="127.0.0.1", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   myvalue = (arg1)
   myvalue2 = (arg2)
   myvalue3 = (arg3)

   myinsert = "CREATE TABLE " + myvalue + " (  " + myvalue2 + " INT NOT NULL AUTO_INCREMENT, " + myvalue3 +  " VARCHAR(45) NOT NULL, PRIMARY KEY ( " + myvalue2 + ", " + myvalue3 + "))"

   cur.execute(myinsert)

   db.commit()

   await client.say("De table met de naam: " + myvalue + " is gemaakt met de variabelen: " + myvalue2 + " en " + myvalue3)

   await client.say("---------")

   cur.close()
   db.close() 


   db = mysql.connector.connect(host="192.168.1.211", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   myinsert2 = "CREATE TABLE " + myvalue + " (  " + myvalue2 + " INT NOT NULL AUTO_INCREMENT, " + myvalue3 +  " VARCHAR(45) NOT NULL, PRIMARY KEY ( " + myvalue2 + ", " + myvalue3 + "))"

   cur.execute(myinsert2)

   db.commit()

   cur.close()
   db.close()


@client.command(pass_context=True)
async def test():
   """Gebruik: .test | test connectie met laptop"""
   db = mysql.connector.connect(host="192.168.1.211", user="mike", password="wachtwoord", database="3cs")


   cur = db.cursor()

   myshow = "SHOW TABLES"
   cur.execute(myshow)

   await client.say("Hier zijn alle tables: ")

   for row in cur.fetchall():
      naam = str(row[0])
      await client.say("Naam: " + naam)

   cur.close()
   db.close()

@client.command(pass_context=True)
async def json():
   """Gebruik: .json | JSON Querie van de database"""

   db = mysql.connector.connect(host="192.168.1.211", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   myshow = "SELECT (JSON_OBJECT(firstname, lastname)) FROM staff"
   cur.execute(myshow)

   await client.say("Het resultaat: ")
   await client.say("firstname:    lastname:")

   for row in cur.fetchall():
      uitkomst = (str(row[0])) 

      #rare leestekens weg halen

      await client.say(uitkomst)

   await client.say("----------")
   cur.close()
   db.close()





@client.command(pass_context=True)
async def zoekNaam(ctx, arg1, arg2, arg3):
   """Gebruik: .zoekNaam (naam) (naam table) (naam column) | Zoekt een naam in de DB"""
   db = mysql.connector.connect(host="127.0.0.1", user="mike", password="wachtwoord", database="3cs")

   cur = db.cursor()

   myvalue = (arg1)
   myvalue2 = (arg2)
   myvalue3 = (arg3)

   myinsert = "SELECT * FROM " + myvalue2 + " WHERE " + myvalue3 + " LIKE " + "'%" +  myvalue + "%'" 

   cur.execute(myinsert)

   await client.say("Hier is het gevonden resultaat: ")

   for row in cur.fetchall():
      id = str(row[0]) 
      naam = str(row[1])
      actief = str(row[2])

      await client.say(id + " " + naam + " " + actief)

   await client.say("----------")

   cur.close()
   db.close()



client.run(TOKEN)
