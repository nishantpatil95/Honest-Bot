#! /usr/bin/env python3
#Imports
import sys
import os
import HonestBot
import LoggerLib

# Credentials
TOKEN = os.getenv('BOT_TOKEN')

if TOKEN==None:
    sys.exit('No token found')

#print(TOKEN)
BOT_PREFIX=['ht ','Ht ']

client = HonestBot.MyBot(TOKEN,BOT_PREFIX)
client.RunBot()
