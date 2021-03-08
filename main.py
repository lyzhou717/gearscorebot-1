import discord
import httplib2
import json
import mimetypes
import os
import re
import herodb
import urllib
from herodb import stats, units
from guide import helpcontent, formula, commandlist
from img import uploadItem
from stayingalive import stayingalive

client = discord.Client()

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




