import os
import datetime
import discord
from discord.ext import commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


verif={}
db2={'id':0} #using dictionary to count ticket number you may use database
botname="Your bot name"

#you can specify prefix for specific channels
def command_prefix(bot, message):
    if "ticket" in str(message.channel.name):
        return ''
    elif "verification" in str(message.channel.name):
        return ''
    elif "support" in str(message.channel.name) and "-" not in str(message.channel.name):
        return ''
    else:
        return '!'

client = commands.Bot(command_prefix = command_prefix)


@client.event
async def on_ready():
    print("Bot running with:")
    print("Username: ", client.user.name)
    print("User ID: ", client.user.id)


#This will send the user a embed message with a ticket icon. When the user who asked to create ticket will react ticket icon then a new channel will be created.
@client.command()
async def support(ctx):
    emoji = '🎫'    

    def check(reaction, user):
        if str(user)==botname:
            return False
        else:
            return  str(reaction) == emoji

    em = discord.Embed(title="Do you need any help?", description= "Click on the :ticket: icon to create a new support channel.", color=0x00a8ff)
    
    message=await ctx.send(embed=em)
    await message.add_reaction(emoji)

    
    
    cc=await client.wait_for('reaction_add', check = check)
    await message.delete()
    await ctx.message.delete()
    await support2(ctx,ctx.message.author)




#NOTE IF YOU DON'T WANT A USER TO PRESS TICKET ICON ON AN EMBED MESSAGE THEN REMOVE COMMENT THIS AND EDIT FUNCTION NAME AS YOU WANT AND COMMENT OUT THE ABOVE FUNCTION.
"""

@client.command()
async def support4(ctx):
    await ctx.message.delete()
    await support2(ctx,ctx.message.author)
"""




#function to create new private channel and send a embed message on that private channel with a lock icon.
@client.command()
async def support2(ctx,user):

    await client.wait_until_ready()
    
    
    data=db2['id']

    ticket_number = int(data)
    ticket_number += 1
    
    db2['id']=ticket_number
    

    
    ticket_channel = await ctx.guild.create_text_channel("support-{}".format(ticket_number))
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "Please be patient our admins will reach you soon.\n Click on :lock: to cose this ticket", color=0x00a8ff)

    vv=await ticket_channel.send(embed=em)
    await vv.add_reaction('🔒')
    member='{}'.format(user)
    created_em = discord.Embed(title="TMC Member Support Tickets", description="{} !Your ticket has been created at {}".format(member,ticket_channel.mention), color=0x00a8ff)
    
    test=await ctx.send(embed=created_em)

    
    emoji2='🔒'

    def check2(reaction, user):
        return (user == ctx.author or user=="ArkoTadashi#5967" or user=="Srijon#4378")and str(reaction) == emoji2
    
    await client.wait_for('reaction_add', check = check2)
    await test.delete()
    await removechannel(ctx,vv.channel.id)
    

#this function is for deleting channel
@client.command()
async def removechannel(ctx, channel_id: int):
    channel = client.get_channel(channel_id)
    try:
        await channel.delete()
    except:
        pass

    
#things to do on a private channel
@client.event
async def on_message(message):
    channel_name=message.channel.name
    msg=message.content
    if message.author.bot:
        return
    else:
        if msg=="hi":
            await message.channel.send("hello")
    
        else:        
            await client.process_commands(message)


client.run("Your token here")

