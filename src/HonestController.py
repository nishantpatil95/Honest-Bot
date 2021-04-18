import discord
import random
import json
import DynamoLib
import string
import BotUtilsLib
from datetime import datetime
import RoleEngine
"""
Controller will be only one who will access databsae
"""
#HonestController
import ConfigLib

import LoggerLib
LOG=LoggerLib.getlogger()

def GetUserTimeStamp(MessageObject):
    lastupdatedxp=DynamoLib.GetMemberAttribute("LastUpdatedXPTime",MessageObject.author)
    if lastupdatedxp==None:
        return 0
    return lastupdatedxp

def GiveUserRandomXP(MessageObject,RXP):
    CurrentXP=DynamoLib.GetMemberAttribute("XP",MessageObject.author)
    if CurrentXP!=None:
        RXP=RXP+CurrentXP
    time_int=BotUtilsLib.to_integer(datetime.now())
    DynamoLib.SetMemberAttribute("XP",MessageObject.author,RXP)
    DynamoLib.SetMemberAttribute("LastUpdatedXPTime",MessageObject.author,time_int)

def IncreaseMsgCount(MessageObject):
    CurrentMsgCount=DynamoLib.GetMemberAttribute("TotalMessages",MessageObject.author)
    if CurrentMsgCount==None:
        CurrentMsgCount=0;
    DynamoLib.SetMemberAttribute("TotalMessages",MessageObject.author,CurrentMsgCount+1)

def GetHelpMode(ChannelObject,MemberObject):
    #Private Conditions
    #Guild-Master And Guild-Master channel or  Guild-Master And Private
    if discord.ChannelType.private==ChannelObject.type:
        if MemberObject.id==-1 or MemberObject.id ==-1:
            return True
        return False
    
    MemberRoles=MemberObject.roles
    MemberRolesIDs=[]
    for single_role in MemberRoles:
        MemberRolesIDs.append(single_role.id)
    AllowedRolesIDs=[]
    
    AllowedRolesIDs.append(ConfigLib.GetRoleIDByAlias("ROLE_GUILD_MASTER"))
    AllowedRolesIDs.append(ConfigLib.GetRoleIDByAlias("ROLE_GUILD_GUARDIAN"))
    
    a_set = set(AllowedRolesIDs) 
    b_set = set(MemberRolesIDs) 

    if (a_set & b_set):
        if ChannelObject.id== ConfigLib.GetChannelIDByAlias("CHNL_MASTER"):
            return True
    return False
    

def GetMemberInfo(GuildObject,MemberObject):
    MemberIntroduction=DynamoLib.GetMemberAttribute("Introduction",GuildObject,MemberObject)
    return MemberIntroduction



def SetUserWaifu(MemberObject,WaifuObject):
    DynamoLib.SetMemberAttribute("Waifu",MemberObject,WaifuObject)


def GetUserWaifu(MemberObject):
    WaifuObject=DynamoLib.GetMemberAttribute("Waifu",MemberObject)
    return WaifuObject 


def GetUserXP(MemberObject):
    UserXP=DynamoLib.GetMemberAttribute("XP",MemberObject)
    if UserXP==None:
        return 0
    return UserXP 
   
def GetAllUserData(MemberObject):
    return DynamoLib.GetAllMemberData(MemberObject)


def GetMemberClasses(MemberObject):
    ClassesArray=DynamoLib.GetMemberAttribute("Classes",MemberObject)
    if ClassesArray==None:
        MemberClass=RoleEngine.GetRandomClass()
        DynamoLib.SetMemberAttribute("Classes",MemberObject,MemberClass)
        ClassesArray=DynamoLib.GetMemberAttribute("Classes",MemberObject)
        if ClassesArray==None:
            LOG.error("Class is not assigned")
    return ClassesArray


def SetUserXP(MemberObject,XP):
    DynamoLib.SetMemberAttribute("XP",MemberObject,XP)


def GetLastSeenWaifu(MemberObject):
    WaifuObject=DynamoLib.GetMemberAttribute("LastSeenWaifu",MemberObject)
    return WaifuObject 
    
def SetLastSeenWaifu(MemberObject,WaifuObject):
    DynamoLib.SetMemberAttribute("LastSeenWaifu",MemberObject,WaifuObject)


def IsThisCommandAllowed(ChannelObject,MemberObject,cmd_name):
    CommandPermissionsChannels=ConfigLib.GetCommandInfo()
    for single_cmd in CommandPermissionsChannels:
        if single_cmd["Name"] == cmd_name:
            if ChannelObject.type==discord.ChannelType.private:
                return single_cmd["WorksInPrivate"]
              
            if ChannelObject.guild.id!=ConfigLib.GetCurrentGuild():
                LOG.critical("Command is used on Another Server")
                return False


            #Role will be available only in Public Channel
            AllowedChannels=single_cmd["ChannelsAllowed"]
            all_member_role=MemberObject.roles
            MemberRoleIDs=[]
            
            for single_role in all_member_role:
                MemberRoleIDs.append(single_role.id)
                
            for single_alias in AllowedChannels:
                if ConfigLib.GetChannelIDByAlias(single_alias) == ChannelObject.id:
                    AllowedRolesAlias=[]
                    
                    for single_role in single_cmd["RolesAllowed"]: 
                        AllowedRolesAlias.append(ConfigLib.GetRoleIDByAlias(single_role))
                    
                    a_set = set(AllowedRolesAlias) 
                    b_set = set(MemberRoleIDs) 
                    if (a_set & b_set): 
                        return True 
    return False

    


    
    
