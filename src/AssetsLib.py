import discord
import random
import json
import string
import glob
import os
from pprint import pprint
import datetime
import LoggerLib
LOG=LoggerLib.getlogger()


QuotesList=[]
MotivationsList=[]
WaifusData=[]
BossData=[]
Attacks=[]
HonestTenVideos=[]

def InitializeWaifus():
    global WaifusData
    WaifuFolderAll=os.path.join(os.getenv('ASSETS_DIR'),'waifus')
    WaifuFolderAll=WaifuFolderAll+"/*.*"
    WaifusPaths=glob.glob(WaifuFolderAll)
    for single_file_path in WaifusPaths:
        WaifuData={
                            "Name":os.path.basename(single_file_path).replace(".JPG",""),
                            "FilePath":single_file_path
                    }

        WaifusData.append(WaifuData)

def GetRandomWaifu():
    global WaifusData
    return WaifusData[random.randint(0,len(WaifusData)-1)]

def InitializeMotivation():
    filename = os.path.join(os.getenv('ASSETS_DIR'),'motivation.txt')
    quotesfile = open(filename, "rb")
    global MotivationsList
    for index,line in enumerate(quotesfile):
        if line != "" or line != "\n":
            MotivationsList.append(line.decode('utf-8'))

def InitializeQuotes():
    filename = os.path.join(os.getenv('ASSETS_DIR'),'anime-quotes.txt')
    quotesfile = open(filename, "rb")
    global QuotesList
    for index,line in enumerate(quotesfile):
        if line != "" or line != "\n":
            QuotesList.append(line.decode('windows-1252'))


def GetAllBossInfo(boss_name):
    global BossData
    if boss_name in BossData.keys():
        return BossInfo[boss_name]
    else:
        return None


def GetRandomMotivation():
    global MotivationsList
    return random.sample(MotivationsList,1)


def GetRandomQuote():
    return random.sample(QuotesList,1)


def LoadAssetsData(assetname):

    global BossData
    global Attacks
    global HonestTenVideos
    filename = os.path.join(os.getenv('ASSETS_DIR'),assetname+'.json')
    
    JsonData=None
    with open(filename, 'rb') as outfile:
        JsonData=json.load(outfile)

    if JsonData==None:
        sys.exit('DataNotLoaded::'+assetname)

    if assetname=='BossInfo':
        for singlekey in JsonData.keys():
            JsonData[singlekey]["Image"]=os.path.join(os.getenv('ASSETS_DIR'),'bosses',JsonData[singlekey]["Name"]+".jpeg")
        BossData=JsonData

    if assetname=='HonestTen':
        for SingleVideo in JsonData:
            SingleVideo["PublishedTime"]=datetime.datetime.strptime(SingleVideo["time"],"%Y-%m-%dT%H:%M:%SZ")
        HonestTenVideos=JsonData
        HonestTenVideos.sort(key=lambda r: r["PublishedTime"])

    if assetname=='Attacks':
        Attacks=JsonData
    LOG.info("Assets Loaded Successfully {0}".format(assetname))


def GetHonestTenVideo(recent=False,query=""):
    global HonestTenVideos
    if recent:
        return HonestTenVideos[:3]
    elif query!="":
        matchedtoquery=[]
        for HonestVideo in HonestTenVideos:
            if query.lower() in HonestVideo["title"].lower():
                matchedtoquery.append(HonestVideo)
                if len(matchedtoquery)>2:
                    return matchedtoquery

        return matchedtoquery
    else:
        return random.sample(HonestTenVideos,1)
    


def InitializeAssets():
    LOG.info("Assets Path:{0}".format(os.getenv('ASSETS_DIR')))

    AssetsList=['BossInfo','HonestTen','Attacks']

    for AssetName in AssetsList:
        LoadAssetsData(AssetName)

    InitializeWaifus();
    InitializeQuotes()
    InitializeMotivation()


InitializeAssets()





