from datetime import datetime
import HonestController
import random
import math
import discord
import ConfigLib
import BotUtilsLib
from pprint import pprint

import LoggerLib
LOG=LoggerLib.getlogger()


def GetRandomClass():
    AvailClasses=["CLASS_WAR","CLASS_RAN","CLASS_SUM","CLASS_SOR"]
    return random.sample(AvailClasses,1)

def IsMemberHasRole(MemberObject,RoleName):
    for singleRole in MemberObject.roles:
        if singleRole.id == ConfigLib.GetRoleIDByAlias(RoleName): 
            return True
    return False

async def AddRoleMember(MemberObject,RoleName):
    RoleObject=MemberObject.guild.get_role(int(ConfigLib.GetRoleIDByAlias(RoleName)))
    await MemberObject.add_roles(RoleObject)

async def RemoveRoleMember(MemberObject,RoleName):
    RoleObject=MemberObject.guild.get_role(int(ConfigLib.GetRoleIDByAlias(RoleName)))
    await MemberObject.remove_roles(RoleObject)


async def AddRemoveRoles(MemberObject,RolesArray):
    MemberCurrentRoles=MemberObject.roles
    RolesTobeRemoved=["ROLE_TRAINEE","ROLE_WAR","ROLE_SUM","ROLE_SOR","ROLE_RAN","ROLE_ELDR_WAR","ROLE_ELDR_SUM","ROLE_ELDR_SOR","ROLE_ELDR_RAN","ROLE_LEGEND_WAR","ROLE_LEGEND_SUM","ROLE_LEGEND_SOR","ROLE_LEGEND_RAN"]
    

    RolesTobeRemovedFiltered=[]
    for singlerole in MemberCurrentRoles:
        for singleroletoberemoved in RolesTobeRemoved:
            if singlerole.id == int(ConfigLib.GetRoleIDByAlias(singleroletoberemoved)):
                RolesTobeRemovedFiltered.append(singleroletoberemoved)

    for singlerole in RolesTobeRemovedFiltered:
        if not singlerole in RolesArray:
            await RemoveRoleMember(MemberObject,singlerole)

    for singlerole in RolesArray:
        LOG.info("Adding role::{}".format(singlerole))
        await AddRoleMember(MemberObject,singlerole)



async def UpdateMemberRole(MemberObject,level):
    LevelSlabs=ConfigLib.GetLevelUps()
    for singleslab in LevelSlabs.keys():
        if  LevelSlabs[singleslab]["MinLevel"]<=level and level <=LevelSlabs[singleslab]["MaxLevel"]:
            LOG.info("M:{} SLB:{}".format(MemberObject.name,singleslab))
            ClassRoles=LevelSlabs[singleslab]["ROLES"]
            MemberClassArray=HonestController.GetMemberClasses(MemberObject)
            NewMembersRoles=[]
            #pprint(ClassRoles)
            #pprint(MemberClassArray)
            for SingleClass in MemberClassArray:
                LOG.info(SingleClass)
            for ClassKey in ClassRoles.keys():
                for MemberClassKey in MemberClassArray:
                    if MemberClassKey==ClassKey:
                        NewMembersRoles.append(ClassRoles[ClassKey])
            
        

            await AddRemoveRoles(MemberObject,NewMembersRoles) 

