import discord 
from discord.ext import commands, tasks
import json
from pokemon import *

client = commands.Bot(command_prefix='')
token = "Nzk3NTQ5ODM2MzUzNzk4MTY1.X_oGKg.399NEvHfccdFcIYzJP8sXCXLNiY"



@client.event
async def on_ready():
    print("Bot is online")

@client.event
async def on_member_join(member):
    # Open Json file 
    with open("leveling.json", 'r') as f:
        users = json.load(f)
    
    await update_user(users, member)
    
    with open("leveling.json", 'w') as f:
        json.dump(users, f)

@client.event 
async def on_message(message):
    # Open Json file 
    with open("leveling.json", 'r') as f:
        users = json.load(f)
    
    await update_user(users, message.author)
    await add_xp(users, message.author, 5)
    thing =  leveling_system(users, message.author, message.channel)
    
    if message.content.lower() == "pokemon":
        # Send a embed
        name = await client.fetch_user(message.author.id) 
        namep = users[str(message.author.id)]['pokemon']['name']
        hpp = users[str(message.author.id)]['pokemon']['hp']
        attackp = users[str(message.author.id)]['pokemon']['attack']
        
        if namep == "squirtle":
            realNamep = "https://imgur.com/vtQ7JjB"
        if namep == "charmander":
            realNamep = "https://imgur.com/aGB19ZL"
        if realNamep == "froakie":
            namep = "https://imgur.com/k28khqu"
        
        
        em = discord.Embed(title=f"{name}'s Pokemon", description="NOne")
        em.add_field(name="hp", value=hpp)
        em.add_field(name="attack", value=attackp)
        await message.channel.send(embed=em)
        await message.channel.send(f"NAME: {realNamep}")
        
    
    if thing[0] == True:
        await message.channel.send(f"Congradulations {message.author} you leveled up to {thing[1]}")
    
    with open("leveling.json", 'w') as f:
        json.dump(users, f)
    

async def update_user(users, user):
    if not str(user.id) in users.keys():
        # Add the users 
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1
        users[str(user.id)]['pokemon'] = {}
    else:
        return 

async def add_xp(users, user, amt):
    users[str(user.id)]['experience'] += amt


    
    
    
def leveling_system(users, user, channel):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience**(1/4))
    
    if lvl_end > lvl_start:
        # He leveled up
        users[str(user.id)]['level'] = lvl_end
        # Check what level the user is for prizes 
        print(lvl_end)
        if lvl_end == 4:
            # Give a squirttle 
            level_four(users, user)
        if lvl_end == 7:
            # Give a Froakie 
            level_seven(users, user)
        if lvl_end == 10:
            # Give a charmander
            level_ten(users, user) 
        return [True, lvl_end]
            
        
            
            
    return [False, None]



client.run(token)