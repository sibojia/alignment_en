# encoding=utf8
import subprocess,time,os,datetime,codecs,chardet,sys
import Levenshtein
from num2words import num2words

class _StaticConfig():
	"""program config"""
	cmd_htk = r'..\htk\HVite.exe'
	cmd_ffmpeg = r'..\htk\ffmpeg.exe'
	file_allword = '../htk/models/all_words_ext.txt'
	file_dict = r'..\htk\models\monophone_sp_ext.dict'
	data_allword = open(file_allword).readline().split(' ')
		
class Config():
	"""config for aligner"""
	language = 'en'
	dir_video = ur"D:/BaiduYunDownload/第四周/"
	ext_video = '.mp4'
	dir_srt_in = '../data/srt_in/'
	dir_srt_out = '../data/srt_out'

class _WordParser():
	"""Convert subtitle to basic words for HTK. 
	Support EN/CN for now."""
	dict_sub_en={
		'cos':'C',
		'sin':'S',
		'^2':'T'
	}
	dict_ext_en={
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

	def _parseChinese(self, line):
		return None

	def _parseEnglish(self, line):
		pass

	def parse(self, lines):
		

	def setLanguage(self, s):
		if s == 'cn':
			self._funcParse = self._parseChinese
		elif s == 'en':
			self._funcParse = self._parseEnglish
			# prepare english word list
			self.wordlist = open(file_allword).readlines().split(' ')

	def __init__(self, s='en'):
		self.setLanguage(s)
		

class _SubtitleData():
	"""Data structure for alignment

	Members:
	lines: subtitle lines list without time label [i]
	timeIndex: time label list for each line [(t0,t1,len_words)]
	words: valid words list ['']
	lineIndex: index of words for every subtitle line [i]
	"""
	def __init__(self):
		pass

	def loadFromSRTFile(self, filein):
		'''Load file to self.lines. Returns True if success'''
		self.lines = list()
		f=open(filein)
		next=False
		for line in f:
			if next==True:	
				if len(line.strip()) > 0: 
					self.lines.append(line.strip())
				else:
					print 'Error parsing subtitle in:', filein
					self.lines = None
					f.close()
					return False
				next=False
			if len(line)>3 and line[2]==':' and line[0]=='0':
				next=True
		f.close()
		return True

	def genMLFforHTK(self, fileout, pathname):
		fo=codecs.open(fileout, 'w','gbk')
		fo.write('''#!MLF!#\n''')
		fo.write(pathname)
		fo.write('\n')
		for w in self.words:
			fo.write(w)
			fo.write('\n')
		fo.close()

	def parseMLFResult(self, filein):
		MLF_TIME_K = 10000000
		mlf=open(filein).readlines()
		findx=self.lineIndex
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
						self.timeIndex.append((startt,0,findx[si-1]-findx[si-2])) 
														# length of sentence
						# if the last phone is a enough long sp
						if t2 == 'sp' and t-t0 > 0.8:
						# it is the end of the last sentence
							self.timeIndex[-1][1] = t0
						else:
						# otherwise the subtitle is continuous
							self.timeIndex[-1][1] = t
					startt = t
				if len(findx) > si and wi == findx[si]:
					self.timeIndex.append((startt,startt,0))
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
			self.timeIndex.append((startt,t1,findx[si-1]-findx[si-2]))
		else:
			print 'something wrong'
		fo.close()

	def _strtime(t): # float t
		s = time.strftime("%H:%M:%S", time.gmtime(t))
		s = s+','
		s = s+(str(t)+'000').split('.')[1][:3]
		return s

	def genSRTFile(self, fileout):
		fo=open(fileout,'w')
		i=1
		q=list()
		for ind,tok in enumerate(self.timeIndex):
			if (tok[0] == tok[1]):
				fo.write(' ')
				fo.write(self.lines[ind])
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
		fo.close()

class SubtitleAligner():
	"""Use HTK force alignment for subtitle automatic alignment"""
			
	def __init__(self):
		print Config.dir_video
