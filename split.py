fob = open('new.txt', 'r', encoding = 'utf-8')

for line in fob.readlines():
	c = line.strip('\n')
	if len(c) == 0:
		continue
	try:
		ymd = c[0:8]
		# content = c.split('/m ')[1]
	except Exception as e:
		print('error:', e)
		continue
	
	ff = open(ymd + '.txt', 'a', encoding = 'utf-8') #追加方式写文件，重复运行前要先删除之前的文件
	ff.write(c + '\n')
	ff.close()

fob.close()