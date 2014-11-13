# encoding=gbk
import codecs
def gen(filename, fileout, pathname):
	f=open(filename)
	fo=codecs.open(fileout, 'w','gbk')
	fo.write('''#!MLF!#\n''')
	fo.write(pathname)
	fo.write('\n')
	for line in f: fo.write(line)
	f.close()
	fo.close()