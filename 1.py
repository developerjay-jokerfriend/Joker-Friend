file=open('abc.txt','r')
lines=0
characters=0
words=0
for line in file:
	lines+=1
	stipped=line.rstrip()
	wordline=stipped.split()
	print(wordline)
	words+=len(wordline)
	for charac in wordline:
		characters+=len(charac)
print ('Lines:',lines)
print ('Words:',words)
print ('Characters:',characters)

