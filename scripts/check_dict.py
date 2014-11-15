from Levenshtein import distance

words=open('../htk/models/all_words_ext.txt').readline().split(' ')

def check(filename):
	print '\n',filename
	f=open(filename)
	fo=open(filename+'_indict','w')
	for line in f:
		s = line.strip().lower()
		if not s in words:
			ds = [distance(s,i) for i in words]
			index = ds.index(min(ds))
			print s, ' (',words[index],')'
			fo.write(words[index]+'\n')
		else:
			fo.write(line)
	f.close()
	fo.close()

if __name__ == '__main__':
	check('w.txt')