
import ConfigLib


#  BotUtilsLib 

#TODO::Use Discord Mention

def MentionUser(Msg,MemberObject):
    return Msg.replace("MENTION_MEMBER","<@"+str(MemberObject.id)+">")
    

def MentionUserWaifu(Msg,WaifuObject):
    return Msg.replace("MENTION_WAIFU",WaifuObject["Name"])
    
    
def MentionUserLevel(Msg,Level):
    return Msg.replace("MENTION_LEVEL",str(Level))

def MentionChannel(Msg):
    ChannelsAlias=ConfigLib.GetChannelIDs()
    for key in ChannelsAlias.keys():
        if key in Msg:
            Msg=Msg.replace(key,"<#"+str(ConfigLib.GetChannelIDByAlias(key))+">")
    return Msg



def GetTrueID(mention):
    return mention.replace("@","").replace(">","").replace("<","").replace("!","").replace("#","").replace("&","")

def GetMemberIDFromMention(member_mention):
    return GetTrueID(member_mention)

def GetRoleIDFromMention(role_mention):
    return GetTrueID(role_mention)

def GetBotDialogByKey(dlg_key,MentionMember=None,MentionWaifu=None,MentionLevel=None):
    Dialog=ConfigLib.GetBotDialogue(dlg_key);
    if MentionMember:
        Dialog=MentionUser(Dialog,MentionMember)
    if MentionWaifu:
        Dialog=MentionUserWaifu(Dialog,MentionWaifu)
    if MentionLevel:
        Dialog=MentionUserLevel(Dialog,MentionLevel)
    Dialog=MentionChannel(Dialog)
    return Dialog

def to_integer(dt_time):
    milliseconds = int(round(dt_time.timestamp() * 1000))
    return milliseconds

def GetComamndNotAllowedMsg(CmdName):
    return 'Command Not Allowed! use "ht help '+CmdName+'" to get more info'
