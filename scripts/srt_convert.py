# encoding=utf-8

def convert(filein,fileout):
	f=open(filein)
	fo=open(fileout,'w')
	next=False
	for line in f:
		if next==True:
			fo.write(line)
			next=False
		if len(line)>3 and line[2]==':' and line[0]=='0':
			next=True
	fo.close()
	f.close()

if __name__ == '__main__':
	convert(u'第一周第五节02.srt',u'1.txt')