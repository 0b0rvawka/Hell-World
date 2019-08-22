# -*- coding: utf-8 -*-

import sys
import the_packet_filter
import merge
#import graphy
import ipaddress
from os import listdir, getcwd
from os.path import isfile, join
from PyQt5.QtCore import QMetaObject, QDateTime, QRect, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QBrush, QColor, QFont
from PyQt5.Qt import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPixmap
from PyQt5.QtWidgets import QMessageBox, QFrame, QMainWindow, QApplication, QDesktopWidget, QTableWidgetItem, QWidget,\
    QProgressBar, QTabWidget, QPushButton, QLabel, QLineEdit, QCheckBox, QPlainTextEdit, QDateTimeEdit, QTableWidget,\
    QStatusBar, QFileDialog, QRadioButton, QDialog, QComboBox, QGridLayout, QHeaderView, QAbstractItemView,\
    QGraphicsScene, QGraphicsView

class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.transprot_mass =[]
        self.netprot_mass =[]
        self.filtering_is_on = 0

        grid = QGridLayout()
        self.setLayout(grid)

        self.IP_list = IP_list(self)
        self.TransProt_list = TransProt_list(self)
        self.NetProt_list = NetProt_list(self)
        self.setWindowTitle('Гамма')
        self.setWindowIcon(QIcon('допочки\Gamma_200x200.png'))
        self.resize(740, 830)
        self.to_center()
        self.centralwidget = QWidget(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(20, 20, 700, 750))
        self.tab = QWidget()

        grid.addWidget(self.tab)

        self.cb_time = QCheckBox(self.tab)
        self.cb_time.setGeometry(QRect(360, 130, 120, 20))
        self.cb_time.setText("Фильтр по времени")
        self.cb_prot = QCheckBox(self.tab)
        self.cb_prot.setGeometry(QRect(20, 130, 140, 20))
        self.cb_prot.setText("Фильтр по протоколам")
        self.cb_addr = QCheckBox(self.tab)
        self.cb_addr.setGeometry(QRect(360, 290, 130, 20))
        self.cb_addr.setText("Фильтр по IP-адресам")

        self.dt_beg = QDateTimeEdit(self.tab)
        self.dt_beg.setGeometry(QRect(360, 210, 150, 20))
        self.dt_beg.setDateTime(QDateTime.currentDateTime())
        self.dt_beg.setDisplayFormat("dd.MM.yyyy H:mm:ss.zzz")
        self.dt_beg.setCalendarPopup(True)
        self.dt_beg.setToolTip('Выбрать начальное время (>=)')
        self.dt_beg.setEnabled(False)

        self.dt_end = QDateTimeEdit(self.tab)
        self.dt_end.setGeometry(QRect(520, 210, 150, 20))
        self.dt_end.setDateTime(QDateTime.currentDateTime())
        self.dt_end.setDisplayFormat("dd.MM.yyyy H:mm:ss.zzz")
        self.dt_end.setCalendarPopup(True)
        self.dt_end.setToolTip('Выбрать конечное время (<)')
        self.dt_end.setEnabled(False)

        self.dt_beg.dateChanged.connect(lambda dc: self.date_changed(1))
        self.dt_end.dateChanged.connect(lambda dc: self.date_changed(2))

        #self.l_input_dir = QLabel(self.tab)
        #self.l_input_dir.setGeometry(QRect(102, 50, 180, 15))
        #self.l_input_dir.setText("Выберите директорию с файлами")
        #self.l_or = QLabel(self.tab)
        #self.l_or.setGeometry(QRect(340, 50, 21, 16))
        #self.l_or.setText("ИЛИ")
        self.l_input_file = QLabel(self.tab)
        self.l_input_file.setGeometry(QRect(300, 50, 90, 15))
        self.l_input_file.setText("Выберите файлы")
        self.l_transpr = QLabel(self.tab)
        self.l_transpr.setGeometry(QRect(50, 190, 180, 16))
        self.l_transpr.setEnabled(False)
        self.l_transpr.setText("Протоколы Транспортного уровня")
        self.l_netpr = QLabel(self.tab)
        self.l_netpr.setGeometry(QRect(50, 290, 180, 16))
        self.l_netpr.setEnabled(False)
        self.l_netpr.setText("Протоколы Сетевого уровня")
        self.l_beg = QLabel(self.tab)
        self.l_beg.setGeometry(QRect(390, 190, 60, 16))
        self.l_beg.setEnabled(False)
        self.l_beg.setText("Начиная с..")
        self.l_end = QLabel(self.tab)
        self.l_end.setGeometry(QRect(560, 190, 80, 16))
        self.l_end.setEnabled(False)
        self.l_end.setText("Оканчивая до..")
        self.l_name = QLabel(self.tab)
        self.l_name.setGeometry(QRect(300, 450, 96, 16))
        self.l_name.setText("Как назвать файл?")
        self.l_filt = QLabel(self.tab)
        self.l_filt.setGeometry(QRect(300, 10, 91, 16))
        self.l_filt.setText("Выборка пакетов")

        self.line = QFrame(self.tab)
        self.line.setGeometry(QRect(0, 110, 690, 15))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self.tab)
        self.line_2.setGeometry(QRect(340, 120, 15, 300))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_3 = QFrame(self.tab)
        self.line_3.setGeometry(QRect(0, 420, 690, 15))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        #self.le_dir = QLineEdit(self.tab)
        #self.le_dir.setGeometry(QRect(110, 80, 211, 20))
        #self.le_dir.setEnabled(False)
        #self.le_dir.setReadOnly(True)
        self.le_file = QLineEdit(self.tab)
        self.le_file.setGeometry(QRect(250, 80, 211, 20))
        #self.le_file.setEnabled(False)
        self.le_file.setReadOnly(True)
        self.le_name = QLineEdit(self.tab)
        self.le_name.setGeometry(QRect(250, 480, 231, 20))

        self.pt_transpr = QPlainTextEdit(self.tab)
        self.pt_transpr.setGeometry(QRect(50, 210, 271, 71))
        self.pt_transpr.setEnabled(False)
        self.pt_transpr.setReadOnly(True)
        self.pt_netpr = QPlainTextEdit(self.tab)
        self.pt_netpr.setGeometry(QRect(50, 320, 271, 71))
        self.pt_netpr.setEnabled(False)
        self.pt_netpr.setReadOnly(True)

        self.pt_addr = QPlainTextEdit(self.tab)
        self.pt_addr.setGeometry(QRect(390, 320, 271, 71))
        self.pt_addr.setEnabled(False)
        self.pt_log = QPlainTextEdit(self.tab)
        self.pt_log.setGeometry(QRect(20, 610, 651, 101))
        self.pt_log.setReadOnly(True)

        self.progressBar = QProgressBar(self.tab)
        self.progressBar.setGeometry(QRect(20, 580, 651, 20))
        self.progressBar.setFormat("%v" + "%")
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        #self.pb_dir = QPushButton(self.tab)
        #self.pb_dir.setGeometry(QRect(80, 80, 21, 20))
        #self.pb_dir.setIcon(QIcon('допочки\_folder.png'))
        #self.pb_dir.clicked.connect(lambda gd: self.get_directory(1))
        self.pb_file = QPushButton(self.tab)
        self.pb_file.setGeometry(QRect(220, 80, 21, 20))
        self.pb_file.setIcon(QIcon('допочки\_folder.png'))
        self.pb_file.clicked.connect(lambda gf: self.get_files(1))
        self.pb_time = QPushButton(self.tab)
        self.pb_time.setGeometry(QRect(480, 240, 71, 20))
        self.pb_time.setToolTip('Добавить ещё временной отрезок')
        self.pb_time.setEnabled(False)
        self.pb_time.setText("Ещё!")

        self.pb_transpr = QPushButton(self.tab)
        self.pb_transpr.setGeometry(QRect(20, 210, 21, 20))
        self.pb_transpr.setToolTip('Выбрать протоколы Транспортного уровня')
        self.pb_transpr.setIcon(QIcon('допочки\_blank.png'))
        self.pb_transpr.setEnabled(False)
        self.pb_transpr.clicked.connect(self.TransProt_list.exec)

        self.pb_netpr = QPushButton(self.tab)
        self.pb_netpr.setGeometry(QRect(20, 320, 21, 20))
        self.pb_netpr.setToolTip('Выбрать протоколы Сетевого уровня')
        self.pb_netpr.setIcon(QIcon('допочки\_blank.png'))
        self.pb_netpr.setEnabled(False)
        self.pb_netpr.clicked.connect(self.NetProt_list.exec)
        self.pb_addr = QPushButton(self.tab)
        self.pb_addr.setGeometry(QRect(530, 290, 132, 20))
        self.pb_addr.setText('Редактировать список')
        self.pb_addr.setEnabled(False)
        self.pb_addr.clicked.connect(self.IP_list.exec)
        self.pb_name = QPushButton(self.tab)
        self.pb_name.setGeometry(QRect(220, 480, 21, 20))
        self.pb_name.setIcon(QIcon('допочки\_folder.png'))
        self.pb_name.clicked.connect(lambda ed: self.extract_to_directory(1))
        self.pb_start = QPushButton(self.tab)
        self.pb_start.setGeometry(QRect(220, 510, 261, 41))
        self.pb_start.setText("Начать выборку")
        self.pb_start.clicked.connect(self.do_it_motherFucker)

        #self.radiobutton = QRadioButton(self.tab)
        #self.radiobutton.setGeometry(QRect(84, 48, 20, 20))
        #self.radiobutton_2 = QRadioButton(self.tab)
        #self.radiobutton_2.setGeometry(QRect(424, 48, 20, 20))

        #self.radiobutton.raise_()
        #self.radiobutton_2.raise_()
        self.cb_time.raise_()
        self.cb_prot.raise_()
        self.cb_addr.raise_()
        self.dt_beg.raise_()
        self.dt_end.raise_()
        #self.l_input_dir.raise_()
        #self.l_or.raise_()
        self.l_input_file.raise_()
        self.l_transpr.raise_()
        self.l_netpr.raise_()
        self.l_beg.raise_()
        self.l_end.raise_()
        self.l_name.raise_()
        self.l_filt.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        #self.le_dir.raise_()
        self.le_file.raise_()
        self.le_name.raise_()
        self.pt_transpr.raise_()
        self.pt_netpr.raise_()
        self.pt_addr.raise_()
        self.pt_log.raise_()
        self.progressBar.raise_()
        #self.pb_dir.raise_()
        self.pb_file.raise_()
        self.pb_time.raise_()
        self.pb_transpr.raise_()
        self.pb_netpr.raise_()
        self.pb_addr.raise_()
        self.pb_name.raise_()
        self.pb_start.raise_()
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.tabWidget.addTab(self.tab, "")

        self.cb_time.clicked['bool'].connect(self.dt_beg.setEnabled)
        self.cb_time.clicked['bool'].connect(self.dt_end.setEnabled)
        self.cb_time.clicked['bool'].connect(self.l_beg.setEnabled)
        self.cb_time.clicked['bool'].connect(self.l_end.setEnabled)
        self.cb_prot.clicked['bool'].connect(self.l_transpr.setEnabled)
        self.cb_prot.clicked['bool'].connect(self.l_netpr.setEnabled)
        self.cb_prot.clicked['bool'].connect(self.pt_transpr.setEnabled)
        self.cb_prot.clicked['bool'].connect(self.pt_netpr.setEnabled)
        self.cb_prot.clicked['bool'].connect(self.pb_transpr.setEnabled)
        self.cb_prot.clicked['bool'].connect(self.pb_netpr.setEnabled)
        self.cb_addr.clicked['bool'].connect(self.pt_addr.setEnabled)
        self.cb_addr.clicked['bool'].connect(self.pb_addr.setEnabled)



        #####------------------------------2_TAB



        self.tab_2 = QWidget()
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), ("II работа с файлами"))

        self.l_merge = QLabel(self.tab_2)
        self.l_merge.setGeometry(QRect(300, 10, 180, 16))
        self.l_merge.setText("Объединение файлов")

        self.l_arch = QLabel(self.tab_2)
        self.l_arch.setGeometry(QRect(300, 250, 180, 16))
        self.l_arch.setText("Архивирование файлов")

        #self.radiobutton_3 = QRadioButton(self.tab_2)
        #self.radiobutton_3.setGeometry(QRect(84, 48, 20, 20))
        #self.radiobutton_4 = QRadioButton(self.tab_2)
        #self.radiobutton_4.setGeometry(QRect(424, 48, 20, 20))

        #self.l_input_dir2 = QLabel(self.tab_2)
        #self.l_input_dir2.setGeometry(QRect(102, 50, 180, 15))
        #self.l_input_dir2.setText("Выберите директорию с файлами")
        #self.l_or2 = QLabel(self.tab_2)
        #self.l_or2.setGeometry(QRect(340, 50, 21, 16))
        #self.l_or2.setText("ИЛИ")
        self.l_input_file2 = QLabel(self.tab_2)
        self.l_input_file2.setGeometry(QRect(102, 50, 180, 15))#442, 50, 90, 15))
        self.l_input_file2.setText("Выберите файлы")
        self.l_name2 = QLabel(self.tab_2)
        self.l_name2.setGeometry(QRect(442, 50, 180, 15))#280, 140, 180, 16))
        self.l_name2.setText("Куда сохранить результат?")
        self.l_ciph2 = QLabel(self.tab_2)
        self.l_ciph2.setGeometry(QRect(84, 298, 180, 15))
        self.l_ciph2.setText("Убрать шифрованный трафик")
        self.l_arch2 = QLabel(self.tab_2)
        self.l_arch2.setGeometry(QRect(424, 298, 180, 15))
        self.l_arch2.setText("Заархивировать файлы")


        #self.le_dir2 = QLineEdit(self.tab_2)
        #self.le_dir2.setGeometry(QRect(110, 80, 211, 20))
        #self.le_dir2.setEnabled(False)
        self.le_file2 = QLineEdit(self.tab_2)
        self.le_file2.setGeometry(QRect(110, 80, 211, 20))#450, 80, 211, 20))
        self.le_file2.setReadOnly(True)
        self.le_name2 = QLineEdit(self.tab_2)
        self.le_name2.setGeometry(QRect(450, 80, 211, 20))#260, 170, 180, 20))

        #self.pb_dir2 = QPushButton(self.tab_2)
        #self.pb_dir2.setGeometry(QRect(80, 80, 21, 20))
        #self.pb_dir2.setIcon(QIcon('допочки\_folder.png'))
        #self.pb_dir2.clicked.connect(lambda gd: self.get_directory(2))
        self.pb_file2 = QPushButton(self.tab_2)
        self.pb_file2.setGeometry(QRect(80, 80, 21, 20))#420, 80, 21, 20))
        self.pb_file2.setIcon(QIcon('допочки\_folder.png'))
        self.pb_file2.clicked.connect(lambda gf: self.get_files(2))
        self.pb_name2 = QPushButton(self.tab_2)
        self.pb_name2.setGeometry(QRect(420, 80, 21, 20))#230, 170, 21, 20))
        self.pb_name2.setIcon(QIcon('допочки\_folder.png'))
        self.pb_name2.clicked.connect(lambda ed: self.extract_to_directory(2))
        self.pb_merge = QPushButton(self.tab_2)
        self.pb_merge.setGeometry(QRect(270, 170, 160, 20))
        self.pb_merge.setText("Объединить")
        self.pb_merge.clicked.connect(self.merge_it_motherFucker)

        self.line_4 = QFrame(self.tab_2)
        self.line_4.setGeometry(QRect(0, 280, 690, 15))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_5 = QFrame(self.tab_2)
        self.line_5.setGeometry(QRect(0, 580, 690, 15))
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.pt_log2 = QPlainTextEdit(self.tab_2)
        self.pt_log2.setGeometry(QRect(20, 610, 651, 101))
        self.pt_log2.setReadOnly(True)

        self.graphicsView = QGraphicsView(self.tab_2)
        self.graphicsView.setGeometry(QRect(0, 330, 714, 277))
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.scene.addPixmap(QPixmap('допочки\_in_working_3.png'))

        self.l_merge.raise_()
        self.l_arch.raise_()
        #self.l_input_dir2.raise_()
        #self.l_or2.raise_()
        self.l_input_file2.raise_()
        self.l_name2.raise_()
        #self.radiobutton_3.raise_()
        #self.radiobutton_4.raise_()
        #self.pb_dir2.raise_()
        self.pb_file2.raise_()
        self.pb_name2.raise_()
        #self.le_dir2.raise_()
        self.le_file2.raise_()
        self.le_name2.raise_()
        self.line_4.raise_()
        self.line_5.raise_()
        self.pt_log2.raise_()



        #####------------------------------2_TAB

        #####------------------------------3_TAB

        self.tab_3 = QWidget()
        self.tabWidget.addTab(self.tab_3, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), ("III Проверка на аномальную активность"))
        self.tab_3.setEnabled(False)

        self.l_filt3 = QLabel(self.tab_3)
        self.l_filt3.setGeometry(QRect(300, 10, 91, 16))
        self.l_filt3.setText("Выборка пакетов")

        self.l_input_file3 = QLabel(self.tab_3)
        self.l_input_file3.setGeometry(QRect(300, 50, 90, 15))
        self.l_input_file3.setText("Выберите файлы")

        self.pb_file3 = QPushButton(self.tab_3)
        self.pb_file3.setGeometry(QRect(220, 80, 21, 20))
        self.pb_file3.setIcon(QIcon('допочки\_folder.png'))
        self.pb_file3.clicked.connect(lambda gf: self.get_files(3))

        self.le_file3 = QLineEdit(self.tab_3)
        self.le_file3.setGeometry(QRect(250, 80, 211, 20))
        self.le_file3.setReadOnly(True)

        self.pb_graphy = QPushButton(self.tab_3)
        self.pb_graphy.setGeometry(QRect(270, 170, 160, 20))
        self.pb_graphy.setText("Построить граф")
        #self.pb_graphy.clicked.connect(self.graph_it)

        #self.label_6 = QLabel(self.tab_3)
        #self.pixmap = QPixmap('допочки\_in_working_1.png')
        #self.label_6.setPixmap(self.pixmap)

        self.l_filt3.raise_()
        self.l_input_file3.raise_()
        self.pb_file3.raise_()
        self.le_file3.raise_()


        #####------------------------------3_TAB

        #####----------------------------IN_WORK



        self.tab_4 = QWidget()
        self.tabWidget.addTab(self.tab_4, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), ("...IV visualization..."))
        self.tab_4.setEnabled(False)


        self.label_7 = QLabel(self.tab_4)
        self.pixmap_2 = QPixmap('допочки\_in_working_2.png')
        self.label_7.setPixmap(self.pixmap_2)

        #####----------------------------IN_WORK





        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), ("I выборка пакетов"))
        QMetaObject.connectSlotsByName(self)

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Ща закроется всё', "Ты чо, реально хочешь выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def to_center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())


    def get_directory(self, gd):
        if gd == 1:
            result = QFileDialog.getExistingDirectory()
            #self.le_dir.setText(result)
            self.le_file.setDisabled(True)
            #self.le_dir.setEnabled(True)
            #self.radiobutton_2.setChecked(False)
            #self.radiobutton.setChecked(True)
        else:
            result = QFileDialog.getExistingDirectory()
            #self.le_dir2.setText(result)
            self.le_file2.setDisabled(True)
            #self.le_dir2.setEnabled(True)
            #self.radiobutton_4.setChecked(False)
            #self.radiobutton_3.setChecked(True)

    def get_files(self, gf):
        if gf == 1:
            result, bullshit = QFileDialog.getOpenFileNames(self, "Выберите pcap-файлы", getcwd(), "files (*.pcap *.pcapng)")
            #self.le_dir.setDisabled(True)
            self.le_file.setEnabled(True)
            #self.radiobutton.setChecked(False)
            #self.radiobutton_2.setChecked(True)
            if len(result):
                self.le_file.setText(", ".join(result))
        elif gf == 3:
            result, bullshit = QFileDialog.getOpenFileNames(self, "Выберите pcap-файлы", getcwd(), "files (*.pcap *.pcapng)")
            #self.le_dir.setDisabled(True)
            self.le_file3.setEnabled(True)
            #self.radiobutton.setChecked(False)
            #self.radiobutton_2.setChecked(True)
            if len(result):
                self.le_file3.setText(", ".join(result))
        else:
            result, bullshit = QFileDialog.getOpenFileNames(self, "Выберите pcap-файлы", getcwd(), "files (*.pcap *.pcapng)")
            #self.le_dir2.setDisabled(True)
            self.le_file2.setEnabled(True)
            #self.radiobutton_3.setChecked(False)
            #self.radiobutton_4.setChecked(True)
            if len(result):
                self.le_file2.setText(", ".join(result))

    def date_changed(self, dc):
        if dc == 1:
            self.dt_end.setMinimumDateTime(QDateTime(self.dt_beg.dateTime()))
        else:
            self.dt_beg.setMaximumDateTime(QDateTime(self.dt_end.dateTime()))

    def extract_to_directory(self, ed):
        if ed == 1:
            result, bullshit =QFileDialog.getSaveFileName(self, "Сохранить файл", getcwd(), "files (*.pcap *.pcapng)")
            self.le_name.setText(result)
        else:
            result, bullshit =QFileDialog.getSaveFileName(self, "Сохранить файл", getcwd(), "files (*.pcap *.pcapng)")
            self.le_name2.setText(result)


    def do_it_motherFucker(self):
        if self.filtering_is_on == 0:
            #if ((not self.radiobutton.isChecked() and not self.radiobutton_2.isChecked())\
            #    or (self.radiobutton.isChecked() and self.le_dir.text() == '')\
            #        or (self.radiobutton_2.isChecked() and self.le_file.text() == ''))\
            #            and self.le_name.text() == '':
            if self.le_file.text() == '' and self.le_name.text() == '':
                self.pt_log.appendPlainText("  " + "Какие файлы обработать? Куда сохранить? Такая неопределённость..")
            #elif (not self.radiobutton.isChecked() and not self.radiobutton_2.isChecked()) or (self.radiobutton.isChecked() and self.le_dir.text() == '') or (self.radiobutton_2.isChecked() and self.le_file.text() == ''):
            elif self.le_file.text() == '':
                self.pt_log.appendPlainText("  " + "Какие файлы обработать?")
            elif self.le_name.text() == '':
                self.pt_log.appendPlainText("  " + "Куда сохранить?")
            else:
                self.filtering_is_on = 1  # эти пиздецы в идеале нужно заменить на что-нибудь адекватное
                self.count_for_pr_b = 0 # эти пиздецы в идеале нужно заменить на что-нибудь адекватное
                self.progressBar.setValue(0)
                self.pb_start.setText("Остановить выборку")

                #my_directory = self.le_dir.text()
                pcap_files_in = self.le_file.text()
                pcap_file_out = self.le_name.text()
                per_quest = 0
                per_beg = ''
                per_end = ''
                prot_quest = 0
                net_prot = 0
                trans_prot = 0
                appl_prot = 0 ##
                ip_quest = 0
                netprot_mass = []
                transprot_mass = []
                addr_mass = []

                if (pcap_file_out.endswith(".pcap") or pcap_file_out.endswith(".pcapng")) == False:
                    pcap_file_out = pcap_file_out + ".pcap"

                self.pt_log.appendPlainText("Сохранить в:")
                self.pt_log.appendPlainText("  " + pcap_file_out)

                #if self.radiobutton.isChecked():
                #    onlyfiles = [my_directory + '/' + f for f in listdir(my_directory) if
                #                 f.endswith(".pcap") or f.endswith(".pcapng") and isfile(join(my_directory, f))]
                #    self.for_pr_b = len(onlyfiles)
#
                #    self.pt_log.appendPlainText("Выбрана директория:")
                #    self.pt_log.appendPlainText("  " + self.le_dir.text())
                #    self.pt_log.appendPlainText("С pcap-файлами:")
                #    for file in onlyfiles:
                #        bullshit, fname = file.rsplit('/', 1)
                #        self.pt_log.appendPlainText("  " + fname)

                #elif self.radiobutton_2.isChecked():
                onlyfiles = pcap_files_in.split(', ')
                self.for_pr_b = len(onlyfiles)

                self.pt_log.appendPlainText("Выбраны pcap-файлы:")
                for file in onlyfiles:
                    self.pt_log.appendPlainText("  " + (file))

                if self.cb_addr.isChecked() and self.pt_addr.toPlainText() != '':
                    ip_quest = 1
                    addr_mass = self.pt_addr.toPlainText().splitlines()

                if self.cb_time.isChecked():
                    per_quest = 1
                    per_beg = self.dt_beg.dateTime()
                    per_end = self.dt_end.dateTime()

                if self.cb_prot.isChecked():
                    prot_quest = 1
                    transprot_mass = self.transprot_mass
                    netprot_mass = self.netprot_mass

                if self.pt_transpr.toPlainText() != '':
                    trans_prot = 1
                if self.pt_netpr.toPlainText() != '':
                    net_prot = 1

                #self.radiobutton.setDisabled(True)
                #self.radiobutton_2.setDisabled(True)
                #self.l_input_dir.setDisabled(True)
                #self.l_or.setDisabled(True)
                self.l_input_file.setDisabled(True)
                #self.pb_dir.setDisabled(True)
                self.pb_file.setDisabled(True)
                #self.le_dir.setDisabled(True)
                self.le_file.setDisabled(True)
                self.cb_time.setDisabled(True)
                self.cb_prot.setDisabled(True)
                self.cb_addr.setDisabled(True)
                self.l_transpr.setDisabled(True)
                self.l_netpr.setDisabled(True)
                self.l_beg.setDisabled(True)
                self.l_end.setDisabled(True)
                self.l_name.setDisabled(True)
                self.l_filt.setDisabled(True)
                self.le_name.setDisabled(True)
                self.dt_beg.setDisabled(True)
                self.dt_end.setDisabled(True)
                self.pt_transpr.setDisabled(True)
                self.pt_netpr.setDisabled(True)
                self.pt_addr.setDisabled(True)
                self.pb_time.setDisabled(True)
                self.pb_transpr.setDisabled(True)
                self.pb_netpr.setDisabled(True)
                self.pb_addr.setDisabled(True)
                self.pb_name.setDisabled(True)

                self.worker = WorkerThread(onlyfiles, pcap_file_out, per_quest, per_beg, per_end, prot_quest, net_prot,
                                           netprot_mass, trans_prot, transprot_mass, appl_prot, ip_quest, addr_mass)
                self.worker.callback_received.connect(self.append_to_log)
                self.worker.start()
                self.pt_log.appendPlainText("")
                self.pt_log.appendPlainText("В работе:")
        elif self.filtering_is_on == 1:
            self.worker.terminate()
            self.pt_log.appendPlainText("")
            self.pt_log.appendPlainText("Работа прервана")
            self.pt_log.appendPlainText("")
            self.pt_log.appendPlainText("")
            self.go_to_starting_set()

    def append_to_log(self, x):
        self.count_for_pr_b += 1
        self.pt_log.appendPlainText("")
        self.pt_log.appendPlainText(x)
        self.progressBar.setValue(self.count_for_pr_b * 100 / (self.for_pr_b + 1))

        if self.progressBar.value() == 100:
            self.pt_log.appendPlainText("")
            self.pt_log.appendPlainText("")
            self.go_to_starting_set()

    def go_to_starting_set(self):
        self.filtering_is_on = 0
        self.pb_start.setText("Начать выборку")

        #self.radiobutton.setDisabled(False)
        #self.radiobutton_2.setDisabled(False)
        #self.l_input_dir.setDisabled(False)
        #self.l_or.setDisabled(False)
        self.l_input_file.setDisabled(False)
        #self.pb_dir.setDisabled(False)
        self.pb_file.setDisabled(False)
        #self.le_dir.setDisabled(False)
        self.le_file.setDisabled(False)
        self.cb_time.setDisabled(False)
        self.cb_prot.setDisabled(False)
        self.cb_addr.setDisabled(False)
        self.l_name.setDisabled(False)
        self.l_filt.setDisabled(False)
        self.le_name.setDisabled(False)
        self.pb_name.setDisabled(False)

        if self.cb_time.isChecked():
            self.dt_beg.setEnabled(True)
            self.dt_end.setEnabled(True)
            self.l_beg.setEnabled(True)
            self.l_end.setEnabled(True)

        if self.cb_prot.isChecked():
            self.l_transpr.setEnabled(True)
            self.l_netpr.setEnabled(True)
            self.pt_transpr.setEnabled(True)
            self.pt_netpr.setEnabled(True)
            self.pb_transpr.setEnabled(True)
            self.pb_netpr.setEnabled(True)

        if self.cb_addr.isChecked():
            self.pt_addr.setEnabled(True)
            self.pb_addr.setEnabled(True)

    def merge_it_motherFucker(self):
        #if self.radiobutton_3.isChecked():
        #    self.pt_log2.appendPlainText("Выбрана директория с pcap-файлами:")
        #    self.pt_log2.appendPlainText("  " + self.le_dir2.text())
        #    self.pt_log2.appendPlainText('Просматриваем "{}"...'.format(self.le_dir2.text()))
        #    onlyfiles = [self.le_dir2.text() + '/' + f for f in listdir(self.le_dir2.text()) if
        #                 f.endswith(".pcap") or f.endswith(".pcapng") and isfile(join(self.le_dir2.text(), f))]
        #    self.pt_log2.appendPlainText(str(onlyfiles))

        #elif self.radiobutton_4.isChecked():
        self.pt_log2.appendPlainText("Выбраны pcap-файлы:")
        self.pt_log2.appendPlainText("  " + self.le_file2.text())
        onlyfiles = self.le_file2.text().split(', ')
        self.pt_log2.appendPlainText('Работаем с "{}"...'.format(onlyfiles))

        merge_file_out = self.le_name2.text()
        if (merge_file_out.endswith(".pcap") or merge_file_out.endswith(".pcapng")) == False:
            merge_file_out = merge_file_out + ".pcap"

        self.pt_log2.appendPlainText("Сохранить в:")
        self.pt_log2.appendPlainText("  " + merge_file_out)
        self.pt_log2.appendPlainText("")

        merge.mergecap(onlyfiles, merge_file_out)

    #def graph_it(self):
    #    onlyfiles = self.le_file3.text().split(', ')
    #    graphy.graph_it(onlyfiles)


class TransProt_list(QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.main = root
        self.setWindowTitle('Список протоколов Транспортного уровня')
        self.resize(900, 900)
        self.layout_tw = QVBoxLayout(self)
        self.layout_b = QHBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setGeometry(QRect(20, 20, 450, 81))
        self.tableWidget.setColumnCount(3)
        hor_header = self.tableWidget.horizontalHeader()
        hor_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hor_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hor_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(1)
        self.layout_tw.addWidget(self.tableWidget)
        self.layout_tw.addLayout(self.layout_b)

        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item.setText("Выбрать")

        item_2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item_2)
        item_2.setText("Код")

        item_3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item_3)
        item_3.setText("Наименование")

        self.tableWidget.verticalHeader().setVisible(False)

        self.tableWidget.horizontalHeader().setFont(QFont('Arial', weight=QFont.UltraExpanded))

        cell_widget = QWidget()
        cb = QCheckBox()
        lay_out = QHBoxLayout(cell_widget)
        lay_out.addWidget(cb)
        lay_out.setAlignment(Qt.AlignCenter)
        lay_out.setContentsMargins(0, 0, 0, 0)
        cell_widget.setLayout(lay_out)
        self.tableWidget.setCellWidget(0, 0, cell_widget)

        ProtFile = open('допочки\PrNmTransCatalog.txt')
        x = 0
        for row in ProtFile:
            tr_cod, tr_pr = row.split("\t")
            vheader = self.tableWidget.verticalHeader()
            vheader.setSectionResizeMode(x, QHeaderView.ResizeToContents)
            self.tableWidget.setItem(x, 1, QTableWidgetItem(tr_cod))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(tr_pr))
            x += 1
            if x == 133:
                continue
            else:
                self.tableWidget.insertRow(x)
                cell_widget = QWidget()
                cb = QCheckBox()
                lay_out = QHBoxLayout(cell_widget)
                lay_out.addWidget(cb)
                lay_out.setAlignment(Qt.AlignCenter)
                lay_out.setContentsMargins(0, 0, 0, 0)
                cell_widget.setLayout(lay_out)
                self.tableWidget.setCellWidget(x, 0, cell_widget)

            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)


        #self.tableWidget.cellWidget(i, 0).findChild(type(QCheckBox())).clicked['bool'].connect(self.tableWidget.clear())
        #self.cb_time.clicked['bool'].connect(self.dt_beg.setEnabled)


    def closeEvent(self, event):
        cnt = 0
        self.main.transprot_mass = []
        self.main.pt_transpr.clear()
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(i, 0).findChild(type(QCheckBox())).checkState() == 2:
                if cnt == 1:
                    self.main.pt_transpr.insertPlainText(",    ")
                self.main.pt_transpr.insertPlainText(self.tableWidget.item(i, 2).text().rstrip())
                self.main.pt_transpr.insertPlainText(" ")
                cnt = 1
                self.main.transprot_mass.append(int(self.tableWidget.item(i, 1).text()))
        self.close()


class NetProt_list(QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.main = root
        self.setWindowTitle('Список протоколов Сетевого уровня')
        self.resize(900, 900)
        self.layout_tw = QVBoxLayout(self)

        self.layout_b = QHBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setGeometry(QRect(20, 20, 450, 81))
        self.tableWidget.setColumnCount(4)
        hor_header = self.tableWidget.horizontalHeader()
        hor_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hor_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hor_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hor_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(1)
        self.layout_tw.addWidget(self.tableWidget)
        self.layout_tw.addLayout(self.layout_b)

        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item.setText("Выбрать")

        item_2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item_2)
        item_2.setText("Hex Код")

        item_3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item_3)
        item_3.setText("Dec Код")

        item_4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item_4)
        item_4.setText("Наименование")

        self.tableWidget.verticalHeader().setVisible(False)

        self.tableWidget.horizontalHeader().setFont(QFont('Arial', weight=QFont.UltraExpanded))

        cell_widget = QWidget()
        cb = QCheckBox()
        lay_out = QHBoxLayout(cell_widget)
        lay_out.addWidget(cb)
        lay_out.setAlignment(Qt.AlignCenter)
        lay_out.setContentsMargins(0, 0, 0, 0)
        cell_widget.setLayout(lay_out)
        self.tableWidget.setCellWidget(0, 0, cell_widget)

        ProtFile = open('допочки\PrNmNetCatalog.txt')
        x = 0
        for row in ProtFile:
            net_hcod, net_dcod, net_pr = row.split("\t")
            vheader = self.tableWidget.verticalHeader()
            vheader.setSectionResizeMode(x, QHeaderView.ResizeToContents)
            self.tableWidget.setItem(x, 1, QTableWidgetItem(net_hcod))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(net_dcod))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(net_pr))
            x += 1
            if x == 53:
                continue
            else:
                self.tableWidget.insertRow(x)
                cell_widget = QWidget()
                cb = QCheckBox()
                lay_out = QHBoxLayout(cell_widget)
                lay_out.addWidget(cb)
                lay_out.setAlignment(Qt.AlignCenter)
                lay_out.setContentsMargins(0, 0, 0, 0)
                cell_widget.setLayout(lay_out)
                self.tableWidget.setCellWidget(x, 0, cell_widget)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def closeEvent(self, event):
        cnt = 0
        self.main.netprot_mass = []
        self.main.pt_netpr.clear()
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(i, 0).findChild(type(QCheckBox())).checkState() == 2:
                if cnt == 1:
                    self.main.pt_netpr.insertPlainText(",    ")
                self.main.pt_netpr.insertPlainText(self.tableWidget.item(i, 3).text().rstrip())
                self.main.pt_netpr.insertPlainText(" ")
                cnt = 1
                self.main.netprot_mass.append(int(self.tableWidget.item(i, 2).text()))
        self.close()


class IP_list(QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.main = root

        self.setWindowTitle('Список IP')
        self.setFixedWidth(504)
        self.layout_tw = QVBoxLayout(self)

        self.layout_b = QHBoxLayout()
        self.layout_b.addItem(QSpacerItem(150, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setGeometry(QRect(20, 20, 464, 81))
        self.tableWidget.setColumnCount(4)

        hor_header = self.tableWidget.horizontalHeader()
        hor_header.setSectionResizeMode(0, QHeaderView.Stretch)
        hor_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hor_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hor_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.layout_tw.addWidget(self.tableWidget)
        self.layout_tw.addLayout(self.layout_b)

        self.pb_cle = QPushButton(self)
        self.pb_cle.setGeometry(QRect(0, 490, 21, 20))
        self.pb_cle.setToolTip('Очистить  таблицу')
        self.pb_cle.setIcon(QIcon('допочки\_broom.png'))
        self.pb_cle.clicked.connect(self.del_all)
        self.layout_b.addWidget(self.pb_cle)

        self.pb_row_add = QPushButton(self)
        self.pb_row_add.setGeometry(QRect(20, 490, 21, 20))
        self.pb_row_add.setToolTip('Добавить строчку')
        self.pb_row_add.setIcon(QIcon('допочки\_+.png'))
        self.pb_row_add.clicked.connect(self.row_add)
        self.layout_b.addWidget(self.pb_row_add)

        self.pb_row_rem = QPushButton(self)
        self.pb_row_rem.setGeometry(QRect(50, 490, 21, 20))
        self.pb_row_rem.setToolTip('Убрать строчку')
        self.pb_row_rem.setIcon(QIcon('допочки\_-.png'))
        self.pb_row_rem.clicked.connect(self.row_rem)
        self.layout_b.addWidget(self.pb_row_rem)

        self.pb_ip = QPushButton(self)
        self.pb_ip.setGeometry(QRect(430, 490, 21, 20))
        self.pb_ip.setToolTip('Загрузить из файла')
        self.pb_ip.setIcon(QIcon('допочки\_ip.png'))
        self.pb_ip.clicked.connect(self.get_IPs)
        self.layout_b.addWidget(self.pb_ip)

        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item.setText("IP адрес")

        item_2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item_2)
        item_2.setText("Порт")

        item_3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item_3)
        item_3.setText("Относится к")

        item_4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item_4)
        item_4.setText("Проверка")

        self.tableWidget.cellChanged.connect(self.onCellChanged)


    def del_all(self):
        self.tableWidget.setRowCount(0)

    def row_add(self):
        i = self.tableWidget.rowCount()
        self.tableWidget.insertRow(i)
        vheader = self.tableWidget.verticalHeader()
        vheader.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        combobox = QComboBox()
        combobox.addItem("Any")
        combobox.addItem("Source")
        combobox.addItem("Destination")
        self.tableWidget.setCellWidget(i, 2, combobox)

        item = QTableWidgetItem()
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.Dense4Pattern)
        self.tableWidget.setItem(i, 3, item)
        item.setFlags(Qt.ItemIsEnabled)
        item.setBackground(brush)

    def row_rem(self):
        cell = self.tableWidget.currentRow()
        self.tableWidget.removeRow(cell)

    def get_IPs(self):
        result, bullshit = QFileDialog.getOpenFileName(self, "Выберите txt/csv-файл", getcwd(), "files (*.txt; *.csv)")
        # нельзя нажимать на крест
        with open(str(result), "r") as fileInput:
            x = self.tableWidget.rowCount()
            for row in fileInput:
                if result.endswith("txt"):
                    if ":" not in row:
                        (ip, port) = (row.rstrip(), '')
                    else:
                        (ip, port) = row.split(":")
                        port = port.rstrip()

                elif result.endswith("csv"):
                    if ";" not in row:
                        (ip, port) = (row.rstrip(), '')
                    else:
                        (ip, port) = row.split(";")
                        port = port.rstrip()

                self.tableWidget.insertRow(x)
                vheader = self.tableWidget.verticalHeader()
                vheader.setSectionResizeMode(x, QHeaderView.ResizeToContents)
                self.tableWidget.setItem(x, 0, QTableWidgetItem(ip))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(port))
                combobox = QComboBox()
                combobox.addItem("Any")
                combobox.addItem("Source")
                combobox.addItem("Destination")
                self.tableWidget.setCellWidget(x, 2, combobox)
                x += 1

    def closeEvent(self, event):
        self.main.pt_addr.clear()
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 3)
            if item is not None and item.background().color().name() == '#00ff00':
                self.main.pt_addr.appendPlainText("")
                for y in range(2):
                    if self.tableWidget.item(i, y) is not None:
                        self.main.pt_addr.insertPlainText(self.tableWidget.item(i, y).text())
                    else:
                        self.main.pt_addr.insertPlainText("")
                    if y < 2:
                        self.main.pt_addr.insertPlainText(":")


                if self.tableWidget.cellWidget(i, 2).currentText() == "Any":
                    self.main.pt_addr.insertPlainText("A")
                elif self.tableWidget.cellWidget(i, 2).currentText() == "Source":
                    self.main.pt_addr.insertPlainText("S")
                else:
                    self.main.pt_addr.insertPlainText("D")

        self.close()

    def onCellChanged(self, row, column):
        if column in (0, 1):
            item1 = self.tableWidget.item(row, 0)
            if item1 is not None:
                item1 = item1.text().replace(' ', '')
                try:
                    ipaddress.ip_address(item1)
                except ValueError:
                    if item1 == '':
                        col0 = 2
                    else:
                        col0 = 0
                else:
                    col0 = 1
            else:
                col0 = 2

            item2 = self.tableWidget.item(row, 1)
            if item2 is not None:
                item2 = item2.text().replace(' ', '')
                if item2.isnumeric() and int(item2) <= 65535:
                    col1 = 1
                elif item2 == '':
                    col1 = 2
                else:
                    col1 = 0
            else:
                col1 = 2

            if (col0 == 0 and col1 == 0)\
                    or (col0 == 2 and col1 == 2):
                backgr = QTableWidgetItem()
                brush = QBrush(QColor(255, 0, 0))
                brush.setStyle(Qt.SolidPattern)
                backgr.setBackground(brush)
                item = QTableWidgetItem()
                self.tableWidget.setItem(row, 3, item)
                item.setFlags(Qt.ItemIsEnabled)
                item.setBackground(brush)

            if (col0 == 0 and (col1 == 1 or col1 == 2))\
                    or (col1 == 0 and (col0 == 1 or col0 == 2)):
                backgr = QTableWidgetItem()
                brush = QBrush(QColor(255, 127, 0))
                brush.setStyle(Qt.SolidPattern)
                backgr.setBackground(brush)
                item = QTableWidgetItem()
                self.tableWidget.setItem(row, 3, item)
                item.setFlags(Qt.ItemIsEnabled)
                item.setBackground(brush)

            if (col0 == 1 and (col1 == 1 or col1 == 2))\
                    or (col1 == 1 and (col0 == 1 or col0 == 2)):
                backgr = QTableWidgetItem()
                brush = QBrush(QColor(0, 255, 0))
                brush.setStyle(Qt.SolidPattern)
                backgr.setBackground(brush)
                item = QTableWidgetItem()
                self.tableWidget.setItem(row, 3, item)
                item.setFlags(Qt.ItemIsEnabled)
                item.setBackground(brush)
        else:
            pass


class WorkerThread(QThread):
    callback_received = pyqtSignal(object)

    def __init__(self, onlyfiles, pcap_file_out, per_quest, per_beg, per_end, prot_quest, net_prot, netprot_mass,
                 trans_prot, transprot_mass, appl_prot, ip_quest, addr_mass):
        QThread.__init__(self)
        self.onlyfiles = onlyfiles
        self.pcap_file_out = pcap_file_out
        self.per_quest = per_quest
        self.per_beg = per_beg
        self.per_end = per_end
        self.prot_quest = prot_quest
        self.net_prot = net_prot
        self.netprot_mass = netprot_mass
        self.trans_prot = trans_prot
        self.transprot_mass = transprot_mass
        self.appl_prot = appl_prot
        self.ip_quest = ip_quest
        self.addr_mass = addr_mass

    def run(self):
        the_packet_filter.pickle_pcap(self.onlyfiles, self.pcap_file_out, self.per_quest, self.per_beg, self.per_end,
                                      self.prot_quest, self.net_prot, self.netprot_mass, self.trans_prot, self.transprot_mass,
                                      self.appl_prot, self.ip_quest, self.addr_mass, lambda x: self.callback_received.emit((x)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())