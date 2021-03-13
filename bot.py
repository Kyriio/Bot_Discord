#Author Kyriio
import discord
import random
import asyncio
from datetime import datetime
from discord.ext import commands
from discord.utils import get



intents = discord.Intents(messages=True,guilds=True,reactions=True,members=True,presences=True)
#prefix of the bot
client = commands.Bot(command_prefix = '=',intents=intents)
#disable fake_help_command
client.remove_command('help')

#connection
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="Le serveur"))
    print('connected')

snipe_message_content=None
snipe_message_author=None
snipe_message_channel=None
snipe_message_discriminator=None
snipe_message_avatar = None
snipe_message_date= None

@client.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author
    global snipe_message_channel
    global snipe_message_discriminator
    global snipe_message_avatar
    global snipe_message_date

    snipe_message_content= message.content
    snipe_message_author= message.author.name
    snipe_message_discriminator = message.author.discriminator
    snipe_message_channel = message.channel
    snipe_message_avatar = message.author.avatar_url
    snipe_message_date = message.created_at

    await asyncio.sleep(30)
    snipe_message_content=None
    snipe_message_author=None
    snipe_message_channel=None
    snipe_message_discriminator=None
    snipe_message_avatar=None
    snipe_message_date=None


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server uwu')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server. :(')

#Ping / first test function
@client.command()
async def ping(ctx):
    embed=discord.Embed(description=f'<a:ping_pong:796453534639587377> Pong! {round(client.latency *1000)}ms', color=0xb0c4de)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def say(ctx,*,msg):
    await ctx.message.delete()
    await ctx.send(msg)

#Clear command
@client.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#Avatar commands
@client.command()
async def av(ctx, member : discord.Member = None):
    if member is None:
        embed = discord.Embed(title=f"{ctx.author}'s Avatar",color=0xb0c4de)
        embed.set_image(url=ctx.author.avatar_url)
    else:
        embed = discord.Embed(title=f"{member}'s Avatar",color=0xb0c4de)
        embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)

#snipe commands ( je dois résoudre le fait que ça ne sauvegarde pas sur plusieurs channel)
@client.command()
async def snipe(ctx):
    global snipe_message_author
    global snipe_message_content
    global snipe_message_channel
    global snipe_message_discriminator
    global snipe_message_avatar
    global snipe_message_date

    currentChan = ctx.channel
    save = snipe_message_channel

    if snipe_message_content==None:
        embed=discord.Embed(description="***Il n'y a rien à sniper.***",color=0xb0c4de)
        await ctx.channel.send(embed=embed)
    else:
        if ((currentChan == snipe_message_channel) or (currentChan == save)):
            embed=discord.Embed(description=snipe_message_content, color=0xb0c4de, timestamp=datetime.utcnow())
            embed.set_author(name=f'{snipe_message_author}#{snipe_message_discriminator}',icon_url=snipe_message_avatar)
            await ctx.channel.send(embed=embed)
            snipe_message_author=None
            snipe_message_content=None
            snipe_message_channel=None
            snipe_message_discriminator=None
            snipe_message_avatar=None
            return
        else:
            save=snipe_message_channel
            await ctx.channel.send(save)
            embed=discord.Embed(description="***Il n'y a rien à sniper.***",color=0xb0c4de)
            await ctx.channel.send(embed=embed)

#Kick command
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx,member : discord.Member,*, reason=None):
    master = get(member.roles, id=769692298517938196)
    helper = get(member.roles, id=769692863960711180)
    if master != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    elif helper != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    else:
        user = client.get_user(member.id)
        try:
            if reason==None:
                embed=discord.Embed(description=f'***{member} a été kick.***',color=0xb0c4de)
                embed2=discord.Embed(description=f'Server : Poltrone \nServer Id : 769688909864239116\nKicked : {member}\nKicked Id : {member.id}',color=0xb0c4de)
                embed2.set_author(name=f'Kicked by : {ctx.author}',icon_url=f'{ctx.message.author.avatar_url}')
                embed2.set_thumbnail(url = member.avatar_url)
                await user.send(embed=embed2)
                await member.kick(reason=reason)
            else:
                embed=discord.Embed(description=f'***{member} a été kick.***',color=0xb0c4de)
                embed2=discord.Embed(description=f'Server : Poltrone\nServer Id : 769688909864239116\nKicked : {member}\nKicked Id : {member.id}\nReason : {reason}',color=0xb0c4de)
                embed2.set_author(name=f'Kicked by : {ctx.author}',icon_url=f'{ctx.message.author.avatar_url}')
                embed2.set_thumbnail(url= member.avatar_url)
                await user.send(embed=embed2)
                await member.kick(reason=reason)
        except:
            await member.kick(reason=reason)
    await ctx.send(embed=embed)



#ban command
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx,member : discord.Member,*,reason=None):
    master = get(member.roles, id=769692298517938196)
    helper = get(member.roles, id=769692863960711180)
    if master != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    elif helper != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    else:
        user = client.get_user(member.id)
        try:
            if reason == None:
                embed=discord.Embed(description=f'***{member} est banni.***',color=0xb0c4de)
                embed2=discord.Embed(description=f'Server : Poltrone\nServer Id : 769688909864239116\nBanned : {member}\nBanned Id : {member.id}',color=0xb0c4de)
                embed2.set_author(name=f'Banned by : {ctx.author}',icon_url=f'{ctx.message.author.avatar_url}')
                embed2.set_thumbnail(url= member.avatar_url)
            else:
                embed=discord.Embed(description=f'***{member} est banni.***',color=0xb0c4de)
                embed2=discord.Embed(description=f'Server : Poltrone\nServer Id : 769688909864239116\nBanned : {member}\nBanned Id : {member.id}\nReason : {reason}',color=0xb0c4de)
                embed2.set_author(name=f'Banned by : {ctx.author}',icon_url=f'{ctx.message.author.avatar_url}')
                embed2.set_thumbnail(url= member.avatar_url)
        except:
            pass
        await user.send(embed=embed2)
        await member.ban(reason=reason,delete_message_days=7)
    await ctx.send(embed=embed)


#unban command
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx,*,id):
    try:
        memberid = discord.Object(id=id)
        await ctx.guild.unban(memberid)
        embed=discord.Embed(description=f'***<@'+id+'> est débanni.***',color=0xb0c4de)
    except:
        pass
    await ctx.send(embed=embed)

#mute command
@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member =None,amount=100000000000000000,real='m',*, reason= None):
    master = get(member.roles, id=769692298517938196)
    helper = get(member.roles, id=769692863960711180)
    if master != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    elif helper != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    else:
        user = client.get_user(member.id)
        mutedRole = ctx.guild.get_role(769894732020056094)
        if (real =='m'):
            time=amount*60
        elif(real =='h'):
            time=amount*3600
        else:
            time=amount*86400
        embed=discord.Embed(description=f'***{member} est mute.***',color=0xb0c4de)
        try:
            if reason==None:
                embed2=discord.Embed(description=f'Server : Poltrone\nServer Id : 769688909864239116\nMuted : {member}\nMuted Id : {member.id}',color=0xb0c4de)
                embed2.set_author(name=f'Muted by : {ctx.author}',icon_url=f'{ctx.message.author.avatar_url}')
                embed2.set_thumbnail(url= member.avatar_url)
            else:
                embed2=discord.Embed(description=f'Server : Poltrone\nServer Id : 769688909864239116\nMuted : {member}\nMuted Id : {member.id}\nReason : {reason}',color=0xb0c4de)
                embed2.set_author(name=f'Muted by : {ctx.author}',icon_url=f'{ctx.message.author.avatar_url}')
                embed2.set_thumbnail(url= member.avatar_url)
        except:
            pass
        await ctx.send(embed=embed)
        await user.send(embed=embed2)
        await member.add_roles(mutedRole, reason=reason)
        await asyncio.sleep(time)
        await member.remove_roles(mutedRole)




#unmute command
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member= None):
    master = get(member.roles, id=769692298517938196)
    helper = get(member.roles, id=769692863960711180)
    if master != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    elif helper != None:
        embed=discord.Embed(description="***C'est un administrateur, je ne peux pas faire ça.***",color=0xdb2903)
    else:
        role = ctx.guild.get_role(769894732020056094)
        if role in member.roles:
            await member.remove_roles(role)
            embed=discord.Embed(description=f'***{member} est mué.***',color=0xb0c4de)
        else:
            embed=discord.Embed(description=f"***{member} n 'est pas mué.***",color=0xb0c4de)
    await ctx.send(embed=embed)

#custom help command
@client.command(pass_context=True)
async def help(ctx):

    embed=discord.Embed(title='Liste des commandes',color=0xb0c4de)
    embed.add_field(name=' ⁢', value='-Help:  **(Montre les commandes.)**',inline=False)
    embed.add_field(name=' ⁢', value="-Av: **(Montre l'avatar.)**",inline=False)
    embed.add_field(name=' ⁢',value ='-Away:  **(Met en mode afk.)**')
    embed.add_field(name=' ⁢', value='-Snipe: **(Snipe le dernier message.)**',inline=False)
    embed.add_field(name=' ⁢', value='-Whois:  **(Montre les informations du membre.)**',inline=False)
    embed.add_field(name=' ⁢⁢⁢⁢',value='**Commandes modération**',inline=False)
    embed.add_field(name=' ⁢',value='-Ban    **<user> <reason>** ⁢⁢⁢⁢⁢')
    embed.add_field(name=' ⁢',value='-Unban   **<user id>** ⁢⁢⁢⁢⁢',inline=False)
    embed.add_field(name=' ⁢',value='-Kick   **<user> <reason>** ⁢⁢⁢⁢⁢',inline=False)
    embed.add_field(name=' ⁢',value='-Mute   **<user> <duration> <reason>**⁢⁢⁢⁢⁢',inline=False)
    embed.add_field(name=' ⁢',value='-Unmute   **<user>**⁢⁢⁢⁢⁢',inline=False)
    embed.add_field(name=' ⁢',value='-Purge   **<amount>**⁢⁢⁢⁢⁢',inline=False)
    embed.set_footer(text='[Prefix: = ]')
    await ctx.send(embed=embed)

@client.command()
async def whois(ctx,member : discord.Member=None):
    if not member:
        member = ctx.message.author

    roles= [role for role in member.roles]
    embed=discord.Embed(color=0xb0c4de,timestamp=ctx.message.created_at,title=f'User Info - {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}')
    embed.add_field(name='ID:', value=member.id,inline=False)
    embed.add_field(name='Display Name:', value=member.display_name,inline=False)
    embed.add_field(name='Registered:', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
    embed.add_field(name='Joined:', value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
    embed.add_field(name='Roles:',value=''.join([role.mention for role in roles]),inline=False)
    await ctx.send(embed=embed)

@client.command()
async def away(ctx):

    afk = discord.utils.get(ctx.author.roles,id=808022899113066517)
    afkrole = ctx.guild.get_role(808022899113066517)

    if afk in ctx.author.roles:
        embed=discord.Embed(colox=0xb0c4de,description=f'***{ctx.author} est de retour.***')
        await ctx.author.remove_roles(afkrole)
    else:
        await ctx.author.add_roles(afkrole)
        embed=discord.Embed(colox=0xb0c4de,description=f'***{ctx.author} est afk.***')
    await ctx.send(embed=embed)

#async def stop(ctx,message,amount=5):
#    for i in range(amount):
#        await ctx.send(message)






client.run("votre_toekn")
