#!/usr/bin/env python3

'''
reads Inbird iBBQ Thermometer temperature values on sensor 1&2 and outs it into a Mysql database

'''




from bluepy.btle import *
import datetime
import mysql.connector

hostname = 'localhost'
username = 'datasrc'
password = 'datasrc000'
database = 'InkBird'

def doQueryInsert (conn, temp1, temp2, batteryPct):
    #blesensor table is date, time, sensor1, sensor2, batteryPct
    cur = conn.cursor()
    dostr = 'INSERT INTO data VALUES (CURRENT_DATE(), NOW(), %s, %s, %s);'
    cur.execute (dostr, (temp1, temp2, batteryPct))
    conn.commit()

myConnection = mysql.connector.connect (host=hostname, user=username, passwd=password, db=database)


class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global temp1, temp2, minV, maxV, currentV, batteryPct
        if cHandle == 37:
            if data[0] == 0x23:
                minV = int.from_bytes(data[1:3],'little')
            if data[0] == 0x24:
                currentV = int.from_bytes(data[1:3],'little')
                maxV = int.from_bytes(data[3:5],'little')
                try:
                    print(maxV, minV, currentV)
                    batteryPct = int(
                        100
                        * ((currentV-minV) / (maxV-minV))
                    )
                except NameError:
                    print ("Not all values present, skipping calculation for now")
        if cHandle == 48:
            temp1 = int(int.from_bytes(data[:2],"little") / 10)
            temp2 = int(int.from_bytes(data[-2:],"little") / 10)
        try:
            print (datetime.datetime.now().strftime("%H:%M:%S"),",",temp1,",",temp2,",",batteryPct,sep="")
            doQueryInsert(myConnection, temp1, temp2, batteryPct)
        except NameError:
            print ("Not gotten all values yet, skipping for now")

# Set thermometer mac adress here
print ("setting dev")
dev = Peripheral("24:7d:4d:6a:74:71")


dev.setDelegate(MyDelegate())


# authenticate
z = dev.getCharacteristics(0x0028,0x0029)
dev.writeCharacteristic(0x0029,bytearray.fromhex("2107060504030201b8220000000000",),1)


# get battery level
# enable settings response
dev.writeCharacteristic(0x0026,bytearray.fromhex("0100"),1)

# Get minimal voltage value
dev.writeCharacteristic(0x0034,bytearray.fromhex("082300000000"),1)

# Get current voltage value
dev.writeCharacteristic(0x0034,bytearray.fromhex("082400000000"),1)


# Enable realtime data collection
s = dev.getCharacteristics(0x0033,0x0034)
dev.writeCharacteristic(0x0031,bytearray.fromhex("0100"),1)

# Subscribe to realtime data
dev.writeCharacteristic(0x0034,bytearray.fromhex("0B0100000000"),1)

# Set initial count to 15 to get first time reading below
cnt = 30

while True:
        try:
                if dev.waitForNotifications(2.0):
                    cnt += 1
                    if cnt > 15:
                        cnt = 0
                        dev.writeCharacteristic(0x0034,bytearray.fromhex("082300000000"),1)
                        dev.writeCharacteristic(0x0034,bytearray.fromhex("082400000000"),1)
                    continue
        except BTLEDisconnectError:
                print ("device disconnected")
                pass

