# encoding=utf-8
from num2words import num2words

def convert(filein, fileout):
	f=open(filein)
	fo=open(fileout,'w')
	foi=open(fileout+'_index','w')
	i=0
	for line in f:
		foi.write(str(i)+'\n')
		words=line.strip().lower().replace('-',' ').split(' ')
		for w in words:
			while len(w) > 0 and w[0] in ' (\'"' : w=w[1:]
			while len(w) > 0 and w[-1] in ' .,:;?!\'"/-=+_~)': w=w[:-1]
			if len(w) > 0 and w[-1]=='%':
				w=w[:-1]
				percent=True
			else:
				percent=False
			if len(w) == 0: continue
			try:
				d=float(w.replace(',','')) # case 1,000
				w=num2words(d)
				w=w.replace(',','')
				if percent: w=w+' percent'
			except ValueError:
				pass
			w=w.replace('-',' ')
			rewords = w.split(' ')
			for w2 in rewords:
				if len(w2) > 0:
					fo.write(w2.strip())
					fo.write('\n')
					i=i+1
	fo.close()
	f.close()
	foi.close()

if __name__ == '__main__':
	convert('1.txt','w.txt')