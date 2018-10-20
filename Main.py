# |\   | |̄̄̄| |\   | |̄̄̄| |̄̄̄| |̄̄\ |̄̄̄| |\    /|      |\    /| |̄̄̄| |  / |̄̄̄ |̄̄\
# | \  | |   | | \  | |   | |  _  |__| |   | | \  / |      | \  / | |   | |_/  |___ |__|
# |  \ | |   | |  \ | |   | |   | | \  |̄̄̄| |  \/  |      |  \/  | |̄̄̄| | \  |    | \
# |   \| |___| |   \| |___| |___| |  \ |   | |      |      |      | |   | |  \ |___ |  \




def pic():
    global picture                                # nonogram picture (in 1 and 0)
    global y
    global rotate_pic
    for i in range(0, y):
        line1 = [int(n) for n in input('line {} '.format(i+1)).split()]
        picture.append(line1)
    # print(*picture, sep="\n")

    rotate_pic = map(list, zip(*picture))       # rotate picture 90 degrees
    # print(*rotate_pic, sep="\n")


def horizontal_hint():
    global picture
    global hint_x
    global x_max
    index = -1
    for i in picture:
        if i.count(0) > 0 and i.count(1) > 0:
            b = i.index(0)
            row_x = [sum(i[:b]), sum(i[b:])]
            row_x = row_x[::-1]                 # reverse the order of row_x,
            row_x.insert(0, '|')                # add '|' to the beginning of row_x,
            row_x = row_x[::-1]                 # reverse back the order of row_x
            if x_max == -1:                     # x_max = number of characters in longest row_x
               x_max = len(row_x)
            else:
               if len(row_x) > x_max:
                   x_max = len(row_x)
            hint_x.append(row_x)
        else:
            if i.count(1) > 1:
                row_x = [i.count(1)]
                row_x.insert(1, '|')               # add '|' to the end of row_x
                hint_x.append(row_x)
                if x_max == -1:
                    x_max = len(row_x)
                else:
                    if len(row_x) > x_max:
                      x_max = len(row_x)
            else:
                row_x = [' ']
                row_x.insert(1, '|')
                hint_x.append(row_x)

    x_max = (2 * x_max) - 1

    index = 0
    for i in hint_x:
        for n in hint_x[index]:
            if len(hint_x[index]) * 2 - 1 < x_max:
                number = (x_max - (len(hint_x[index])) - 2)
                print(number)
                hint_x[index].insert(0, (number * ' '))
        index += 1

    hint_x = [' '.join([str(c) for c in lst]) for lst in hint_x]

    # print(*hint_x, sep="\n")


def vertical_hint():
    global hint_y
    global x_max
    global y_max
    global x
    for i in rotate_pic:
        if i.count(0) > 0 and i.count(1) > 0:
            b = i.index(0)
            row_y = [sum(i[:b]), sum(i[b:])]
            row_y = row_y[::-1]                 # reverse the order of row_y,
            row_y.insert(0, '-')                # add '_' to the beginning of row_y,
            row_y = row_y[::-1]                 # reverse back the order of row_y
            hint_y.append(row_y)
        else:
            if i.count(1) > 1:
                row_y = [i.count(1)]
                row_y = row_y[::-1]
                row_y.insert(0, '-')
                row_y = row_y[::-1]
                hint_y.append(row_y)
            else:
                row_y = [' ']
                row_y = row_y[::-1]
                row_y.insert(0, '-')
                row_y = row_y[::-1]
                hint_y.append(row_y)

    index = 0
    for i in hint_y:                                        # find the longest hint_y sublist
        if len(hint_y[index]) > y_max:
            y_max = len(hint_y[index])
        index += 1

    index = 0
    for i in hint_y:                                        # add  (y_max - len(hint_y)) * ' ' to the beginning
        for l in hint_y[index]:
            n = y_max - len(hint_y[index])
            if len(hint_y[index]) < y_max:
                for n in range(n):
                    hint_y[index].insert(0, ' ')
        index += 1

    hint_y = map(list, zip(*hint_y))

    # index = 0
    # for n in hint_y:
    #     hint_y[index].insert(0, (x_max * ' '))
    #     index += 1

    hint_y = [' '.join([str(c) for c in lst]) for lst in hint_y]


picture = []
rotate_pic = []
hint_x = []
hint_y = []
x_max = -1
y_max = -1
x = int(input('width? '))                    # input the dimensions of the picture
y = int(input('height? '))
pic()
# horizontal_hint()
vertical_hint()
print(*hint_y, sep="\n")
# print(*hint_x, sep="\n")
