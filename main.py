import discord 
from discord.ext import commands, tasks
import json

client = commands.Bot(command_prefix='')
token = "Nzk3NTQ5ODM2MzUzNzk4MTY1.X_oGKg.c9pDO7X-5i-5HRhkKKOofVsvMQU"



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
    else:
        return 

async def add_xp(users, user, amt):
    users[str(user.id)]['experience'] += amt
    
def leveling_system(users, user, channel):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience**(1/4))
    print(lvl_end, experience)
    
    if lvl_end > lvl_start:
        # He leveled up
        users[str(user.id)]['level'] = lvl_end
        return [True, lvl_end] 
    return [False, None]



client.run(token)