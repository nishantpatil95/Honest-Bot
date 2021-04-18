from discord.ext import tasks,commands
import discord
import HonestCommands
import asyncio
import MessageProcessor
import random
import ConfigLib

import LoggerLib
LOG=LoggerLib.getlogger()


class MyBot(commands.Bot):
    def __init__(self,Token,BotPrefix):
        my_intents = discord.Intents.default()
        my_intents.members = True
        commands.Bot.__init__(self, command_prefix=BotPrefix,intents=my_intents)
        self._Token=Token
        self.remove_command('help')
        
##################################################################### Public Commands #####################################################################

        @self.command(name='hi')
        async def cmd_hi(ctx):
            await HonestCommands.SayHello(ctx,'hi')
        
        @self.command(name='quote')
        async def cmd_quote(ctx):
            await HonestCommands.SendRandomQuote(ctx,'quote')

        @self.command(name='motivate')
        async def cmd_quote(ctx):
            await HonestCommands.SendRandomMotivation(ctx,'motivate')

        @self.command(name='whois')
        async def cmd_whois(ctx,member_name):
            await HonestCommands.SendMemberIntro(ctx,'whois',member_name)
        
        @self.command(name='waifu')
        async def cmd_waifu(ctx):
            await HonestCommands.SendWaifu(ctx,'waifu')
            
        @self.command(name='mywaifu')
        async def cmd_mywaifu(ctx):
            await HonestCommands.SendMyWaifu(ctx,'mywaifu')
            
        @self.command(name='propose')
        async def cmd_propose(ctx):
            await HonestCommands.ProposePriviousWaifu(ctx,'propose')
            
        @self.command(name='level')
        async def cmd_level(ctx):
            await HonestCommands.SendUserStats(ctx,'level')
        
        @self.command(name='atk')
        async def cmd_atk(ctx,atk_name):
            await HonestCommands.PerformAttack(ctx,'atk',atk_name)
            
        @self.command(name='myatk')
        async def cmd_myatk(ctx):
            await HonestCommands.SendMyAttacks(ctx,'myatk')
        
        @self.command(name='honest')
        async def cmd_honestten(ctx,*searchQuery):
            await HonestCommands.SendRandomTopTen(ctx,'honest',searchQuery)
        
        @self.command(name='help')
        async def cmd_help(ctx,CmndNameHelp=None):
            await HonestCommands.HelpCommand(ctx,'help',CmndNameHelp)

#################################### Private Commands ######################################


        @self.command(name='startbattle')
        async def cmd_startbattle(ctx,boss_name):
            await HonestCommands.StartBattle(ctx,"startbattle",boss_name,self)
        
        @self.command(name='endbattle')
        async def cmd_endbattle(ctx):
            await HonestCommands.EndBattle(ctx,"endbattle")
            
        @self.command(name='kick')
        async def cmd_kick(ctx,member_mention):
            await HonestCommands.RemoveUser(ctx,'kick',member_mention)
        
        @self.command(name='clearchats')
        async def cmd_clearchats(ctx):
            await HonestCommands.DeleteAllChats(ctx,'clearchats')
        
        @self.command(name='dlg')
        async def cmd_kick(ctx,dialogue_name=None):
            await HonestCommands.SendDialogues(ctx,"dlg",dialogue_name)
            
        @self.command(name='setrole')
        async def cmd_set_role(ctx,role_name,member_mention):
            await HonestCommands.SetMemberRoleForce(ctx,'setrole',role_name,member_mention)
        
        @self.command(name='unsetrole')
        async def cmd_un_set_role(ctx,role_name,member_mention):
            await HonestCommands.UnSetMemberRoleForce(ctx,'unsetrole',role_name,member_mention)
        
        #TODO:: Use tasks to clean up chats


#################################### Loops  ######################################        
        
        @tasks.loop(minutes=0.01)
        async def test():
            #print("c")
            for guild in self.guilds:
                for rl in guild.roles:
                    if(rl.name=="Guild-Master"):
                        await rl.edit(reason = None, colour = discord.Colour(random.randint(0, 16777216)))

            

#################################### Events  ######################################
        
        #Events
        @self.event
        async def on_ready():
            text_channel_list={}
            #await HonestCommands.GetReady(self)
            #test.start()
            """for guild in self.guilds:
                for channel in guild.text_channels:
                    text_channel_list[channel.id]=channel.name
            for item in text_channel_list.keys():
                print(item,text_channel_list[item])"""
            
            GuildID=ConfigLib.GetCurrentGuild()
            GuildObjectFromBot=self.get_guild(GuildID)
 
            LOG.info("Guild::{}".format(GuildObjectFromBot.name))

            AllGuildChannels=ConfigLib.GetChannelIDs()

            for SingleChannelKey in AllGuildChannels.keys():
                chnl=self.get_channel(AllGuildChannels[SingleChannelKey])
                LOG.info("{} -> {}".format(SingleChannelKey,chnl.name))
            
            AllGuildRoles=ConfigLib.GetRoleIDs()

            for SingleRoleKey in AllGuildRoles.keys():
                rl=discord.utils.get(GuildObjectFromBot.roles,id=AllGuildRoles[SingleRoleKey])
                LOG.info("{} -> {}".format(SingleRoleKey,rl.name))

            LOG.info('Ready!')
            print('Bot is online!')

        @self.event
        async def on_message(message):
            if message.author.id == self.user.id:
                return;
            #################WRITE BELOW##############
            await MessageProcessor.processmessage(self,message)


        @self.event    
        async def on_member_join(member):
            await HonestCommands.OnMemberJoin(self,member)
            
        @self.event    
        async def on_command_error(ctx,error):
            await HonestCommands.HandleCommandErrors(self,ctx,error)
            
        @self.event
        async def on_member_update(MemberBefore,MemberAfter):
            
            LOG.info("MemberRolesChanged {}".format(MemberBefore.name))
            for singlerole in MemberBefore.roles:
                LOG.info("RB:{}".format(singlerole.name))
            
            for singlerole in MemberAfter.roles:
                LOG.info("RA:{}".format(singlerole.name))
    def RunBot(self):
        self.run(self._Token)
        
