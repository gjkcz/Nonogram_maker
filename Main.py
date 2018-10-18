
x_max = 0
x = int(input('width?'))
y = int(input('height?'))               #input the dimensions of the picture
print(x, y)

picture = []                            #nonogram picture (in 1 and0 )
for i in range(0, y):
    line1 = [int(n) for n in input('line {} '.format(i+1)).split()]
    picture.append(line1)
print(*picture, sep="\n")

rotate_pic = map(list, zip(*picture))   #rotate pictur 90 digrees
print(*rotate_pic, sep="\n")