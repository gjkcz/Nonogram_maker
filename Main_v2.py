import numpy as np
from PIL import Image
import os.path

def name():
    global name
    global type
    global filename
    global new_filename
    global folder_path
    global path
    name, type = input("name? ").split(".")
    name = str(name)
    type = str(type)
    filename = (name + "." + type)
    new_filename = (name + "_nonogram." + type)
    folder_path = "D:/nonogram/"
    path = os.path.join(folder_path, filename)

def pic():
    global picture                                                                       # nonogram picture (in 1 and 0)
    global y
    global rotate_pic
    line1 = []
    for i in range(0, y):
        # line1 = [int(n) for n in input('line {} '.format(i+1)).split()]
        line1 = list(map(int, input('line {} '.format(i+1)).split()))
        picture.append(line1)
    print(*picture, sep="\n")

    rotate_pic = list(map(list, zip(*picture)))                                              # rotate picture 90 degrees
    # print(*rotate_pic, sep="\n")

def resize():
    global img
    global res_x
    global y
    # y = int((img.size[1]/(img.size[0]/res_x)))
    img = img.resize((res_x, y))

def baw_pic():
    global img
    global baw
    global new_filename
    global folder_path
    baw = img.point(lambda x: 0 if x<128 else 255, '1')
    new_path = os.path.join(folder_path + new_filename)
    baw.save(new_path)
    baw.show()

def baw_to_array():
    global res_x
    global y
    global x
    global picture
    global rotate_pic
    img_data = baw.getdata(0)
    img_list = np.asarray(img_data, dtype=int)
    img_list = img_list.reshape((y, x))
    print(baw.size)
    img_list[img_list == 0] = 1
    img_list[img_list == 255] = 0
    picture = img_list.tolist()
    rotate_pic = list(map(list, zip(*picture)))

def horizontal_hint():
    global picture
    global hint_x
    global x_max
    row_x = []
    n = 0
    index = 0
    pos = 0
    for i in range(len(picture)):
        if 1 in picture[i] and 0 in picture[i]:
            row_x.clear()
            for l in range(len(picture[i])):
                if picture[i][l] == 0:
                    row_x.append(n)
                    if n != 0:
                        row_x.append(0)
                    n = 0
                    pos += 1
                elif picture[i][l] == 1:
                    n += 1
                    pos += 1
                if pos == x and n != 0:
                    row_x.append(n)
                    n = 0
            # row_x.append('|')
            hint_x.append(row_x[:])
            pos = 0
        elif 1 in picture[i] and 0 not in picture[i]:
            row_x.clear()
            row_x.append(picture[i].count(1))
            # row_x.append('|')
            hint_x.append(row_x[:])
            index += 1
        elif 1 not in picture[i] and 0 in picture[i]:
            row_x.clear()
            row_x.append(' ')
            # row_x.append('|')
            hint_x.append(row_x[:])
            index += 1

    index = 0
    for i in range(len(hint_x)):                                                                # remove zeros from list
        if 0 in hint_x[i]:
            while 0 in hint_x[i]:
                hint_x[i].remove(0)
        index += 1

    index = 0                                                            # x_max = number of characters in longest row_x
    for i in range(len(hint_x)):
        if x_max < len(hint_x[i]):
            x_max = len(hint_x[i])
        index += 1

    for i in range(len(hint_x)):
        for j in hint_x[i]:
            n = x_max - len(hint_x[i])
            if len(hint_x[i]) < x_max:
                for k in range (n):
                    hint_x[i].insert(0, ' ')

    hint_x = [' '.join([str(c) for c in lst]) for lst in hint_x]

def vertical_hint():
    global rotate_pic
    global hint_y
    global x_max
    global x
    global y
    y_max = -1
    row_y = []
    pos = 0
    n = 0
    for i in range(len(rotate_pic)):
        if 1 in rotate_pic[i] and 0 in rotate_pic[i]:                     # if 1 in rotate_pic[i] and 0 in rotate_pic[i]
            row_y.clear()
            for l in range(len(rotate_pic[i])):
                if rotate_pic[i][l] == 0:
                    row_y.append(n)
                    if n != 0:
                        row_y.append(0)
                    n = 0
                    pos += 1
                elif rotate_pic[i][l] == 1:
                    n += 1
                    pos += 1
                if pos == y and n != 0:
                    row_y.append(n)
                    n = 0
            # row_y.append('_')
            hint_y.append(row_y[:])
            pos = 0
        elif 1 in rotate_pic[i] and 0 not in rotate_pic[i]:
            row_y.clear()
            row_y.append(rotate_pic[i].count(1))
            # row_y.append('_')
            hint_y.append(row_y[:])
        elif 1 not in rotate_pic[i] and 0 in rotate_pic[i]:
            row_y.clear()
            row_y.append(' ')
            # row_y.append('_')
            hint_y.append(row_y[:])

    for i in range(len(hint_y)):                                                                # remove zeros from list
        if 0 in hint_y[i]:
            while 0 in hint_y[i]:
                hint_y[i].remove(0)

    for i in range(len(hint_y)):                                         # y_max = number of characters in longest row_y
        if y_max < len(hint_y[i]):
            y_max = len(hint_y[i])

    for i in range(len(hint_y)):                                     # add  (y_max - len(hint_y)) * ' ' to the beginning
        for j in hint_y[i]:
            n = y_max - len(hint_y[i])
            if len(hint_y[i]) < y_max:
                for k in range(n):
                    hint_y[i].insert(0, ' ')

    hint_y = list(map(list, zip(*hint_y)))

    for m in range(len(hint_y)):                                                   # add  x_max * ' ' to the beginning
        for n in range(x_max):
                hint_y[m].insert(0, ' ')

    hint_y = [' '.join([str(c) for c in lst]) for lst in hint_y]

while True:
    picture = []
    rotate_pic = []
    hint_x = []
    hint_y = []
    x_max = -1
    name()
    img = Image.open(path).convert("L")  # open picture and make it grayscale
    res_x = int(input("res_x? "))
    if res_x == 0:
        x = int(img.size[0])
        y = int(img.size[1])
    else:
        y = int((img.size[1] / (img.size[0] / res_x)))
        x = res_x
        resize()
    baw_pic()
    baw_to_array()

    # pic()
    # rotate_pic = list(map(list, zip(*picture)))
    horizontal_hint()
    vertical_hint()
    print('Nonogram''\n')
    print(*hint_y, sep='\n')
    print(*hint_x, sep='|' + x * '_|' + '\n', end='|' + x * '_|')
    question = input('\n\n' + "Pro zadani noveho nonogramu stisknete y""\n"
                              "Pro ukonceni stisknete jakoukoli jinou klavesu""\n")
    if question == 'y' or question == 'Y':
        continue
    else:
        exit()