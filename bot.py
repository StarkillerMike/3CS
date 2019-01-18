#imports for the api requests
import aiohttp
import random

#imports for discord and the database
import discord
import json
import mysql.connector
import asyncio

from discord import game
from discord.ext import commands

#insert your discord bot token here
#I've removed my own token because if you use it it would give you full control over my bot
TOKEN = ''


#data for the api requests
key =  'e20bc74149eb7451a37bec8314860c5a'
units = 'metric'
#Amsterdam
cityid = '2759794'
#Utrecht
cityid2 = '2745909'
#Purmerend
cityid3 = '2748413'



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
#This is mostly so you know what variables the bot expects with the different commands

#We've written these commands to show what different things we're capable of doing with this bot
#All the commands can be expended and changed to personal preference
#You can make them with more or less variables to give the user more or less input options

#We have connected 2 different databases to this bot, one that is on the Raspberry Pi (host1) itself (like this script is) and one that is on our laptop (host2).
#This is done as a way of creating a back-up database with the same changes as the main database
#But also because the database on the pi can't handle JSON Queries and the one on the laptop can

#If you're recreating this and use the laters version of the MySQL server there is no need for the second database and you could remove the double input lines

#This is all interchangeable to your own databases
#The database that it's connected to is only an example of some of the things that you can do with this bot

@client.command(pass_context=True)
async def showData(ctx, arg1):
   """Gebruik: .showData (name tabel) | Show the data from a table"""

   db = mysql.connector.connect(host="ip host1", user="username", password="password", database="name of database")

   cur = db.cursor()

   cur.execute("SHOW columns FROM "+ arg1)

   await client.say("This is the result: ") 
   await client.say("This are the columns: ")

   for row in cur.fetchall():
      column = str(row[0])
      await client.say(column)

   cur.execute("SELECT * FROM " + arg1)

   await client.say("This is the data: ")

   for row in cur.fetchall():
      rij1 = str(row[0])
      rij2 = str(row[1])
      rij3 = str(row[2])

      await client.say(rij1 + " -  " + rij2 + " -  " + rij3) 

   await client.say("----------")

   cur.close()
   db.close()

@client.command(pass_context=True)
async def showTables(): 
   """Usage: .showTables | Shows all the tables from the database"""
   db = mysql.connector.connect(host="ip host1", user="username", password="password", database="name of database")

   cur = db.cursor()

   myshow = "SHOW TABLES"
   cur.execute(myshow)

   await client.say("Here are all the tables: ")

   for row in cur.fetchall():
      naam = str(row[0])
      await client.say("Name: " + naam)


   await client.say("----------")

   cur.close()
   db.close() 

@client.command(pass_context=True)
async def makeName(arg1, arg2, arg3, arg4):
   """Usage: .makeName (firstname, lastname, active, married)"""
   db = mysql.connector.connect(host="ip host1", user="username", password="password", database="name of database")

   cur = db.cursor()
  
    
   myinsert = "INSERT INTO staff (firstname, lastname, active, married) VALUES (%s, %s, %s, %s)" 
   myvalues = (arg1, arg2, arg3, arg4)

   cur.execute(myinsert) 

   db.commit()

   await client.say("The name " + arg1 + arg2 + " with the values " + arg3 + arg4 + " is added to the database")


   await client.say("----------")

   cur.close()
   db.close()


   db = mysql.connector.connect(host="ip host2", user="username", password="password", database="name of database")

   cur = db.cursor()

   myinsert2 = "INSERT INTO staff (firstname, lastname, active, married) VALUES (%s, %s, %s, %s)"
   myvalues2 = (arg1, arg2, arg3, arg4)

   cur.execute(myinsert2)

   db.commit()

   cur.close()
   db.close() 


@client.command(pass_context=True)
async def makeTable(ctx, arg1):
   """Usage: .makeTable (name) | Creates a table in the database"""
   db = mysql.connector.connect(host="ip host1", user="username", password="password", database="name of database")

   cur = db.cursor()
   
   myvalue = (arg1)
   myinsert = "CREATE TABLE " + myvalue + " (`id` INT NOT NULL AUTO_INCREMENT, `firstname` VARCHAR(45) NOT NULL, `lastname` VARCHAR(45) NOT NULL, PRIMARY KEY (`id`, `firstname`, `lastname`))"

   cur.execute(myinsert)

   db.commit()

   await client.say("The table " + arg1 + " is created")


   await client.say("----------")

   cur.close()
   db.close() 

   db = mysql.connector.connect(host="ip host2", user="username", password="password", database="name of database")

   cur = db.cursor()

   myinsert2 = "CREATE TABLE " + myvalue + " (`id` INT NOT NULL AUTO_INCREMENT, `firstname` VARCHAR(45) NOT NULL, `lastname` VARCHAR(45) NOT NULL, PRIMARY KEY (`id`, `firstname`, `lastname`))" 

   cur.execute(myinsert2)

   db.commit()

   cur.close()
   db.close() 


@client.command(pass_context=True)
async def makeTable2(ctx, arg1, arg2, arg3):
   """Usage: .makeTable2 (name) (name for id) (name for second value)"""
   db = mysql.connector.connect(host="ip host1", user="username", password="password", database="name of database")

   cur = db.cursor()

   myvalue = (arg1)
   myvalue2 = (arg2)
   myvalue3 = (arg3)

   myinsert = "CREATE TABLE " + myvalue + " (  " + myvalue2 + " INT NOT NULL AUTO_INCREMENT, " + myvalue3 +  " VARCHAR(45) NOT NULL, PRIMARY KEY ( " + myvalue2 + ", " + myvalue3 + "))"

   cur.execute(myinsert)

   db.commit()

   await client.say("The table with the name: " + myvalue + " is created with the following variables: " + myvalue2 + " en " + myvalue3)

   await client.say("---------")

   cur.close()
   db.close() 


   db = mysql.connector.connect(host="ip host2", user="username", password="password", database="name of database")

   cur = db.cursor()

   myinsert2 = "CREATE TABLE " + myvalue + " (  " + myvalue2 + " INT NOT NULL AUTO_INCREMENT, " + myvalue3 +  " VARCHAR(45) NOT NULL, PRIMARY KEY ( " + myvalue2 + ", " + myvalue3 + "))"

   cur.execute(myinsert2)

   db.commit()

   cur.close()
   db.close()


#This command is an example of what a JSON Querie would look like
@client.command(pass_context=True)
async def json():
   """Usage: .json | JSON Querie that shows the first and lastname"""

   db = mysql.connector.connect(host="ip host2", user="username", password="password", database="name of database")

   cur = db.cursor()

   myshow = "SELECT (JSON_OBJECT(firstname, lastname)) FROM staff"
   cur.execute(myshow)

   await client.say("The Result: ")
   await client.say("firstname:    lastname:")

   for row in cur.fetchall():
      uitkomst = (str(row[0])) 

      await client.say(uitkomst)

   await client.say("----------")
   cur.close()
   db.close()





@client.command(pass_context=True)
async def searchName(ctx, arg1, arg2, arg3):
   """Usage: .searchName (name) (table name) (naam column) | Searches a name in the database"""
   db = mysql.connector.connect(host="ip host1", user="username", password="password", database="name of database")

   cur = db.cursor()

   myvalue = (arg1)
   myvalue2 = (arg2)
   myvalue3 = (arg3)

   myinsert = "SELECT * FROM " + myvalue2 + " WHERE " + myvalue3 + " LIKE " + "'%" +  myvalue + "%'" 

   cur.execute(myinsert)

   await client.say("Here are the results: ")

   for row in cur.fetchall():
      id = str(row[0]) 
      naam = str(row[1])
      actief = str(row[2])

      await client.say(id + " " + naam + " " + actief)

   await client.say("----------")

   cur.close()
   db.close()



#Commands for API Requests

@client.command()
async def weerAmsterdam():
   """Shows the weather from Amsterdam"""

   url = 'http://api.openweathermap.org/data/2.5/weather?id='+cityid+'&units='+units+'&APPID='+key

   async with aiohttp.ClientSession() as session:
      raw_response = await session.get(url)
      response = await raw_response.text()
      weather = json.loads(response)

      temp = ("The temperature: ", weather['main']['temp'], "Degrees C")
      wind = ("The wind: ", weather['wind']['speed'], "m/s speeds")
      clouds = ("The overcast: ", weather['clouds']['all'], "%")

      await client.say("The weather in Amsterdam")
      await client.say((temp))
      await client.say((wind))
      await client.say((clouds))


@client.command()
async def weerUtrecht():
   """Shows the weather from Utrecht"""

   url = 'http://api.openweathermap.org/data/2.5/weather?id='+cityid2+'&units='+units+'&APPID='+key

   async with aiohttp.ClientSession() as session:
      raw_response = await session.get(url)
      response = await raw_response.text()
      weather = json.loads(response)

      temp = ("The temperature: ", weather['main']['temp'], "Degrees C")
      wind = ("The wind: ", weather['wind']['speed'], "m/s speeds")
      clouds = ("The overcast: ", weather['clouds']['all'], "%")

      await client.say("The weather in Utrecht")
      await client.say((temp))
      await client.say((wind))
      await client.say((clouds))


@client.command()
async def weerPurmerend():
   """Shows the weather from Purmerend"""

   url = 'http://api.openweathermap.org/data/2.5/weather?id='+cityid3+'&units='+units+'&APPID='+key

   async with aiohttp.ClientSession() as session:
      raw_response = await session.get(url)
      response = await raw_response.text()
      weather = json.loads(response)

      temp = ("The temperature: ", weather['main']['temp'], "Degrees C")
      wind = ("The wind: ", weather['wind']['speed'], "m/s speeds")
      clouds = ("The overcast: ", weather['clouds']['all'], "%")

      await client.say("The weather in Purmerend")
      await client.say((temp))
      await client.say((wind))
      await client.say((clouds))


client.run(TOKEN)
