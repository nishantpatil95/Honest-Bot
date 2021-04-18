import discord
import random
import json
import string
import glob
import os
from pprint import pprint

import LoggerLib
LOG=LoggerLib.getlogger()

MasterConfigData={}


def GetCurrentGuild():
    global MasterConfigData
    return MasterConfigData["GuildInfo"]["GUILD_ID"]


def GetRoleAttacks():
    global MasterConfigData 
    return MasterConfigData["RoleAttacks"]

def GetRoleIDByAlias(DummyName):
    global MasterConfigData 
    return MasterConfigData['GuildInfo']['ROLES'][DummyName]

def GetRoleIDs():
    global MasterConfigData 
    return MasterConfigData['GuildInfo']['ROLES']

def GetBotDialogue(DummyName):
    global MasterConfigData 
    BotDialogues=MasterConfigData['Dialogue']
    if DummyName in BotDialogues.keys():
        return BotDialogues[DummyName]
    else:
        return None

def GetDlgKeys():
    global MasterConfigData 
    BotDialogues=MasterConfigData['Dialogue']
    return BotDialogues.keys()

def GetCommandInfo():
    global MasterConfigData 
    return MasterConfigData['Commands']


def GetChannelIDByAlias(DummyName):
    global MasterConfigData 
    return MasterConfigData['GuildInfo']['CHANNELS'][DummyName]

def GetChannelIDs():
    global MasterConfigData 
    return MasterConfigData['GuildInfo']['CHANNELS']
   

def GetLevelUps():
    global MasterConfigData 
    return MasterConfigData['LevelUps']
   

def LoadConfigFileData(configname):
    global MasterConfigData

    TestGuild=""
    if configname == "GuildInfo":
        TestGuild="Test" if os.getenv('ENV_NAME')=='dev' else "" 

    filename = os.path.join(os.getenv('CONFIG_DIR'),configname+TestGuild+'.json')
    MasterConfigData[configname]=None

    with open(filename, 'rb') as outfile:
        MasterConfigData[configname]=json.load(outfile)

    if MasterConfigData[configname]==None:
        sys.exit('DataNotLoaded::'+configname)

    if configname=='Dialogue':
        for sindlgkey in MasterConfigData[configname].keys():
            if not type(MasterConfigData[configname][sindlgkey]) is str:    
                MasterConfigData[configname][sindlgkey]="".join(MasterConfigData[configname][sindlgkey])

    if configname=='Commands':
        for single_cmd in MasterConfigData[configname]:
            single_cmd["Description"]=MasterConfigData['Dialogue'][single_cmd["Description"]]
        
        for key in MasterConfigData['GuildInfo']['CHANNELS'].keys():
            for single_cmd in MasterConfigData[configname]:
                if key in single_cmd["Description"]:
                    single_cmd["Description"]=single_cmd["Description"].replace(key,"<#"+str(GetChannelIDByAlias(key))+">")
    

    LOG.info("Config Loaded Successfully {0}".format(configname))
    #print("Config Loaded Successfully -> ",configname)




def InitializeConfig():

    LOG.info("EnvName::{}".format(os.getenv('ENV_NAME')))

    LOG.info("Config Path:{0}".format(os.getenv('CONFIG_DIR')))

    ConfigList=['GuildInfo','Dialogue','Commands','RoleAttacks','LevelUps']

    for ConfigName in ConfigList:
        LoadConfigFileData(ConfigName) 



InitializeConfig()
