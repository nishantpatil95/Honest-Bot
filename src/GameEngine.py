
from datetime import datetime
import HonestController
import random
import math
import discord
import ConfigLib
import AssetsLib
import RoleEngine
import BotUtilsLib
import LoggerLib
LOG=LoggerLib.getlogger()

def to_integer(dt_time):
    milliseconds = int(round(dt_time.timestamp() * 1000))
    return milliseconds

def convertMillis(millis):
    millis = int(millis)
    
    seconds=(millis/1000)%60
    seconds = int(seconds)
    
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    
    hours=(millis/(1000*60*60))%24
    hours=int(hours)
    return (hours,":",minutes,":",seconds)

def getSeconds(millis):
    millis = int(millis)
    
    seconds=(millis/1000)%60
    seconds = int(seconds)
    
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    
    hours=(millis/(1000*60*60))%24
    hours=int(hours)
    return (hours*60*60)+(minutes*60)+seconds
    #return (hours,":",minutes,":",seconds)

def GetLevelFromXP(xp):
    if xp<=0:
        return 0
    level = math.floor((25 + math.sqrt(625 + 100 * xp)) / 50)
    return level

def GetXPFromLevel(level):
    if level<=0:
        return 0
    xp = 25 * level * level - 25 * level
    return xp
    

def GetUserCurrentLevel(MemberObject):
    MemberXP=HonestController.GetUserXP(MemberObject)
    return GetLevelFromXP(MemberXP)

#TODO::Time will be diff in dev and prod

def GiveUserXP(MessageObject):
    HonestController.IncreaseMsgCount(MessageObject)
    LastXPTime=HonestController.GetUserTimeStamp(MessageObject)
    #print(LastXPTime)
    now=to_integer(datetime.now())
    #print(convertMillis(now))
    #print(convertMillis(LastXPTime))
    if LastXPTime != 0:
        diff=now-LastXPTime
    else:
        diff=1000000000
   # print(convertMillis(diff),getSeconds(diff))
    #TODO:: take constants from database only
    if(getSeconds(diff)>0):
        UserrandomXP=random.randint(25,50)
        HonestController.GiveUserRandomXP(MessageObject,UserrandomXP)

#TODO:: Databased this
IsBattleRunnning=False

CurrentBoss={}

async def BeginBattle(bot,Context,BossName):
    global IsBattleRunnning
    global CurrentBoss
    if not IsBattleRunnning:
        BossJsonObject=AssetsLib.GetAllBossInfo(BossName)
        if BossJsonObject==None:
            await Context.channel.send("No boss found")
            return 
        
        CurrentBoss=BossJsonObject
        battlechannel=bot.get_channel(ConfigLib.GetChannelIDByAlias("CHNL_ARENA_BASIC"))
        print("Staring battle:",CurrentBoss)
        
        #battlechannel.send(CurrentBoss)
        
        await battlechannel.send(file=discord.File(CurrentBoss["Image"]))
        await battlechannel.send(CurrentBoss["Intro"])
        await battlechannel.send("HP:"+str(CurrentBoss["XP"]))
        IsBattleRunnning=True
        
        
    #Send msg in Battle arena





def EndBattle():
    global IsBattleRunnning
    IsBattleRunnning=False



def GetMemberAttacks(MemberObject):
    MemberRoles=MemberObject.roles
    RoleAttacks=ConfigLib.GetRoleAttacks()
    AttackObject={}
    for rakeys in RoleAttacks.keys():
        for memberrole in  MemberRoles:
            if ConfigLib.GetRoleIDByAlias(rakeys)==memberrole.id:
                for SingleAttack in RoleAttacks[rakeys].keys():
                    AttackObject[SingleAttack]=RoleAttacks[rakeys][SingleAttack]
        
    return AttackObject 
    HonestController.SetMemberAttacks(MemberObject,AttackObject)


async def Attack(Context,AttackName):
    global IsBattleRunnning
    global CurrentBoss
    #TODO::Delete Old Msgs When Battle is running
    if not IsBattleRunnning:
        return
    AttackName=AttackName.lower()
    AttacksArray=AssetsLib.GetAttacks()
    AttackFound=False
    for SingleAttack in AttacksArray:
        if AttackName==SingleAttack["Name"]:
            AttackFound=True
    
    if not AttackFound:
        await Context.channel.send(BotUtilsLib.GetBotDialogByKey("DLG_ATK_NOTFOUND",MentionMember=Context.author))
        return


    #TODO::Check Attack Limit Here
    
    MemberAttacks=GetMemberAttacks(Context.author)
    
    if AttackName in MemberAttacks.keys():
        AttackInfo=MemberAttacks[AttackName]
        Damage=random.randint(AttackInfo["dmgmin"],AttackInfo["dmgmax"])
        CurrentBoss["XP"]=CurrentBoss["XP"]-Damage
        await Context.channel.send(file=discord.File(CurrentBoss["Image"]))
        await Context.channel.send("HP:"+str(CurrentBoss["XP"]))
        await Context.channel.send(BotUtilsLib.GetBotDialogByKey("DLG_ATK_DAMAGE",MentionMember=Context.author)+str(Damage))
    else:
        await Context.channel.send(BotUtilsLib.GetBotDialogByKey("DLG_ATK_NOTAVAIL",MentionMember=Context.author))
    
    
    
    
    #Check MemberRole
    #Function to get member attacks
    #check if attack name available or not
    #Perform Damage
    #UpdateUsageInMemberModel
    #StoreUserBattleRecordInDatabase
    
    #Later
    
        #Attacks
        #Attacks    UseCount
        #DamageDone





async def ManageLevel(bot,MessageObject):
    CurrentLevel=GetUserCurrentLevel(MessageObject.author)
    GiveUserXP(MessageObject)
    NewLevel=GetUserCurrentLevel(MessageObject.author)
    if CurrentLevel<NewLevel:
        await MessageObject.channel.send(BotUtilsLib.GetBotDialogByKey("DLG_LEVEL_UP",MentionMember=MessageObject.author,MentionLevel=NewLevel))
        await RoleEngine.UpdateMemberRole(MessageObject.author,NewLevel)
    
   
        
def GetAllUserInfo(Context):
    AllUserData=HonestController.GetAllUserData(Context.author)
    #print(AllUserData)
    UserDataToBeSend={}
    UserDataToBeSend["Name"]=Context.author.name
    UserDataToBeSend["XP"]=AllUserData["XP"]
    UserDataToBeSend["TotalMessages"]=AllUserData["TotalMessages"]
    UserDataToBeSend["Level"]=GetLevelFromXP(AllUserData["XP"])
    UserDataToBeSend["PrevLevelXP"]=GetXPFromLevel(UserDataToBeSend["Level"]-1)
    UserDataToBeSend["NextLevelXP"]=GetXPFromLevel(UserDataToBeSend["Level"]+1)
    UserDataToBeSend["AvatarURL"]=Context.author.avatar_url
    
    #do additional computation
    #for index in range(1,100):
    #    print(index,GetXPFromLevel(index))
    #calculate level
    #compute role may be
    userroles=[]
    for single_role in Context.author.roles:
        userroles.append(single_role.name)
    UserDataToBeSend["Roles"]=userroles
    
    
    return UserDataToBeSend
    
    
#def MakeUserFile(AllUserData)
    
    
    
    
    
    
    
    
    
    
    
    

        
    
