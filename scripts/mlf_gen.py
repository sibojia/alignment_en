# encoding=utf-8

def gen(filename, fileout, pathname):
	f=open(filename)
	fo=open(fileout, 'w')
	fo.write('''#!MLF!#\n''')
	fo.write(pathname)
	fo.write('\n')
	for line in f: fo.write(line)
	f.close()
	fo.close()