import time

def strtime(t):
	s = time.strftime("%H:%M:%S", time.gmtime(float(t)))
	s = s+','
	s = s+t.split('.')[1]
	return s

def gen(linefile,timefile,fileout):
	fl=open(linefile)
	ft=open(timefile)
	fo=open(fileout,'w')
	i=1
	for line in ft:
		fo.write(str(i)+'\n')
		i+=1
		tok=line.strip().split(' ')
		fo.write(strtime(tok[0]))
		fo.write(' --> ')
		fo.write(strtime(tok[1]))
		fo.write('\n')
		fo.write(fl.readline())
		fo.write('\n')
	fl.close()
	ft.close()
	fo.close()

if __name__ == '__main__':
	gen('1.txt','time.txt','out.srt')