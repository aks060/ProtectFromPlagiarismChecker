import requests
import json

s=requests.session()

skip=open('skip.txt').read()
skip=skip.split("\n")
#print(skip)

skiptext=0
def getsynnony(word):
	global s, skip, skiptext
	if '*' in word:
		if skiptext==0:
			skiptext=1
		else:
			skiptext=0

		if '*'==word[0]:
			return word[1:]
		elif '*'==word[-1]:
			return word[:-1]
		else:
			return word
	if word.lower() in (name.lower() for name in skip):
		return word
	out=s.get('https://tuna.thesaurus.com/pageData/'+word)
	js=json.loads(out.content.decode())
	if js['data']==None:
		return word
	#js['data']['definitionData']['definitions']['0']['synonyms']))
	js=js['data']['definitionData']['definitions'][0]['synonyms']
	maxsim=49
	finalword=word
	type(js)
	for i in js:
		if i['isVulgar']==None and i['isInformal']=='0':
			if int(i['similarity'])>maxsim:
				finalword=i['term']
				maxsim=int(i['similarity'])
	return finalword

sen=input('Enter sentence: ')
newsen=[]
sen=sen.split(' ')
print("\n\n\n")
for i in sen:
	res=getsynnony(i)
	newsen.append(res)
for i in newsen:
	print(i, end=' ')