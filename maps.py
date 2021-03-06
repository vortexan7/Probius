from urllib.request import urlopen

async def getMaps():
	return ['alterac-pass','battlefield-of-eternity','blackhearts-bay','braxis-holdout','cursed-hollow','dragon-shire','garden-of-terror',
	'hanamura-temple','haunted-mines','infernal-shrines','sky-temple','tomb-of-the-spider-queen','towers-of-doom','volskaya-foundry','warhead-junction']

async def mapString(battleground):
	output=battleground.replace('-',' ').title().replace('Of','of').replace('The','the')
	return output

async def mapAliases(text):
	maps=await getMaps()
	text=text.lower().replace("'",'').replace(' ','')
	for i in maps:#Acronyms
		if text==''.join(j[0] for j in i.split('-')):
			return i
	for i in maps:
		if text in i.replace('-',''):
			return i
	if text in ['bhb']:
		return 'blackhearts-bay'
	elif text in ['dshire']:
		return 'dragon-shire'

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def coreAbilities(channel,battleground):
	if battleground in ['alterac-pass','haunted-mines','towers-of-doom']:
		await channel.send('No special abilities.')
	page=''.join(i for i in [urlopen('https://nexuscompendium.com/battlegrounds/'+battleground).read().decode('utf-8')]).split('Core Ability - ')[1]
	coreAbilityName=page.split('<')[0]
	page=page.split('The Core ')[1]
	coreDescription=page.split('<')[0]
	page=page.split('Recast after <b>')[1]
	cooldown=page.split(' sec')[0]
	await channel.send('``'+await mapString(battleground)+'`` **Core Ability - '+coreAbilityName+':** Every '+cooldown+' seconds, the Core '+coreDescription)