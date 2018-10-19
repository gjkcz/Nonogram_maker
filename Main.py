# Nonogram_maker
x = int(input('width?'))
y = int(input('height?'))                   # input the dimensions of the picture
# print(x, y)

picture = []                                # nonogram picture (in 1 and 0)
for i in range(0, y):
    line1 = [int(n) for n in input('line {} '.format(i+1)).split()]
    picture.append(line1)
# print(*picture, sep="\n")

rotate_pic = map(list, zip(*picture))       # rotate picture 90 degrees
# print(*rotate_pic, sep="\n")

hint_x = []
row_x = []
x_max = -1
for i in picture:
    if i.count(0) > 0:
        b = i.index(0)
        row_x = [sum(i[:b]), sum(i[b:])]
        row_x = row_x[::-1]                 # reverse the order of row_x,
        row_x.insert(0, '|')                # add '|' to the begining of row_x,
        row_x = row_x[::-1]                 # reverse back the order of row_x
        if x_max == -1:
            x_max = row_x.count(1)
        else:
            if row_x.count(1) > x_max:
                x_max = row_x.count(1)
        hint_x.append(row_x)
    else:
        row_x = [i.count(1)]
        row_x.insert(1, '|')                # add '|' to the end of row_x
        if x_max == -1:
            x_max = row_x.count(1)
        else:
            if row_x.count(1) > x_max:
                x_max = row_x.count(1)
        hint_x.append(row_x)

#print(*hint_x, sep="\n")
print(x_max)

#hint_y = []
#for i in rotate_pic:
#    b = i.index(0)
#    row_y = [sum(i[:b]), sum(i[b:])]
#    hint_y.append(row_y)
#hint_y = map(list, zip(*picture))
#print(hint_y)
