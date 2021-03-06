from lfg import roleAliases

async def trim(text):
	toRemove=[' ','#','<@&557521663894224912>','*','\n','league']
	text=text.lower()
	for i in toRemove:
		text=text.replace(i,'')
	return text

async def sort(roles,member,olympian,client):
	guild=client.get_guild(535256944106012694)#Wind Striders
	channel=guild.get_channel(557366982471581718)#general
	if 557521663894224912 not in [role.id for role in olympian.roles]:
		#await channel.send('You need to be a mod to sort users!')
		return
	if len(roles)!=3:
		await channel.send('Need ping and 3 roles')
		return
	#Colours between bestBot and IM
	bestBot=guild.get_role(635187043676323842)
	IM=guild.get_role(557550150109888513)
	#Ranks and regions between lopez and core member
	lopez=guild.get_role(571525173698756608)
	coreMember=guild.get_role(571321937821696001)

	unsorted=guild.get_role(560435022427848705)

	if unsorted not in member.roles:
		#await channel.send('**'+member.name+'** is not unsorted')
		return
	roles=list(set(roles))
	if len(roles)!=3:
		await channel.send('Need 3 *different* roles')
		return
	rolesToAdd=[]
	for role in roles:
		try:
			role=roleAliases(role)
			for i in sorted(guild.roles):
				if (i<bestBot and i>IM) or (i<lopez and i>coreMember):
					if await trim(i.name)==await trim(role):
						rolesToAdd.append(i)
					elif await trim(i.name)==await trim(''.join([i for i in role if not i.isdigit()])):#Rank numbers
						rolesToAdd.append(i)
					elif await trim(i.name)==await trim(role+'1'):#Add colour #1
						rolesToAdd.append(i)
					else:
						continue
					raise Exception('Role done!')
		except:
			pass
	if len(rolesToAdd)!=3:
		await channel.send('At least one role was wrong or inaccessible. Valid roles: '+', '.join([i.name for i in rolesToAdd]))
		return
	memberRole=guild.get_role(557522023190888468)
	rolesToAdd.append(memberRole)
	await member.add_roles(*rolesToAdd)
	await member.remove_roles(unsorted)
	await channel.send('**'+member.name+'** has been sorted!')

async def sortFromMessage(text,message,client):
	unsortedMember,text=(await trim(text)).split('>')
	unsortedMember+='>'
	guild=client.get_guild(535256944106012694)#Wind Striders
	unsortedMember=guild.get_member(int(unsortedMember.replace(' ','')[2:-1].replace('!','')))

	roles=text.split(',')
	if roles[0]=='':
		roles.pop(0)
	await sort(roles,unsortedMember,message.author,client)

async def sortFromReaction(message,reacterID,client):
	roles=await trim(message.content)
	if '/' in roles:
		roles=roles.split('/')
	else:
		roles=roles.split(',')
	unsortedMember=message.author
	guild=client.get_guild(535256944106012694)
	olympian=guild.get_member(int(reacterID))
	await sort(roles,unsortedMember,olympian,client)