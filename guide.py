helpcontent = '''Hello. Thanks for using my GS bot! GS(Gear Score) is a way of rating the quality of a piece of gear, with high quality gear falling in the 70+ range and lower-end gear falling in the 40-50 range.

Commands needed to use the bot can be accessed with $commands'''

formula = '''**Substats can be converted to GS values in the following way:**

Attack, HP, Def, Eff, Eff Res can all be converted to GS values in a 1:1 ratio

Spd has a x2 multiplier, Crit Chance has a x1.5 multipler and Crit Damage has a x1 multiplier like other stats but has a +1 value for every 7% CD 
'''

commandlist = '''
$help: gets help
$commands: gets list of commands 
$formula: returns method to which substats are converted to gs values
$hs: returns base stats of specified hero
$gs: prompts the bot to ask for your stats, to which you reply in the format: <x> <y> <x> <y> <x> <y> <x> <y>, where x is the abbreviated name of the substat(i.e. atk, hp, def, spd, cc, cd, eff, er) with a space between each word/value
$herogs: allows user to calculate gs of gear with flat stats. command prompts bot to ask for stats followed by the name of the unit. stat input follows the format of the $gs command, with flat stats taking the name of fatk, fhp, fdef for atk, hp and def respectively.
$search: prompts the bot to give build references for given unit
'''


