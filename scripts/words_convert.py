# encoding=utf-8
from num2words import num2words

dict_sub={
	'cos':'C',
	'sin':'S',
	'^2':'T'
}
dict_ext={
	'+':['plus'],
	'-':['minus'],
	'*':['times'],
	'×':['times'],
	'/':['over'],
	'=':['equals'],
	'%':['percent'],
	'!':['factorial'],
	u'±':['plus','or','minus'],
	u'√':['square','root'],
	u'α':['alpha'],
	u'β':['beta'],
	u'γ':['gamma'],
	u'θ':['theta'],
	u'π':['pi'],
	u'Σ':['sigma'],
	u'∑':['sigma'],
	u'∞':['infinity'],
	'T':['square'],
	'C':['consine'],
	'S':['sine']
}


def convert_old(filein, fileout):
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


def convert_word(w):
	w=w.replace(',','').replace('  ',' ')
	w_test = w
	while len(w_test) > 0 and w_test[0] in ' (\'"' : w_test=w_test[1:]
	while len(w_test) > 0 and w_test[-1] in ' .,:;?!\'")': w_test=w_test[:-1]
	lenw = len(w_test)
	chars = [i for i in w_test if (i < 'a' or i > 'z') and i not in '\'"']
	if len(chars) > 0 and (lenw <= 4  or lenw/len(chars) < 4):
		# Heuristic rule for math expression
		print w_test
		for k in dict_sub: w_test=w_test.replace(k,dict_sub[k])
		digits=''
		is_power=False
		l=[]
		for c in w_test.decode('u8'):
			if (c>='0' and c<='9') or c=='.':
				digits+=c
			else:
				if len(digits) > 0:
					# l.append(float(digits)) expand it now
					l += num2words(float(digits)).replace('-',' ').split(' ')
					digits = ''
					if is_power:
						l.append('power')
						is_power=False
				if dict_ext.has_key(c):
					l+=dict_ext[c]
				elif c=='^':
					is_power = True
					l+=['to','the']
					continue
				elif c>='a' and c<='z':
					l.append(c)
				if is_power:
					# l.append('power') complicated power, ignoring
					is_power=False
		if len(digits) > 0 : l += num2words(float(digits)).replace('-',' ').split(' ')
		if is_power : l.append('power')
		return l
	elif set(chars) == {'-'}: # like-a-king
		return w_test.split('-')
	elif set(chars).issubset({'(',')'}): # alright(yeah)
		return w_test.replace('(',' ').replace(')',' ').strip().split(' ')
	else:
		return [w_test]

def convert(filein, fileout):
	f=open(filein)
	fo=open(fileout,'w')
	foi=open(fileout+'_index','w')
	i=0
	for line in f:
		foi.write(str(i)+'\n')
		words=line.strip().lower().split(' ')
		for w in words:
			wlist = convert_word(w)
			for w in wlist:
				if len(w) > 0:
					fo.write(w.strip())
					fo.write('\n')
					i=i+1
	fo.close()
	f.close()
	foi.close()

if __name__ == '__main__':
	convert_new('z:/1.txt','z:/w.txt')
	# print convert_word('(b^(3)-1021.4ac')