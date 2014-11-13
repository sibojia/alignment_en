
MLF_TIME_K = 10000000

def convert(mlffile,indexfile,fileout):
	mlf=open(mlffile).readlines()
	findx=[int(i.strip()) for i in open(indexfile).readlines()]
	si=0
	wi=0
	startt=-1
	fo=open(fileout,'w')
	for line in mlf:
		tok=line.strip().split(' ')
		if len(tok) < 4:continue
		if len(tok) == 5:
			if len(findx) > si and wi == findx[si]: # this is the start of a sentence
				si+=1
				t=float(tok[0])/MLF_TIME_K - 0.2
				if startt != -1: # print last sentence
					fo.write(str(startt)+' ')
					# if the last phone is a enough long sp
					if t2 == 'sp' and t-t0 > 0.8:
					# it is the end of the last sentence
						fo.write(str(t0))
					else:
					# otherwise the subtitle is continuous
						fo.write(str(t))
					fo.write(' ' + str(findx[si-1]-findx[si-2])) # length of sentence
					fo.write('\n')
				startt = t
			if len(findx) > si and wi == findx[si]:
				fo.write(str(startt) + ' ' + str(startt) + ' 0\n')
				si+=1
			wi+=1
		t0=float(tok[0])/MLF_TIME_K
		t1=float(tok[1])/MLF_TIME_K
		t2=tok[2]
		if t2 == 'sp' and t1-t0 > 5.0 and wi == 1:
			# Title music?
			print '\tDetected title music'
			startt = t1-1.0

	if startt != -1:
		fo.write(str(startt)+' ')
		fo.write(str(t1))
		fo.write(' ' + str(findx[si-1]-findx[si-2]) + '\n')
	else:
		print 'something wrong'
	fo.close()

if __name__ == '__main__':
	convert('aligned.mlf','w.txt_index','time.txt')



