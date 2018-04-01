file = open('1.csv')
for index, line in enumerate(file):
    tmp_line = line.lstrip('').rstrip('\n').split(';')
    if tmp_line[0]=='':
        tmp_line.pop(0)
    print(tmp_line)