# encoding=gbk
import subprocess,time,os,datetime,codecs,chardet

def ffmpeg(filein,fileout):
	s=ur'..\htk\ffmpeg.exe -i "%s" -ar 16000 -acodec pcm_s16le -ac 1 "%s"' % (filein,fileout)
	print s
	return subprocess.call(s.encode('gbk'))

def htk(filein, fileout, wavfile):
	# %s: result.mlf, label.mlf, train.scp
	f=codecs.open('train.scp','w','gbk')
	f.write(wavfile)
	f.close()
	s=r"..\htk\HVite.exe -A -D -T 1 -l '*' -C ..\htk\models\config.fromwav -H ..\htk\models\wsj_mono\macros -H ..\htk\models\wsj_mono\hmmdefs -i %s -m -y lab -t 1000 20000 41000 -a -I %s -S train.scp ..\htk\models\monophone_sp.dict ..\htk\models\monophones_sp" % (fileout, filein)
	tic = time.time()
	ret = subprocess.call(s.encode('gbk'))
	toc = int(time.time()-tic)
	os.remove('train.scp')
	log=open('htk.log','a')
	log.write(datetime.datetime.now().strftime('%c')+' ')
	log.write(filein.encode('utf8'))
	log.write(': %d:%2d (%s)' % (toc/60, toc%60, str(ret))+'\n')
	log.close()
	print 'Time elapsed:', '%d:%2d' % (toc/60, toc%60), 'with return code', ret

if __name__ == '__main__':
	# ffmpeg('z:/1.wma','z:/1.wav')
	htk('test.mlf','test_out.mlf','1.wav')