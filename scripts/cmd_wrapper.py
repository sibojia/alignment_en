# encoding=utf-8
import subprocess

def ffmpeg(filein,fileout):
	s=ur'..\htk\ffmpeg.exe -i "%s" -ar 16000 -acodec pcm_s16le -ac 1 "%s"' % (filein,fileout)
	print s
	return subprocess.call(s.encode('gbk'))

def htk(filein, fileout, wavfile):
	# %s: result.mlf, label.mlf, train.scp
	f=open('train.scp','w')
	f.write(wavfile)
	f.close()
	s=r"..\htk\HVite.exe -A -D -T 1 -l '*' -o S -C ..\htk\models\config.fromwav -H ..\htk\models\wsj_mono\macros -H ..\htk\models\wsj_mono\hmmdefs -i %s -m -t 250.0 150.0 1000.0 -y lab -a -I %s -S train.scp ..\htk\models\monophone_sp.dict ..\htk\models\monophones_sp" % (fileout, filein)
	return subprocess.call(s)