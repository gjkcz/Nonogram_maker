#############################################################################################
#                                                                                           #
#   |\   | |---| |\   | |---| |---| |--\ |---| |\    /|      |\    /| |---| |  / |--- |--\  #
#   | \  | |   | | \  | |   | |  _  |__| |   | | \  / |      | \  / | |   | |_/  |___ |__|  #
#   |  \ | |   | |  \ | |   | |   | | \  |---| |  \/  |      |  \/  | |---| | \  |    | \   #
#   |   \| |___| |   \| |___| |___| |  \ |   | |      |      |      | |   | |  \ |___ |  \  #
#                                                                                           #
#############################################################################################
import numpy as np
from PIL import Image
import os.path
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, \
                            QFileDialog, QDesktopWidget, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QPixmap


class App(QWidget):
    def __init__(self):
        super().__init__()
        global picture
        global rotate_pic
        global hint_x
        global hint_y
        picture = []
        rotate_pic = []
        hint_x = []
        hint_y = []
        self.gui()
        self.path_name()
        self.open_resize()
        self.baw_pic()
        self.baw_to_array()
        self.horizontal_hint()
        self.vertical_hint()
        self.print()
        self.repeat()

    def gui(self):
        self.setWindowTitle("Nonogram_maker")
        self.setWindowIcon(QIcon("kepler.png"))
        label = QLabel(self)
        pixmap = QPixmap("icon.png")
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.setGeometry(700, 350, 500, 500)
        self.show()


    def path_name(self):
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
        cesta = os.path.join(os.path.dirname(__file__), "_IMG")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Zvolte výchozí obrázek", cesta,
                                                  "Images (*.png *.jpg *.bmp)", options=options)
        if filename:
            _, filename = os.path.split(filename)
            name, type = filename.split(".")
            # ▼new_filename = name of new (b&w, pixelated) image
            new_filename = (name + "_nonogram." + type)
            # ▼hint_name = name of hint for nonogram
            hint_name = (name + "_hint.txt")
            main_path = os.path.dirname(__file__)
            # ▼img_path = path to original image
            img_path = os.path.join(main_path, "_IMG", filename)
            # ▼new_folder_path = path to the specific nonogram folder
            new_folder_path = os.path.join(main_path, name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            # ▼new_img_path = path to the new image
            new_img_path = os.path.join(new_folder_path, new_filename)
            # ▼hint_path = path to nonogram hint
            hint_path = os.path.join(new_folder_path, hint_name)


    def open_resize(self):
        global img
        global res_x
        global y
        global x
        # ▼open picture and make it grayscale
        img = Image.open(img_path).convert("L")
        text = "Obrázek má rozlišení " + str(img.size[0]) + "x" + str(img.size[1]) + "px. Přejete si změnit?"
        res_x, okpressed = QInputDialog.getInt(self, "Nonogram_maker", text, 0, 0, 100, 1)
        if okpressed and res_x != 0:
            y = int((img.size[1] / (img.size[0] / res_x)))
            x = res_x
            img = img.resize((res_x, y))


    def baw_pic(self):
        global img
        global baw
        global new_img_path
        baw = img.point(lambda x: 0 if x < 128 else 255, '1')
        # baw = baw.crop(baw.getbbox())
        baw.save(new_img_path)
        # baw.show()


    def baw_to_array(self):
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


    def horizontal_hint(self):
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
                hint_x.append(row_x[:])
                pos = 0
            elif 1 in picture[i] and 0 not in picture[i]:
                row_x.clear()
                row_x.append(picture[i].count(1))
                hint_x.append(row_x[:])
                index += 1
            elif 1 not in picture[i] and 0 in picture[i]:
                row_x.clear()
                row_x.append(' ')
                hint_x.append(row_x[:])
                index += 1

        # ▼remove zeros from list
        index = 0
        for i in range(len(hint_x)):
            if 0 in hint_x[i]:
                while 0 in hint_x[i]:
                    hint_x[i].remove(0)
            index += 1

        # ▼x_max = number of characters in longest row_x
        index = 0
        for i in range(len(hint_x)):
            if x_max < len(hint_x[i]):
                x_max = len(hint_x[i])
            index += 1

        # ▼add spaces to hint_x lines
        for i in range(len(hint_x)):
            for j in hint_x[i]:
                n = x_max - len(hint_x[i])
                if len(hint_x[i]) < x_max:
                    for k in range(n):
                        hint_x[i].insert(0, ' ')

        hint_x = [' '.join([str(c) for c in lst]) for lst in hint_x]


    def vertical_hint(self):
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
            if 1 in rotate_pic[i] and 0 in rotate_pic[i]:
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
                hint_y.append(row_y[:])
            elif 1 not in rotate_pic[i] and 0 in rotate_pic[i]:
                row_y.clear()
                row_y.append(' ')
                hint_y.append(row_y[:])

        # ▼remove zeros from list
        for i in range(len(hint_y)):
            if 0 in hint_y[i]:
                while 0 in hint_y[i]:
                    hint_y[i].remove(0)

        # ▼y_max = number of characters in longest row_y
        for i in range(len(hint_y)):
            if y_max < len(hint_y[i]):
                y_max = len(hint_y[i])

        # ▼add  (y_max - len(hint_y)) * ' ' to the beginning
        for i in range(len(hint_y)):
            for j in hint_y[i]:
                n = y_max - len(hint_y[i])
                if len(hint_y[i]) < y_max:
                    for k in range(n):
                        hint_y[i].insert(0, ' ')

        hint_y = list(map(list, zip(*hint_y)))

        # ▼add  x_max * ' ' to the beginning
        for m in range(len(hint_y)):
            for n in range(x_max):
                    hint_y[m].insert(0, ' ')

        hint_y = [' '.join([str(c) for c in lst]) for lst in hint_y]


    def print(self):
        print(*hint_y, sep='\n')
        print(*hint_x, sep='|' + x * '_|' + '\n', end='|' + x * '_|')
        # ▼print hint to file
        file = open(hint_path, "a")
        print(*hint_y, sep='\n', file=file)
        print(*hint_x, sep='|' + x * '_|' + '\n', end='|' + x * '_|', file=file)
        file.close()


    def repeat(self):
        question = QMessageBox.question(self, 'Nonogram_maker', "Chcete vytvořit další nonogram?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if question == QMessageBox.Yes:
            self.__init__()
        else:
            exit()


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
