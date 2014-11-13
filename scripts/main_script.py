# encoding=utf-8
import sys, os, check_dict, srt_convert, words_convert, cmd_wrapper, mlf_gen, mlf_conv, srt_gen

dirs = {
	'video_in': ur"D:/BaiduYunDownload/第四周/",
	'wav': './wav/',
	'srt_in': './srt_in/',
	'sentences': './sentences/',
	'words': './words/',
	'mlf_in': './mlfs/',
	'mlf_out': './result/',
	'srt_out': './srt_out/'
}

video_ext = '.mp4'

def video_conv(basename_list):
	print 'This converts video to wav compatible for HTK'
	for basename in basename_list:
		print basename
		cmd_wrapper.ffmpeg(dirs['video_in']+basename+video_ext,dirs['wav']+basename+'.wav')


def srt_process(basename_list):
	print 'Generate label files from subtitle'
	for basename in basename_list:
		print basename
		srt_convert.convert(dirs['srt_in']+basename+'.srt',dirs['sentences']+basename+'.txt')
		words_convert.convert(dirs['sentences']+basename+'.txt',dirs['words']+basename+'.txt')
		check_dict.check(dirs['words']+basename+'.txt')
		mlf_gen.gen(dirs['words']+basename+'.txt_indict', dirs['mlf_in']+basename+'.mlf', '"../data/wav/'+basename+'.lab"')

def htk(basename_list):
	print 'Run HTK'
	for basename in basename_list:
		cmd_wrapper.htk(dirs['mlf_in']+basename+'.mlf',dirs['mlf_out']+basename+'.txt','../data/wav/'+basename+'.wav')

def srtgen(basename_list):
	print 'Generate srt from result'
	for basename in basename_list:
		print basename
		mlf_conv.convert(dirs['mlf_out']+basename+'.txt', dirs['words']+basename+'.txt_index', 'time.txt')
		srt_gen.gen(dirs['sentences']+basename+'.txt', 'time.txt', dirs['srt_out']+basename+'.srt')
	# os.remove('time.txt')


class ArgError(Exception):
	pass

if __name__ == '__main__':
	d = {'v':video_conv, 's':srt_process, 'h':htk, 'm':srtgen}
	try:
		if len(sys.argv)!=2 and len(sys.argv)!=3:
			raise ArgError
		os.chdir('../data/')
		# check and mkdir
		for d_name in dirs.values():
			if not os.path.exists(d_name): os.mkdir(d_name)
		name_list = list()
		if len(sys.argv) == 2:
			name_list = [os.path.splitext(s)[0] for s in os.listdir(dirs['video_in'])]
		else:
			name_list = [sys.argv[2]]
		if sys.argv[1] == 'a':
			d['v'](name_list)
			d['s'](name_list)
			d['h'](name_list)
			d['m'](name_list)
		else:
			for arg in sys.argv[1]:
				if arg not in 'vshm':
					raise ArgError
				else:
					d[arg](name_list)
	except ArgError:
		print 'Supported functions: video(v) | srt2mlf(s) | htk(h) | mlf2srt(m) | all(a)'
		print 'You can use multiple letters, e.g. main_script.py vshm [specify file] or run on all files'