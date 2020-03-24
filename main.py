import requests
import json
import sys

inp=sys.argv
sen=''
noun=1
if '-s' in inp:
	ind=inp.index('-s')
	sen=inp[ind+1]

if '-nonoun' in inp:
	noun=0

s=requests.session()

skip=open('skip.txt').read()
skip=skip.split("\n")
#print(skip)
tochange=0

skiptext=0
def getsynnony(word):
	global s, skip, skiptext, tochange, noun
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
	tmp=js['data']['definitionData']['definitions'][0]['pos']
	if noun==0 and tmp=='noun':
		return word 
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

if sen=='':
	sen=input('Enter sentence: ')
#percent=int(input('Enter percentage to change: '))
newsen=[]
sen=sen.split(' ')
totallen=len(sen)
#print(totallen)
#tochange=(percent//100)*totallen
print("\n\n\n")
for i in sen:
	res=getsynnony(i)
	newsen.append(res)
for i in newsen:
	print(i, end=' ')
