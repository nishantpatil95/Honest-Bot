import discord
import GameEngine
import HonestController
import ConfigLib
import traceback
import LoggerLib
LOG=LoggerLib.getlogger()

async def processmessage(selfbot,message):
    
    if message.author.bot:
        return

    await selfbot.process_commands(message)

    if discord.ChannelType.private==message.channel.type:
        return

    
    if message.guild.id!=ConfigLib.GetCurrentGuild():
        LOG.critical("Bot is used on Another Server")
        return 
    
    try:
        await GameEngine.ManageLevel(selfbot,message)
    except Exception as e: 
        print(e)
        LOG.critical("some error in process message")
        tb_str="".join(traceback.format_exception(type(e),e,e.__traceback__))
        LOG.error(tb_str)
        print(tb_str)

    
            
