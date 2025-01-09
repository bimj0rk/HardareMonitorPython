import serial #pentru legatura cu Arduino, se poate scoate in cazul in care nu se foloseste un Arduino
import time
import psutil
import py3nvml #pentru a prelua date despre un GPU de la NVidia (asta folosesc, pentru AMD nu stiu daca exista un package similar)

arduino = serial.Serial(port = "/dev/ttyACM0", baudrate = 115200, timeout = .1) #portul se schimba in functie de ce detecteaza sistemul de operare

def sendAndRecieveDataToArduino(data):
    arduino.write(data.encode())
    time.sleep(0.05)
    data = arduino.readline()
    return data

def initializeNVML():
    py3nvml.nvmlInit()

def handle():
    handle = py3nvml.nvmlDeviceGetHandleByIndex(0)
    return handle

def getInfo():
    cpuTemp = psutil.sensors_temperatures()['coretemp'][0].current #primul nucleu al cpu ului
    cpuLoad = psutil.cpu_percent()
    memLoad = psutil.virtual_memory().percent
    gpuTemp = py3nvml.nvmlDeviceGetTemperature(handle(), 0)
    gpuLoad = py3nvml.nvmlDeviceGetUtilizationRates(handle()).gpu
    
    def writeToArduino():
        #template ul pe care l-am luat pentru display are un format specific, aranjam datele in functie de asta
        A = " " + str(int(cpuTemp))
        
        if(cpuLoad < 10):
            B = "  " + str(int(cpuLoad))
        elif(cpuLoad > 10 and cpuLoad < 100):
            B = " " + str(int(cpuLoad)) 
        else:
            B = str(int(cpuLoad))

        if(memLoad < 10):
            C = "  " + str(int(memLoad))
        elif(memLoad > 10 and memLoad < 100):
            C = " " + str(int(memLoad)) 
        else:
            C = str(int(memLoad))
            
        finalString1 = "1:" + A + "," + B + "," + C + ",N/A,;" #acel N/A vine in locul senzorului de temp pt motherboard, ceea ce nu se poate afla cu libraria psutil (si nici cu alta librarie din research ul pe care l-am facut)
        
        E = " " + str(int(gpuTemp))
        
        if(gpuLoad < 10):
            F = "  " + str(int(gpuLoad))
        elif(gpuLoad > 10 and gpuLoad < 100):
            F = " " + str(int(gpuLoad)) 
        else:
            F = str(int(gpuLoad))
            
        finalString2 = "2:" + E + "," + F + ",N/A,N/A,;" #cei doi N/A vin de la FPS ul aplicatiei curente (would be nice to have) si de la temp carcasei (in proiectul de arduino, cine l-a facut a lipit un senzor de temp pe carcasa)
        finalString3 = "3:;"
        
        return finalString1, finalString2, finalString3
    

initializeNVML()
handle = handle()
while True:
    getInfo()
    sendAndRecieveDataToArduino(getInfo()[0])
    sendAndRecieveDataToArduino(getInfo()[1])
    sendAndRecieveDataToArduino(getInfo()[2])