import time
# import numpy as np

def strtime(t):
	s = time.strftime("%H:%M:%S", time.gmtime(float(t)))
	s = s+','
	s = s+(t+'000').split('.')[1][:3]
	return s

def gen(linefile,timefile,fileout):
	fl=open(linefile)
	ft=open(timefile)
	fo=open(fileout,'w')
	i=1
	q=list()
	for line in ft:
		tok=line.strip().split(' ')
		if (float(tok[0]) == float(tok[1])):
			fo.write(' ')
			fo.write(fl.readline().strip())
			continue
		elif i!=1:
			fo.write('\n\n')
		fo.write(str(i)+'\n')
		i+=1
		fo.write(strtime(tok[0]))
		fo.write(' --> ')
		fo.write(strtime(tok[1]))
		fo.write('\n')
		s = fl.readline().strip()
		fo.write(s)
		# ------- Debug: print time/string length ratio
		# t = (float(tok[1])-float(tok[0]))/int(tok[2]) # (len(s)+1)
		# fo.write('  %.3f' % t)
		# q.append(t)
		# if len(q) > 5:
		# 	a = np.abs(q[-1] - np.mean(q))
		# 	b = np.std(q[-5:])
		# 	fo.write(' %.3f %.3f' % (a,b))
		# -------
	fo.write('\n\n')		
	fl.close()
	ft.close()
	fo.close()

if __name__ == '__main__':
	gen('1.txt','time.txt','out.srt')