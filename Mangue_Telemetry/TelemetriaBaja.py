from PyQt5.QtSql import QSqlDatabase
from tkinter import *
from struct import unpack
from collections import deque
from colorama import Cursor
import matplotlib.pyplot as plt
import serial
from scipy import signal
import sys
import glob
from PyQt5 import QtCore, QtGui, QtWidgets
import io
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import threading
from threading import *
import time
from PIL import Image
import random
from random import randint
from paho.mqtt import client as mqtt_client
import sqlite3
import json
import pandas as pd

broker = "fe80::b982:1519:74d7:f929"
port = 1883
topic = "/logging"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'owntracks'
password = 'aratucampeao'

SIZE = 29
FORMAT = '<BHHHHHHHHBBBBBBBLB'

car = deque(200 * [''], 200)
accx = deque(200 * [0], 200)
accx = deque(200 * [0], 200)
accy = deque(200 * [0], 200)
accz = deque(200 * [0], 200)
dpsy = deque(200 * [0], 200)
dpsz = deque(200 * [0], 200)
rpm = deque(200 * [0], 200)
speed = deque(200 * [0], 200)
temp_motor = deque(200 * [0], 200)
flags = deque(200 * [0], 200)
soc = deque(200 * [0], 200)
temp_cvt = deque(200 * [0], 200)
volt = deque(200 * [0], 200)
latitude = deque(200 * [0], 200)
longitude = deque(200 * [0], 200)
timestamp = deque(200 * [0], 200)
eixo = deque(200 * [0], 200)

b, a = signal.butter(1, 0.1, analog=False)

car_save = []
accx_save = []
accy_save = []
accz_save = []
dpsx_save = []
dpsy_save = []
dpsz_save = []
rpm_save = []
speed_save = []
temp_motor_save = []
flags_save =[]
soc_save = []
temp_cvt_save = []
volt_save = []
latitude_save = []
longitude_save = []
timestamp_save = []

stop_threads = False


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def connect_mqtt(broker, port, client_id, username, password):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):

        mqttmsg = msg.payload.decode()

        if mqttmsg[0] == 22:
            car.append("MB2")
            accx.append(mqttmsg[1] * 0.061 / 1000)
            accy.append(mqttmsg[2] * 0.061 / 1000)
            accz.append(mqttmsg[3] * 0.061 / 1000)
            rpm.append((mqttmsg[7] / 65535) * 5000)
            speed.append((mqttmsg[8] / 65535) * 60)
            temp_motor.append(mqttmsg[9])
            flags.append(mqttmsg[10])
            soc.append(mqttmsg[11])
            temp_cvt.append(mqttmsg[12])
            volt.append(mqttmsg[13])
            latitude.append(mqttmsg[14])
            longitude.append(mqttmsg[15])
            timestamp.append(mqttmsg[16])

            car_save.append("MB2")
            accx_save.append(mqttmsg[1] * 0.061 / 1000)
            accy_save.append(mqttmsg[2] * 0.061 / 1000)
            accz_save.append(mqttmsg[3] * 0.061 / 1000)
            rpm_save.append((mqttmsg[7] / 65535) * 5000)
            speed_save.append((mqttmsg[8] / 65535) * 60)
            temp_motor_save.append(mqttmsg[9])
            flags_save.append(mqttmsg[10])
            soc_save.append(mqttmsg[11])
            temp_cvt_save.append(mqttmsg[12])
            volt_save.append(mqttmsg[13])
            latitude_save.append(mqttmsg[14])
            longitude_save.append(mqttmsg[15])
            timestamp_save.append(mqttmsg[16])

        if mqttmsg[0] == 11:
            car.append("MB1")
            accx.append(mqttmsg[1] * 0.061 / 1000)
            accy.append(mqttmsg[2] * 0.061 / 1000)
            accz.append(mqttmsg[3] * 0.061 / 1000)
            rpm.append((mqttmsg[7] / 65535) * 5000)
            speed.append((mqttmsg[8] / 65535) * 60)
            temp_motor.append(mqttmsg[9])
            flags.append(mqttmsg[10])
            soc.append(mqttmsg[11])
            temp_cvt.append(mqttmsg[12])
            volt.append(mqttmsg[13])
            latitude.append(mqttmsg[14])
            longitude.append(mqttmsg[15])
            timestamp.append(mqttmsg[16])

            car_save.append("MB1")
            accx_save.append(mqttmsg[1] * 0.061 / 1000)
            accy_save.append(mqttmsg[2] * 0.061 / 1000)
            accz_save.append(mqttmsg[3] * 0.061 / 1000)
            rpm_save.append((mqttmsg[7] / 65535) * 5000)
            speed_save.append((mqttmsg[8] / 65535) * 60)
            temp_motor_save.append(mqttmsg[9])
            flags_save.append(mqttmsg[10])
            soc_save.append(mqttmsg[11])
            temp_cvt_save.append(mqttmsg[12])
            volt_save.append(mqttmsg[13])
            latitude_save.append(mqttmsg[14])
            longitude_save.append(mqttmsg[15])
            timestamp_save.append(mqttmsg[16])

    client.subscribe(topic)
    client.on_message = on_message

class Receiver(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.com = self.connectSerial(serial_ports())
        print(f'Connected into {self.com}')
        self.connected_mqtt = True
        try:
            self.client = connect_mqtt(broker, port, client_id, username, password)
            self.client.loop_start()
        except TimeoutError:
            self.connected_mqtt = False
            print("MQTT Timed out")

        #self.conn = sqlite3.connect('mangue_database.db')
        #self.id_count = 0

        #try:
            #self.conn.execute("CREATE TABLE aquisitions (ID INT PRIMARY KEY, accx INT, accy INT, accz INT, "
                              #"rpm INT, speed INT, temp_motor REAL, flags INT, soc INT, temp_cvt REAL, volts REAL, "
                              #"latitude REAL, longitude REAL, timestamp INT)")
        #except sqlite3.OperationalError:
            #print("Tabela 'aquisitions' j?? existe. Ignorando erro...")

        #self.conn.commit()

    def connectSerial(self, USB_PORT):
        com = []
        for usb in USB_PORT:
            try:
                com = serial.Serial(f'{usb}', 115200)
            except:
                print("Tentativa...")
                com = []
            if com:
                break

        if not com:
            raise Exception("N??o h?? nenhuma porta serial dispon??vel")
        else:
            return com

    def run(self):
        self.com.flush()

        while True:
            try:
                self.checkData()
            except:
                break
    
    def checkData(self):
        c = 0
        while c != b'\xff':
            c = self.com.read()
            # print(f'trying, {c}')
        msg = self.com.read(SIZE)
        # print(msg)
        pckt = list(unpack(FORMAT, msg))
        # print(pckt)
        # print((pckt[25]/65535)*5000)
        if pckt[0] == 22:
            car.append("MB2")
            accx.append(pckt[1] * 0.061 / 1000)
            accy.append(pckt[2] * 0.061 / 1000)
            accz.append(pckt[3] * 0.061 / 1000)
            rpm.append((pckt[7] / 65535) * 5000)
            speed.append((pckt[8] / 65535) * 60)
            temp_motor.append(pckt[9])
            flags.append(pckt[10])
            soc.append(pckt[11])
            temp_cvt.append(pckt[12])
            volt.append(pckt[13])
            latitude.append(pckt[14])
            timestamp.append(pckt[16])

            car_save.append("MB2")
            accx_save.append(pckt[1] * 0.061 / 1000)
            accy_save.append(pckt[2] * 0.061 / 1000)
            accz_save.append(pckt[3] * 0.061 / 1000)
            rpm_save.append((pckt[7] / 65535) * 5000)
            speed_save.append((pckt[8] / 65535) * 60)
            temp_motor_save.append(pckt[9])
            flags_save.append(pckt[10])
            soc_save.append(pckt[11])
            temp_cvt_save.append(pckt[12])
            volt_save.append(pckt[13])
            latitude_save.append(pckt[14])
            longitude_save.append(pckt[15])
            timestamp_save.append(pckt[16])

        if pckt[0] == 11:
            car.append("MB1")
            accx.append(pckt[1] * 0.061 / 1000)
            accy.append(pckt[2] * 0.061 / 1000)
            accz.append(pckt[3] * 0.061 / 1000)
            rpm.append((pckt[7] / 65535) * 5000)
            speed.append((pckt[8] / 65535) * 60)
            temp_motor.append(pckt[9])
            flags.append(pckt[10])
            soc.append(pckt[11])
            temp_cvt.append(pckt[12])
            volt.append(pckt[13])
            latitude.append(pckt[14])
            longitude.append(pckt[15])
            timestamp.append(pckt[16])

            car_save.append("MB1")
            accx_save.append(pckt[1] * 0.061 / 1000)
            accy_save.append(pckt[2] * 0.061 / 1000)
            accz_save.append(pckt[3] * 0.061 / 1000)
            rpm_save.append((pckt[7] / 65535) * 5000)
            speed_save.append((pckt[8] / 65535) * 60)
            temp_motor_save.append(pckt[9])
            flags_save.append(pckt[10])
            soc_save.append(pckt[11])
            temp_cvt_save.append(pckt[12])
            volt_save.append(pckt[13])
            latitude_save.append(pckt[14])
            longitude_save.append(pckt[15])
            timestamp_save.append(pckt[16])

        data = {

            'Carro': car_save,
            'Acelera????o X': accx_save,
            'Acelera????o Y': accy_save,
            'Acelera????o Z': accz_save,
            'RPM': rpm_save,
            'Velocidade': speed_save,
            'Temperatura Motor': temp_motor_save,
            'Flags': flags_save,
            'State of Charge': soc_save,
            'Temperatura CVT': temp_cvt_save,
            'Volts': volt_save,
            'Latitude': latitude_save,
            'Longitude': longitude_save,
            'Timestamp': timestamp_save

        }
        ccsv = pd.DataFrame(data, columns=['Carro', 'Acelera????o X', 'Acelera????o Y', 'Acelera????o Z', 'RPM',
                                          'Velocidade', 'Temperatura Motor', 'Flags', 'State of Charge',
                                          'Temperatura CVT', 'Volts', 'Latitude', 'Longitude', 'Timestamp'])
       
        ccsv.to_csv('dados_telemetria.csv')

    sqlmsg = list()
    sqlmsg.append(str(car[-1]))
    sqlmsg.append(str(accx[-1]))
    sqlmsg.append(str(accy[-1]))
    sqlmsg.append(str(accz[-1]))
    sqlmsg.append(str(rpm[-1]))
    sqlmsg.append(str(speed[-1]))
    sqlmsg.append(str(temp_motor[-1]))
    sqlmsg.append(str(flags[-1]))
    sqlmsg.append(str(soc[-1]))
    sqlmsg.append(str(temp_cvt[-1]))
    sqlmsg.append(str(volt[-1]))
    sqlmsg.append(str(latitude[-1]))
    sqlmsg.append(str(longitude[-1]))
    sqlmsg.append(str(timestamp[-1]))
    if self.connected_mqtt:
            MQTT_JSON = json.dumps({"car": f"{sqlmsg[0]}", "accx": f"{sqlmsg[1]}", "accy": f"{sqlmsg[2]}", "accz": f"{sqlmsg[3]}",
            "rpm": f"{sqlmsg[4]}", "speed": f"{sqlmsg[5]}", "motor": f"{sqlmsg[6]}", "flags": f"{sqlmsg[7]}",
            "soc": f"{sqlmsg[8]}", "cvt": f"{sqlmsg[9]}", "volt": f"{sqlmsg[10]}", "latitude": f"{sqlmsg[11]}",
            "longitude": f"{sqlmsg[12]}", "timestamp": f"{sqlmsg[13]}"})

            publish(self.client, topic, MQTT_JSON)
        #try:
            #self.conn.execute("INSERT INTO aquisitions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              #(self.id_count, sqlmsg[0], sqlmsg[1], sqlmsg[2], sqlmsg[3], sqlmsg[4], sqlmsg[5], sqlmsg[6], sqlmsg[7],
                               #sqlmsg[8], sqlmsg[9], sqlmsg[10], sqlmsg[11], sqlmsg[12], sqlmsg[13]))
        #except sqlite3.IntegrityError:
            #print("Dado j?? existente...  Desfazendo modifica????es!!!")
            #self.conn.rollback()
        #else:
            #print("Tudo ok.  Commitando...")
            #self.conn.commit()

        #self.id_count += 1


class Ui_MainWindow(object):
    def __init__(self):
        self.webView = QWebEngineView()
        self.opening = True
        self.cont = 0


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 460)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.map = QtWidgets.QLabel(self.centralwidget)
        self.map.setGeometry(QtCore.QRect(10, 10, 461, 251))
        self.map.setObjectName("map")

        self.graph_rot = pg.PlotWidget(self.centralwidget)
        self.graph_rot.setGeometry(QtCore.QRect(10, 290, 221, 150))
        self.graph_rot.setObjectName("graph_rot")
        self.graph_rot.setBackground('w')
        self.graph_rot.setTitle("RPM", color='r')

        self.graph_vel = pg.PlotWidget(self.centralwidget)
        self.graph_vel.setGeometry(QtCore.QRect(250, 290, 221, 150))
        self.graph_vel.setObjectName("graph_vel")
        self.graph_vel.setBackground('w')
        self.graph_vel.setTitle("Velocidade", color='b')

        font = QtGui.QFont()
        font.setPointSize(16)

        self.acc_x = QtWidgets.QLabel(self.centralwidget)
        self.acc_x.setGeometry(QtCore.QRect(480, 10, 130, 51))
        self.acc_x.setObjectName("acc_x")
        self.acc_x.setFont(font)

        self.acc_y = QtWidgets.QLabel(self.centralwidget)
        self.acc_y.setGeometry(QtCore.QRect(620, 10, 130, 51))
        self.acc_y.setObjectName("acc_y")
        self.acc_y.setFont(font)

        self.acc_z = QtWidgets.QLabel(self.centralwidget)
        self.acc_z.setGeometry(QtCore.QRect(760, 10, 130, 51))
        self.acc_z.setObjectName("acc_z")
        self.acc_z.setFont(font)

        self.fuel = QtWidgets.QLabel(self.centralwidget)
        self.fuel.setGeometry(QtCore.QRect(510, 60, 161, 200))
        self.fuel.setObjectName("fuel")
        self.fuel.setText("")
        self.fuel.setPixmap(QtGui.QPixmap("fuel_full.jpg"))
        self.fuel.setScaledContents(True)

        self.batt = QtWidgets.QLabel(self.centralwidget)
        self.batt.setGeometry(QtCore.QRect(690, 110, 161, 101))
        self.batt.setObjectName("batt")
        self.batt.setFont(font)

        self.temp_motor = QtWidgets.QLabel(self.centralwidget)
        self.temp_motor.setGeometry(QtCore.QRect(690, 240, 161, 101))
        self.temp_motor.setObjectName("temp_motor")
        self.temp_motor.setFont(font)

        self.temp_cvt = QtWidgets.QLabel(self.centralwidget)
        self.temp_cvt.setGeometry(QtCore.QRect(510, 240, 161, 101))
        self.temp_cvt.setObjectName("temp_cvt")
        self.temp_cvt.setFont(font)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(570, 370, 181, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(770, 370, 101, 31))
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 19))
        self.menubar.setObjectName("menubar")
        self.menuRadio = QtWidgets.QMenu(self.menubar)
        self.menuRadio.setObjectName("menuRadio")
        self.menuMQTT = QtWidgets.QMenu(self.menubar)
        self.menuMQTT.setObjectName("menuMQTT")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionStartRadio = QtWidgets.QAction(MainWindow)
        self.actionStartRadio.setObjectName("actionStartRadio")
        self.actionStartRadio.triggered.connect(self.thread_radio)

        self.actionStopRadio = QtWidgets.QAction(MainWindow)
        self.actionStopRadio.setObjectName("actionStopRadio")
        self.actionStopRadio.triggered.connect(self.stop_clicked)

        self.actionStartMQTT = QtWidgets.QAction(MainWindow)
        self.actionStartMQTT.setObjectName("actionStartMQTT")
        self.actionStartMQTT.triggered.connect(self.thread_mqtt)

        self.actionStopMQTT = QtWidgets.QAction(MainWindow)
        self.actionStopMQTT.setObjectName("actionStopMQTT")
        self.actionStopMQTT.triggered.connect(self.stop_clicked)

        self.menuRadio.addAction(self.actionStartRadio)
        self.menuRadio.addAction(self.actionStopRadio)
        self.menuMQTT.addAction(self.actionStartMQTT)
        self.menuMQTT.addAction(self.actionStopMQTT)
        self.menubar.addAction(self.menuRadio.menuAction())
        self.menubar.addAction(self.menuMQTT.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_plots(self, rot_x, rot_y, vel_x, vel_y):
        self.rpm_pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.vel_pen = pg.mkPen(color=(0, 0, 255), width=2)

        self.graph_rot.setXRange(-50 + self.cont, self.cont)
        self.graph_rot.setYRange(0, 6000)
        self.rot_line = self.graph_rot.plot(rot_x, rot_y, pen=self.rpm_pen)

        self.graph_vel.setXRange(-50 + self.cont, self.cont)
        self.graph_vel.setYRange(0, 60)
        self.vel_line = self.graph_vel.plot(vel_x, vel_y, pen=self.vel_pen)

    def update_map(self, coordinate):

        if coordinate == (0, 0):
            coordinate = (-8.07305556, -37.266611111)

        self.m = folium.Map(
            zoom_start=17,
            location=coordinate
        )
        folium.Marker(location=coordinate).add_to(self.m)
        self.m.save("map.html")

        if self.opening:
            img_data = self.m._to_png(1)
            img = Image.open(io.BytesIO(img_data))
            img.save('map.png')
            self.map.setPixmap(QtGui.QPixmap("map.png"))
            self.map.setScaledContents(True)
            self.opening = False

    def stop_clicked(self):
        global stop_threads
        stop_threads = True

    def thread_radio(self):
        self.t1 = Thread(target=self.start_clicked_radio)
        self.t1.start()
        self.t2 = Thread(target=self.thread_map)
        self.t2.start()

    def thread_mqtt(self):
        self.t1 = Thread(target=self.start_clicked_mqtt)
        self.t1.start()
        self.t2 = Thread(target=self.thread_map)
        self.t2.start()

    def thread_map(self):
        while True:
            img_data = self.m._to_png(1)
            img = Image.open(io.BytesIO(img_data))
            img.save('map.png')
            self.map.setPixmap(QtGui.QPixmap("map.png"))
            self.map.setScaledContents(True)

            global stop_threads
            if stop_threads:
                if box.com:
                    box.com.close()
                break

    def start_clicked_radio(self):
        self.cont = 0

        while True:
            self.rot_line.clear()
            self.vel_line.clear()

            self.cont += 1
            eixo.append(self.cont)

            sig_rpm = signal.filtfilt(b, a, rpm)
            sig_speed = signal.filtfilt(b, a, speed)

            self.update_plots(eixo, sig_rpm, eixo, sig_speed)
            self.update_map((latitude[-1], longitude[-1]))

            self.acc_x.setText(f"Acc x = {round(accx[-1], 1)}g")
            self.acc_y.setText(f"Acc y = {round(accy[-1], 1)}g")
            self.acc_z.setText(f"Acc z = {round(accz[-1], 1)}g")

            self.batt.setText(f"Bateria = {soc[-1]}%")

            self.temp_cvt.setText(f"CVT = {temp_cvt[-1]}??C")
            self.temp_motor.setText(f"Motor = {temp_motor[-1]}??C")

            time.sleep(0.5)

            global stop_threads
            if stop_threads:
                if box.com:
                    box.com.close()
                break

    def start_clicked_mqtt(self):
        if box.connected_mqtt:
            subscribe(box.client, topic)
        self.cont = 0

        self.rot_line.clear()
        self.vel_line.clear()

        while True:
            self.cont += 1
            eixo.append(self.cont)

            sig_rpm = signal.filtfilt(b, a, rpm)
            sig_speed = signal.filtfilt(b, a, speed)

            self.update_plots(eixo, sig_rpm, eixo, sig_speed)
            self.update_map((latitude[-1], longitude[-1]))

            self.acc_x.setText(f"Acc x = {round(accx[-1], 1)}g")
            self.acc_y.setText(f"Acc y = {round(accy[-1], 1)}g")
            self.acc_z.setText(f"Acc z = {round(accz[-1], 1)}g")

            self.batt.setText(f"Bateria = {soc[-1]}%")

            self.temp_cvt.setText(f"CVT = {temp_cvt[-1]}??C")
            self.temp_motor.setText(f"Motor = {temp_motor[-1]}??C")

            time.sleep(0.5)

            global stop_threads
            if stop_threads:
                if box.com:
                    box.com.close()
                break

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mangue Telemetria"))

        self.update_map((-8.07305556, -37.266611111))
        self.update_plots([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
        self.acc_x.setText(_translate("MainWindow", f"Acc x = {0}g"))
        self.acc_y.setText(_translate("MainWindow", f"Acc y = {0}g"))
        self.acc_z.setText(_translate("MainWindow", f"Acc z = {0}g"))
        self.batt.setText(_translate("MainWindow", f"Bateria = {0}%"))
        self.temp_motor.setText(_translate("MainWindow", f"Motor = {0}??C"))
        self.temp_cvt.setText(_translate("MainWindow", f"CVT = {0}??C"))
        self.comboBox.setItemText(0, _translate("MainWindow", "BOX"))
        self.pushButton.setText(_translate("MainWindow", "Enviar"))
        self.menuRadio.setTitle(_translate("MainWindow", "Radio"))
        self.menuMQTT.setTitle(_translate("MainWindow", "MQTT"))
        self.actionStartRadio.setText(_translate("MainWindow", "Start"))
        self.actionStopRadio.setText(_translate("MainWindow", "Stop"))
        self.actionStartMQTT.setText(_translate("MainWindow", "Start"))
        self.actionStopMQTT.setText(_translate("MainWindow", "Stop"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    box = Receiver(name='serial_port')
    if box.com:
        box.start()
    # exemplo: ui.acc_x.setText("Acc x = 2g")
    sys.exit(app.exec_())
