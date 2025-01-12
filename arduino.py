import serial #pentru legatura cu Arduino, se poate scoate in cazul in care nu se foloseste un Arduino
import time
import preluator_de_date as pdd

arduino = serial.Serial(port = "COM6", baudrate = 115200, timeout = .1) #portul se schimba in functie de ce detecteaza sistemul de operare

def writeToArduino(data):
    arduino.write(data.encode())
    time.sleep(0.05)
    data = arduino.readline()
    return data
    

def getInfo():
    cpuTemp = pdd.getCpuTemp()
    cpuLoad = pdd.getGpuLoad()
    memLoad = pdd.getMemLoad()
    gpuTemp = pdd.getGpuTemp()
    gpuLoad = pdd.getGpuLoad()

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

while True:
    writeToArduino(getInfo()[0])
    writeToArduino(getInfo()[1])
    writeToArduino(getInfo()[2])

    time.sleep(0.5)