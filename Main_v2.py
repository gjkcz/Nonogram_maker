import numpy as np
from PIL import Image
import os.path


def path_name():
    global name
    global type
    global filename
    global new_filename
    global hint_name
    global img_path
    global new_folder_path
    global main_path
    global new_img_path
    global hint_path
    filename = input("name? ")
    name, type = filename.split(".")
    new_filename = (name + "_nonogram." + type)  # new_filename = name of new (b&w, pixelated) image
    hint_name = (name + "_hint.txt")  # hint_name = name of hint for nonogram

    main_path = os.path.dirname(__file__)
    img_path = os.path.join(main_path, "_IMG", filename)  # img_path = path to original image
    if not os.path.exists(img_path):
        print("Tento soubor neexistuje, zadejte jiny nazev")
        path_name()
    new_folder_path = os.path.join(main_path, name)  # new_folder_path = path to the specific nonogram folder
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    new_img_path = os.path.join(new_folder_path, new_filename)  # new_img_path = path to the new image
    hint_path = os.path.join(new_folder_path, hint_name)  # hint_path = path to nonogram hint


def resize():
    global img
    global res_x
    global y
    global x
    print("width= " + str(img.size[0]))
    res_x = int(input("res_x? "))
    if res_x != 0:
        y = int((img.size[1] / (img.size[0] / res_x)))
        x = res_x
        img = img.resize((res_x, y))


def baw_pic():
    global img
    global baw
    global new_img_path
    baw = img.point(lambda x: 0 if x<128 else 255, '1')
    # baw = baw.crop(baw.getbbox())
    baw.save(new_img_path)
    baw.show()


def baw_to_array():
    global res_x
    global y
    global x
    global picture
    global rotate_pic
    x = int(baw.size[0])
    y = int(baw.size[1])
    img_data = baw.getdata(0)
    img_list = np.asarray(img_data, dtype=int)
    img_list = img_list.reshape((y, x))
    img_list[img_list == 0] = 1
    img_list[img_list == 255] = 0
    picture = img_list.tolist()
    rotate_pic = list(map(list, zip(*picture)))


def horizontal_hint():
    global picture
    global hint_x
    global x_max
    global more_digits
    x_max = -1
    more_digits = 0
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
                else:
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

    # remove zeros from list
    index = 0
    for i in range(len(hint_x)):
        if 0 in hint_x[i]:
            while 0 in hint_x[i]:
                hint_x[i].remove(0)
        index += 1

    # x_max = number of characters in longest row_x
    index = 0
    for i in range(len(hint_x)):
        if x_max < len(hint_x[i]):
            x_max = len(hint_x[i])
        index += 1

    for i in range(len(hint_x)):
        for j in hint_x[i]:
            n = x_max - len(hint_x[i])
            if len(hint_x[i]) < x_max:
                for k in range(n):
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
                else:
                    n += 1
                    pos += 1
                if pos == y and n != 0:
                    row_y.append(n)
                    n = 0
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
    path_name()
    img = Image.open(img_path).convert("L")  # open picture and make it grayscale
    resize()
    baw_pic()
    baw_to_array()
    horizontal_hint()
    vertical_hint()
    print(*hint_y, sep='\n')
    print(*hint_x, sep='|' + x * '_|' + '\n', end='|' + x * '_|')

    file = open(hint_path, "a")
    print(*hint_y, sep='\n', file=file)
    print(*hint_x, sep='|' + x * '_|' + '\n', end='|' + x * '_|', file=file)
    file.close()

    question = input('\n\n' + "Pro zadani noveho nonogramu stisknete y""\n"
                              "Pro ukonceni stisknete jakoukoli jinou klavesu""\n")
    if question == 'y' or question == 'Y':
        continue
    else:
        exit()
