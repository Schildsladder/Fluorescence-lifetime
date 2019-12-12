from multiprocessing import Process, Queue
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from serial import Serial
import time
from os import listdir
from os.path import isfile, join
import queue as Q
import msvcrt
from scipy.signal import savgol_filter
import pandas as pd
#def integ_set():



def func1(queue):
    
#    ser = Serial("COM7")
    import serial.tools.list_ports
    def find_arduino(serial_number):
        for pinfo in serial.tools.list_ports.comports():
            if pinfo.serial_number == serial_number:
                return serial.Serial(pinfo.device)
        raise IOError("Could not find an arduino - is it plugged in?")
    
    ser = find_arduino(serial_number='7')
#    ser = serial.Serial('COM4')

    
    def kb():
        x=msvcrt.kbhit()
        if x:
            xxx=msvcrt.getch()
        else:
            return False
        return xxx

    
    
    
    data_buff_size = 3695     
    data = np.zeros(data_buff_size) 
    n_bytes = 7390
    n=3694
    k=0
    kk=0
    kkk=0
    data11=np.zeros(n)
    datax=np.zeros([0])
#    mydata=np.zeros([8,3694])
#    mydatab=np.zeros([2,3694])
    k1=0
    xa=3
    xb=0
    k3=0
    datax=np.zeros([3,3695])
    
    
    def save_file(dmas):

        files = [f for f in listdir('data') if isfile(join('data', f))]
        hh=len(files)+1
#        hh=90
        hh1='data/'+str(hh)+'.npy'
        hh3='datax/'+str(hh)+'.xlsx'
        data = dmas.astype(dtype=np.float)
        np.save(hh1, data)
#        print "logging data for : ", time.time()-t2, " second"
#        print "saving data as : ", hh1 
        ## convert your array into a dataframe
        
        x=np.linspace(0,(3694.0/666),n)
        xxx=np.append([x],[data],axis=0)
        df = pd.DataFrame (xxx.T)
        ## save to xlsx file
       
        df.to_excel(hh3, index=False)


    xx="b "
    ta=time.time()
    qa=0
    while k == 0: 
                
    #    while k==0:
        x=kb()
        try:
            if x!= False and x!='\r':
        #         try:         
                x=x.decode()
                xx=xx+x
#                print (x)
            if x!=False and x=='\r':
#                print ("aaa")
#                print (xx)
                if xx[2]== "d":        
                    print ("finish")
                    xa=1
                elif xx[2]== "s":
                    xa=0
                    print("start")

                xx="b"
        except UnicodeDecodeError:
            print ("only number are allowed")
            x=kb()
            xx="b"
        except ValueError:
            xx="b"
            print ("only number are allowed")
        except IndexError:
            xx="b"
            print ("please input number")
    #    time.sleep(0.03)



        kkk=kkk+1         
        rslt = ser.read(7390)
        data = np.fromstring(rslt, dtype=np.uint16)
        ## print "ok ", time.time()-t1
        if data[0] > 12500:
            rslt=rslt[1:-1]
            data = np.fromstring(rslt, dtype=np.uint16)
            kk=ser.read(1)
            print ("error")

        datax=np.append(datax,[data],axis=0)
       
        
        if k3==5:
            try:
                datax=datax[-30:]
            except:
                pass
            datab=np.mean(datax,0)
            queue.put(datab)
            k3=0
        k3+=1



        
        if xa==0:
            print ("begin data logging")
            k1=1
#            dataxx=np.zeros([3,3695])
#            dataxx=np.append(dataxx,[data],axis=0)
            dataxx=data[:-1]
            qa=1
            t2=time.time()
            xa=3
        if xa==1:
            k1=0
#            dataxx=dataxx[3:]
#            dataxx=dataxx[:,0:-1]
            qa=0
            save_file(dataxx)
#            print ("okkkk")
            xa=3
            
        if k1==1:
            xb=xb+1
            try:
#                dataxx=dataxx[3:]
#                dataxx=dataxx[:,0:-1]
                dataxx=(dataxx*(qa/(qa+1)))+(data[:-1]*(1/(qa+1)))
                qa=qa+1
#                datax=np.append(datax,data)
            except ValueError:
                print (mydata.shape)




def func2(queue):
#    from scipy.signal import savgol_filter
    
    time.sleep(0.8)
    win = pg.GraphicsWindow()
    win.setWindowTitle('Data')
    n=4000
#    data11=np.zeros(n)
    global datx
    datx=np.zeros(n)
#    global dataave
#    dataave=np.zeros([505,n])
    
    
    p1 = win.addPlot()
#    win.nextRow()
#    p2 = win.addPlot()
    curvea = p1.plot(datx, pen=(0,255 ,0))
#    curveb= p2.plot(data22, pen=(0,0 , 255))
#    p1.setYRange(-30, 2300, padding=0)
    

    
    def update1():
        global datx
        try:
            datx=queue.get(timeout=0.9)
            curvea.setData(datx[0:-1])
        except:
            curvea.setData(datx[0:-1])
#        curveb.setData(datx[1::2])
        
        



    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update1)
    timer.start(50)
    
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()




if __name__ == '__main__':
    queue=Queue()

#    queue5=Queue()
#    queue6=Queue()
    
    p1 = Process(target=func1,args=(queue,))
    p1.start()
    p2 = Process(target=func2,args=(queue,))
    p2.start()

#    p4 = Process(target=func4,args=(queue2,))
#    p4.start()
    
    p1.join()
    p2.join()

#    p4.join()