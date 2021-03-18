import discord
import os
import re
import herodb
import validators
import random
import sqlite3
from herodb import stats, units
from guide import helpcontent, formula, commandlist
from stayingalive import stayingalive

client = discord.Client()

conn = sqlite3.connect("examples.db")
db = conn.cursor()

validsubstats = ['atk', 'fatk', 'hp', 'fhp', 'def', 'fdef', 'spd', 'cc', 'cd', 'cdam', 'eff', 'er', 'res']


@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(msg):
  if msg.author == client.user:
    return
  
  if msg.content.startswith('$help'):
    await msg.channel.send(helpcontent)
  
  if msg.content.startswith('$commands'):
    await msg.channel.send(commandlist)
  
  if msg.content.startswith('$formula'):
    await msg.channel.send(formula)

  if msg.content.startswith('$hs'):
    await msg.channel.send('pls input hero name')

    def check(x):
      return x.content.lower() in stats.keys() and x.channel == msg.channel

    msg = await client.wait_for('message', check=check)
    await msg.channel.send(stats[msg.content.lower()])

  if msg.content.startswith('$submit'):
    await msg.channel.send('pls input img link, followed by unit name')

    def check(x):
      return x.channel == msg.channel

    msg = await client.wait_for('message', check=check)

    link = msg.content.split()[0]
    name = msg.content.split(link, 1)[1].lstrip()

    if validators.url(link):
      check_exist = db.execute("SELECT * FROM images WHERE link = ?", (link,))
      if len(check_exist.fetchall()) != 0:
        await msg.channel.send('link already exists in database')
      else:
        db.execute("INSERT INTO images (name, link) VALUES(?, ?)", (name.lower(), link)) 
        conn.commit()
        await msg.channel.send('unit recorded')
    else:
      await msg.channel.send('invalid name/link')
  
  if msg.content.startswith('$search'):
    await msg.channel.send('pls input unit name')

    def check(x):
      return x.channel == msg.channel

    msg = await client.wait_for('message', check=check)
    
    name = msg.content.lower()

    db.execute("SELECT name, link FROM images WHERE name = ?", (name,))
    results = db.fetchall()
    
    img = random.choice(results)[1]
    await msg.channel.send(img)

  if msg.content.startswith('$delete'):
    await msg.channel.send('pls input link to delete')

    def check(x):
      return validators.url(x.content) and x.channel == msg.channel

    msg = await client.wait_for('message', check=check)
    db.execute("DELETE FROM images WHERE link = ?", (msg.content,))
    conn.commit()
    await msg.channel.send('link removed')


  if msg.content.startswith('$herogs'):
    await msg.channel.send('pls input gear stats followed by the unit name')

    def check(x):
      return re.search(r'([a-z]+\s\d+\s*)+[\sa-z]+', x.content) and x.channel == msg.channel

    msg = await client.wait_for('message', check=check)
    p = re.compile('([a-z]+\s\d+\s*)+')
    m = p.match(msg.content)
    l = m.group().lower()
    slist = l.split()
    name = msg.content.split(l, 1)[1]
    checkvalid = []

    for i in range(0, len(slist), 2):
      checkvalid.append(slist[i].lower())
    
    sdict = {}

    if name.lower() in stats.keys() and all(sub in validsubstats for sub in checkvalid):
      for i in range(0, len(slist), 2):
        if slist[i].lower() == 'spd':
          sdict[slist[i]] = 2*float(slist[i+1])
        
        elif slist[i].lower() == 'cc':
          sdict[slist[i]] = 1.6*float(slist[i+1])
      
        elif slist[i].lower() == 'cd' or slist[i].lower == 'cdam':
          sdict[slist[i]] = float(slist[i+1])+float(slist[i+1])//7
        
        elif slist[i].lower() == 'fatk':
          percent = 100*(float(slist[i+1])/float(stats[name]['atk']))
          sdict[slist[i]] = percent

        elif slist[i].lower() == 'fhp':
          percent = 100*(float(slist[i+1])/float(stats[name]['hp']))
          sdict[slist[i]] = percent

        elif slist[i].lower() == 'fdef':
          percent = 100*(float(slist[i+1])/float(stats[name]['def']))
          sdict[slist[i]] = percent
        
        else:
          sdict[slist[i]] = slist[i+1]
        
      score = sum(map(float, sdict.values()))
      await msg.channel.send('{:.2f}'.format(score))

    else:
      await msg.channel.send('Invalid substat entered, pls type properly.')

  if msg.content.startswith('$gs'):
    await msg.channel.send('pls input gear stats')
    
    def check(x):
      return re.search(r'([a-z]+\s\d+\s*)+', x.content) and x.channel == msg.channel
    
    msg = await client.wait_for('message', check = check)
    slist = msg.content.split()
    checkvalid = []

    for i in range(0, len(slist), 2):
      checkvalid.append(slist[i].lower())


    sdict = {}

    if all(sub in validsubstats for sub in checkvalid):
      for i in range(0, len(slist), 2):
        if slist[i].lower() == 'spd':
          sdict[slist[i]] = 2*float(slist[i+1])
        
        elif slist[i].lower() == 'cc':
          sdict[slist[i]] = 1.6*float(slist[i+1])
      
        elif slist[i].lower() == 'cd' or slist[i].lower == 'cdam':
          sdict[slist[i]] = float(slist[i+1])+float(slist[i+1])//7
        
        else:
          sdict[slist[i]] = slist[i+1]
        
      score = sum(map(float, sdict.values()))
      await msg.channel.send(score)
    
    else:
      await msg.channel.send('Invalid substat entered, pls type properly.')


stayingalive()
client.run(os.getenv('token'))




