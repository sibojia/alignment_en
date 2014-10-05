# encoding=utf-8
import sys, os, check_dict, srt_convert, words_convert, cmd_wrapper, mlf_gen, mlf_conv, srt_gen

def video_conv():
	print 'This converts video to wav compatible for HTK'
	src_dir=ur"D:/BaiduYunDownload/第一周样片/MP4/"
	dest_dir="z:/C1/"
	for v in os.listdir(src_dir):
		if v.endswith('mp4'):
			basename=os.path.splitext(v)[0]
			print basename
			cmd_wrapper.ffmpeg(src_dir+v,dest_dir+basename+'.wav')


def srt_process():
	os.chdir('../data/')
	srt_dir='./srt_sample/'
	sent_dir='./sentences/'
	words_dir='./words/'
	mlf_dir='./mlfs/'
	if not os.path.exists(sent_dir): os.mkdir(sent_dir)
	if not os.path.exists(words_dir): os.mkdir(words_dir)
	if not os.path.exists(mlf_dir): os.mkdir(mlf_dir)
	for fname in os.listdir(srt_dir):
		basename=fname[:fname.rfind('.')]
		srt_convert.convert(srt_dir+fname,sent_dir+basename+'.txt')
		words_convert.convert(sent_dir+basename+'.txt',words_dir+basename+'.txt')
		check_dict.check(words_dir+basename+'.txt')
		mlf_gen.gen(words_dir+basename+'.txt_indict', mlf_dir+basename+'.mlf', '"../data/wav/'+basename+'.lab"')

def htk():
	print 'Run htk'
	os.chdir('../data/')
	mlf_dir='./mlfs/'
	res_dir='./result/'
	if not os.path.exists(mlf_dir): os.mkdir(mlf_dir)
	if not os.path.exists(res_dir): os.mkdir(res_dir)
	for fname in os.listdir(mlf_dir):
		basename=fname[:fname.rfind('.')]
		cmd_wrapper.htk(mlf_dir+basename+'.mlf',res_dir+basename+'.txt','../data/wav/'+basename+'.wav')

def srtgen():
	print 'Generate srt from result'
	os.chdir('../data/')
	res_dir='./result/'
	srt_dir='./srt_out/'
	words_dir='./words/'
	sent_dir='./sentences/'
	if not os.path.exists(srt_dir): os.mkdir(srt_dir)
	for fname in os.listdir(res_dir):
		basename=fname[:fname.rfind('.')]
		mlf_conv.convert(res_dir+fname, words_dir+basename+'.txt_index', 'time.txt')
		srt_gen.gen(sent_dir+basename+'.txt', 'time.txt', srt_dir+basename+'.srt')
	os.remove('time.txt')

def run_all(basename):
	
	
class ArgError(Exception):
	pass

if __name__ == '__main__':
	d = {'v':video_conv, 's':srt_process, 'h':htk, 'm':srtgen}
	try:
		if len(sys.argv)!=2:
			raise ArgError
		for arg in sys.argv[1]:
			if arg not in 'vshm':
				raise ArgError
			else:
				d[arg]()
	except ArgError:
		print 'Supported functions: video(v) | srt2mlf(s) | htk(h) | mlf2srt(m) | custom(c)'
		print 'You can use multiple letters to run them all, e.g. main_script.py vshm'