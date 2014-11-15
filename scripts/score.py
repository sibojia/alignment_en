# encoding=utf-8
import Levenshtein

'''
data: [(startTime, endTime, content, isContinuous)]
score: 100 means identical. Higher the better.
'''

def _parsetime(s):
	try:
		l1=(s.split(',')[0]).split(':')
		s2=s.split(',')[1]
		t = int(l1[0])*3600 + int(l1[1])*60 + int(l1[2]) + ((int(s2)+0.0)/pow(10,len(s2)))
		return t
	except Exception, e:
		print 'Error parsing time:', s, e
		return -1

def _read(filein):
	f=open(filein)
	next=False
	ts=''
	data = []
	for line in f:
		if next==True:
			if len(line.strip()) > 0:
				l=ts.split('-->')
				t1 = _parsetime(l[0].strip())
				t2 = _parsetime(l[1].strip())
				if len(data) == 0:
					data.append((t1, t2, line.strip(), False))
				else:
					data.append((t1, t2, line.strip(), t1 == data[-1][1]))
			else:
				print 'Error parsing subtitle in:', filein, ',',line
				data = None
				break
			next=False
		if len(line)>3 and line[2]==':' and line[0]=='0':
			next=True
			ts=line
	f.close()
	return data

def _dataAlign(d1,d2):
	imap=[]
	for i,x in enumerate(d1):
		base = 0
		if len(imap) > 0: base=imap[-1]+1
		while len(d2) > base and Levenshtein.ratio(x[2],d2[base][2]) < 0.9: base+=1
		if len(d2) > base:
			imap.append(base)
		else:
			print 'Error aligning two files'
			return None
	return imap


def getScore(fname1, fname2):
	data1 = _read(fname1)
	data2 = _read(fname2)
	tsum=0.
	tdiff=0.
	if data1 != None and data2 != None:
		imap = _dataAlign(data1,data2)
		for i1,i2 in enumerate(imap):
			if not data1[i1][3] and not data2[i2][3]:
				tdiff += abs(data1[i1][0] - data2[i2][0])
			tdiff += abs(data1[i1][1] - data2[i2][1])
			tsum += data1[i1][1] - data1[i1][0]
	return 100-tdiff/tsum*100

if __name__ == '__main__':
	print 'hello'
	print getScore(r"D:\work\align_en\acc_test\4-3-2_truth.srt", r"D:\work\align_en\acc_test\4-3-2_orig.srt")
	print getScore(r"D:\work\align_en\acc_test\4-3-2_truth.srt", r"D:\work\align_en\acc_test\4-3-2_new.srt")
	'''
	result: 72.7554808563 86.7221986222
	Cheers~
	'''