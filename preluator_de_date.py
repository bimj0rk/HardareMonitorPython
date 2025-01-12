import wmi
import platform
import psutil
import py3nvml

if platform.system() == 'Windows':
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    sensors = w.Sensor()

    def getSensorValue(sensor_type, sensor_name):
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == sensor_type and sensor.Name == sensor_name:
                return sensor.Value
        return None

    def getCpuTemp():
        return getSensorValue('Temperature', 'CPU Package')

    def getCpuLoad():
        return getSensorValue('Load', 'CPU Total')

    def getMemLoad():
        return getSensorValue('Load', 'Memory')

    def getGpuTemp():
        return getSensorValue('Temperature', 'GPU Core')

    def getGpuLoad():
        return getSensorValue('Load', 'GPU Core')

#to modify, la un moment dat mergea, acum nu suntem siguri ca nu avem linux pe pc/laptop
elif platform.system() == 'Linux':
    def getCpuTemp():
        return psutil.sensors_temperatures()['coretemp'][0].current

    def getCpuLoad():
        return psutil.cpu_percent()

    def getMemLoad():
        return psutil.virtual_memory().percent

    def getGpuTemp():
        return py3nvml.grab_gpus()[0].temperature

    def getGpuLoad():
        return py3nvml.grab_gpus()[0].load