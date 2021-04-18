import HonestController
import discord
import discord.utils
import random
from PIL import Image, ImageDraw, ImageFont
import GameEngine
import ConfigLib
import BotUtilsLib
import sys
import traceback
from discord.ext import tasks,commands
from pprint import pprint
import AssetsLib
import LoggerLib
LOG=LoggerLib.getlogger()


def decorator_command_validator(OriginalCommandFuntion):
    async def ValidateCommand(*args, **kwargs):
        Context=args[0]
        CmdName=args[1]
        IsAllowed=HonestController.IsThisCommandAllowed(Context.channel,Context.author,CmdName)
        LOG.info("C:{} M:{} V:{}".format(CmdName,Context.author.name,IsAllowed))
        if IsAllowed:
            await OriginalCommandFuntion(*args, **kwargs)
        else:
            await Context.send(BotUtilsLib.GetComamndNotAllowedMsg(CmdName))
    return ValidateCommand


#########################################################
#           SayHello
#########################################################
@decorator_command_validator
async def SayHello(Context,CmdName):
    HelloMsg=BotUtilsLib.GetBotDialogByKey("DLG_HELLO",MentionMember=Context.author)
    await Context.send(HelloMsg)

#########################################################
#           SendRandomQuote
#########################################################

@decorator_command_validator
async def SendRandomQuote(Context,CmdName):
    QuoteToSend= AssetsLib.GetRandomQuote()
    await Context.send("```"+QuoteToSend+"```")

#########################################################
#           SendRandomMotivation
#########################################################

@decorator_command_validator
async def SendRandomMotivation(Context,CmdName):
    QuoteToSend= AssetsLib.GetRandomMotivation()
    await Context.send("```"+QuoteToSend+"```")

#########################################################
#           SendMemberIntro
#########################################################

@decorator_command_validator
async def SendMemberIntro(Context,CmdName,member_mention=None):
    if not "@" in member_mention:
        await Context.send("Please Mention member using @<member_name>")
    else:
        user_id=BotUtilsLib.GetMemberIDFromMention(member_mention)
        if user_id==0:
            await Context.send("Member Not found!")
        else:
            UserIntro=HonestController.GetAllUserData(Context.guild.get_member(int(user_id)))
            await Context.send(UserIntro["Introduction"])

#########################################################
#           DeleteAllChats
#########################################################

@decorator_command_validator
async def DeleteAllChats(Context,CmdName):
    deleted = await Context.channel.purge(limit=100)
    await Context.channel.send('Deleted {} message(s)'.format(len(deleted)))

#########################################################
#           HelpCommand
#########################################################
@decorator_command_validator
async def HelpCommand(Context,CmdName,CmndNameHelp=None):
    IsHelpModePrivate=HonestController.GetHelpMode(Context.channel,Context.author)
    CommandsInfo=ConfigLib.GetCommandInfo()
    """
    ispub priv mode 
    0     0          0
    0     1          1
    1     0          1
    1     1          1
    """
    cmndlist=[]
    for single_cmnd in CommandsInfo:
        if single_cmnd["IsPublic"] or IsHelpModePrivate:
            cmndlist.append(single_cmnd)
    if CmndNameHelp:
        commandfound=False
        for single_cmnd in cmndlist:
            if CmndNameHelp == single_cmnd["Name"]:
                commandfound=True
                await Context.send(single_cmnd["Description"])
        if not commandfound:
            await Context.send("Sorry I didn't find any command named "+CmndNameHelp+"\n> use **ht help** to get list of our commands")    
    else:
        allcommands="> "
        for sin_cmnd in cmndlist:
            allcommands=allcommands+"`"+sin_cmnd["Name"]+"`  "
        await Context.send(BotUtilsLib.GetBotDialogByKey("DLG_HELP")+allcommands)





#TODO:: Add Emojis to bot to give him persanality
        
#TODO::Bot reply will delete itself after some time    


###############################################
#        SendUserStats
###############################################

@decorator_command_validator
async def SendUserStats(Context,CmdName):
    UserInfo=GameEngine.GetAllUserInfo(Context)#TODO::Use ImageLib here
    print(UserInfo)
    user=Context.author
    embed = discord.Embed(
        colour=discord.Colour(0xE5E242),
        title=f"{user.name}'s Stats and Information."
    )
    embed.set_thumbnail(url=user.avatar_url_as(format="png"))
    embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
                                                               f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}\n")
    embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
                                                                      f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
                                                                      f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}\n"
                                                                      f"**Level:** {UserInfo['Level']}\n"
                                                                      f"**XP:** {UserInfo['XP']}\n"
                                                                      f"**XP Next Level:** {UserInfo['NextLevelXP']}\n"
                                                                      )

    await Context.send(embed=embed)


#########################################################
#           SendWaifu
#########################################################

@decorator_command_validator
async def SendWaifu(Context,CmdName):
    global LastSeenWaifu
    #await Context.send("https://yande.re/post/show/"+str(random.randint(10000,50000)))
        
    RandomWaifu=AssetsLib.GetRandomWaifu()
    #print(RandomWaifu)
    LastSentWaifu=RandomWaifu
    HonestController.SetLastSeenWaifu(Context.author,LastSentWaifu)
    RandomWaifuData="> Name:"+RandomWaifu["Name"]
    await Context.send(RandomWaifuData,file=discord.File(RandomWaifu["FilePath"]))



###############################################
#        SendMyWaifu
###############################################

@decorator_command_validator
async def SendMyWaifu(Context,CmdName):
    UserWaifu=HonestController.GetUserWaifu(Context.author)
    if UserWaifu=={} or UserWaifu==None:
        await Context.send(BotUtilsLib.GetBotDialogByKey("DLG_PROPOSE_NOMARRIED"))
        return
        
    UserWaifuData="> Name:"+UserWaifu["Name"]
    await Context.send(UserWaifuData,file=discord.File(UserWaifu["FilePath"]))


###############################################
#        ProposePriviousWaifu
###############################################

@decorator_command_validator
async def ProposePriviousWaifu(Context,CmdName):
    WaifuFound=False
    async for message in Context.channel.history(limit=10):
        LastSentWaifu=HonestController.GetLastSeenWaifu(Context.author)
        if len(message.attachments)==1 and not LastSentWaifu==None:
            WaifuFound=True
            for sin_attach in message.attachments:
                ProposeReply=""
                if random.randint(0,100) < 101:
                    ProposeReply=BotUtilsLib.GetBotDialogByKey("DLG_PROPOSE_YES",MentionMember=Context.author,MentionWaifu=LastSentWaifu)
                    HonestController.SetUserWaifu(Context.author,LastSentWaifu)
                else:
                    ProposeReply=BotUtilsLib.GetBotDialogByKey("DLG_PROPOSE_NO",MentionMember=Context.author,MentionWaifu=LastSentWaifu)
                await Context.send(ProposeReply,file=discord.File(LastSentWaifu["FilePath"]))
            break
    if not WaifuFound:
        await Context.send(BotUtilsLib.GetBotDialogByKey("DLG_PROPOSE_NOFOUND"))

#################################################
#     SendDialogues
#################################################
@decorator_command_validator
async def SendDialogues(Context,CmdName,Dlg):
    BotDialoge=""
    if Dlg == None:
        alldlgs=ConfigLib.GetDlgKeys()
        for sindlg in alldlgs:
            BotDialoge=BotDialoge+sindlg+"\n"
    else:
        BotDialoge=ConfigLib.GetBotDialogue(Dlg.upper())
    if BotDialoge:
        await Context.send(BotDialoge)
    else:
        await Context.send(BotUtilsLib.GetBotDialogByKey("DLG_DLG_NOFOUND",MentionMember=Context.author))

###############################################
#        PerformAttack
###############################################
@decorator_command_validator
async def PerformAttack(Context,CmdName,atk_name):
    await GameEngine.Attack(Context,atk_name)


###########################################
#StartBattle
###########################################

@decorator_command_validator
async def StartBattle(Context,CmdName, BossName,bot):
    await GameEngine.BeginBattle(bot,Context,BossName)
    

###########################################
#EndBattle
###########################################

async def EndBattle(Context,CmdName):
    GameEngine.EndBattle()

###########################################
#OnMemberJoin
###########################################
async def OnMemberJoin(bot,MemberObject):
    welcome_channel=bot.get_channel(ConfigLib.GetChannelIDByAlias("CHNL_WELCOME"))
    welcome_msg=BotUtilsLib.GetBotDialogByKey("DLG_GREET",MentionMember=MemberObject)
    await welcome_channel.send(welcome_msg)



async def SetUnsetRole(Context,role_mention,member_mention,SetRole=True):
    MemberObject=None
    RoleObject=None
    #TODO::use dialog here
    if not "@" in member_mention or not "@" in role_mention:
        await Context.send("Please Mention member using @<member_name> and role using @<role_name>")
    else:
        user_id=BotUtilsLib.GetMemberIDFromMention(member_mention)
        role_id=BotUtilsLib.GetRoleIDFromMention(role_mention)
        if user_id==0:
            await Context.send("Member Not found!")
        else:
            MemberObject=Context.guild.get_member(int(user_id))
            RoleObject = Context.guild.get_role(int(role_id))
    if SetRole:
        await MemberObject.add_roles(RoleObject,reason="Changed by Guild-Master")
    else:
        await MemberObject.remove_roles(RoleObject,reason="Changed by Guild-Master")
    

###########################################
#SetMemberRoleForce
###########################################
@decorator_command_validator
async def SetMemberRoleForce(Context,CmdName,role_mention,member_mention):
    await SetUnsetRole(Context,role_mention,member_mention)    

    
###########################################
#UnSetMemberRoleForce
###########################################
@decorator_command_validator
async def UnSetMemberRoleForce(Context,CmdName,role_mention,member_mention):
    await SetUnsetRole(Context,role_mention,member_mention,False)    
        

###########################################
#RemoveUser
###########################################
@decorator_command_validator
async def RemoveUser(Context,CmdName,member_mention):
    user_id=BotUtilsLib.GetMemberIDFromMention(member_mention)
    MemberObject=Context.guild.get_member(int(user_id))
    if(MemberObject):
        await Context.guild.kick(MemberObject)    
    else:
        await Context.guild.kick("No member found")    


###########################################
#   SendMyAttacks
###########################################
@decorator_command_validator
async def SendMyAttacks(Context,CmdName):
    UserAttacks=GameEngine.GetMemberAttacks(Context.author)
    if UserAttacks != None or UserAttacks != {}:
        await Context.channel.send(UserAttacks)    
    else:
        await Context.channel.send("No Attacks Found")    
    

###########################################
#  SendRandomTopTen 
###########################################
@decorator_command_validator
async def SendRandomTopTen(Context,CmdName,SearchQuery=None):
    if len(SearchQuery)==0:
        YoutubeData=AssetsLib.GetHonestTenVideo()
    elif SearchQuery[0].lower()=="recent":
        YoutubeData=AssetsLib.GetHonestTenVideo(recent=True)
    else:
        YoutubeData=AssetsLib.GetHonestTenVideo(query=" ".join(SearchQuery))
    if len(YoutubeData)==0:
        await Context.send("No videos found...try using single words")
        return
    EmbedList=[]
    for sample in YoutubeData:
        embed = discord.Embed(
        title=sample["title"],
        colour=discord.Colour(0xE5E242),
        url=sample["url"]
        )
        embed.set_thumbnail(url=sample["thumbnails"])
        EmbedList.append(embed)
        await Context.send(embed=embed)
    
    
###########################################
#   HandleCommandErrors
###########################################
async def HandleCommandErrors(Bot,ContextObject,ErrorObject=None):
    ErrorChannel=Bot.get_channel(ConfigLib.GetChannelIDByAlias("CHNL_BOT_ERROR"))
    if isinstance(ErrorObject, commands.MissingRequiredArgument):
        await ContextObject.channel.send(BotUtilsLib.GetBotDialogByKey("DLG_ERR_MISS_ARG",MentionMember=ContextObject.author))
    elif isinstance(ErrorObject, commands.CommandNotFound):
        await ContextObject.channel.send(BotUtilsLib.GetBotDialogByKey("DLG_ERR_CMD_NOTFOUND",MentionMember=ContextObject.author))
    else:
        LOG.critical("Command has failed")
        LOG.error(ErrorObject)
        LOG.error('Exception in command {}:'.format(ContextObject.command))
        traceback.print_exception(type(ErrorObject), ErrorObject, ErrorObject.__traceback__, file=sys.stderr)
        tb_str = "".join(traceback.format_exception(type(ErrorObject), ErrorObject, ErrorObject.__traceback__))
        LOG.error(tb_str)
        await ErrorChannel.send(ErrorObject)
        await ContextObject.channel.send(BotUtilsLib.GetBotDialogByKey("DLG_ERR_UNKNOWN"))


#async def GetReady(bot):
#    print("Bot is getting ready...")
    
    

    
    
