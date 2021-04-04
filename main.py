import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import(
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
    GaussianBlur, UnsharpMask
)

app = QApplication([])

main_win = QWidget()
main_win.setWindowTitle('Пустое окно')
poisk = QPushButton('Поиск')
chb = QPushButton('Ч/Б')
rezkost = QPushButton('РЕЗКОСТЬ')
zerkalo = QPushButton('Зеркало')
pravo = QPushButton('Право')
levo = QPushButton('Лево')
kartinka = QLabel('Картинка')
papka = QPushButton('Папка')
papka_list = QListWidget()
line1 = QVBoxLayout()
line2 = QHBoxLayout()
line3 = QVBoxLayout()
line4 = QHBoxLayout()

line1.addWidget(papka)
line1.addWidget(papka_list)

line2.addWidget(poisk)
line2.addWidget(chb)
line2.addWidget(rezkost)
line2.addWidget(zerkalo)
line2.addWidget(pravo)
line2.addWidget(levo)

line3.addWidget(kartinka)
line3.addLayout(line2)

line4.addLayout(line1)
line4.addLayout(line3)

main_win.setLayout(line4)
main_win.show()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
   
def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir() 
    filenames = filter(os.listdir(workdir), extensions)
    papka_list.clear()
    for filename in filenames:
        papka_list.addItem(filename)
    
papka.clicked.connect(showFilenamesList)

class ImageProcessor():

    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/" 
    def loadImage(self, filename):
        # при загрузке запоминаем путь и имя файла
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(image_path)


    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path,self.filename)
        workimage.showImage(image_path)
        
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        fullname = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
  

    def showImage(label, path):
        kartinka.hide()
        pixmapimage = QPixmap(path)
        w, h = kartinka.width(), kartinka.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        kartinka.setPixmap(pixmapimage)
        kartinka.show()
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        fullname = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        fullname = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        fullname = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        fullname = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
def showChosenImage():
    if papka_list.currentRow() >= 0:
        filename = papka_list.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))

workimage = ImageProcessor()
papka_list.currentRowChanged.connect(showChosenImage)
chb.clicked.connect(workimage.do_bw)
rezkost.clicked.connect(workimage.do_sharpen)
pravo.clicked.connect(workimage.do_right)
levo.clicked.connect(workimage.do_left)
zerkalo.clicked.connect(workimage.do_flip)
app.exec_()