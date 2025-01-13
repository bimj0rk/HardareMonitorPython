import wmi

def log_warning(message):
    print(f"WARNING: {message}")


try:
    w = wmi.WMI(namespace = r"root\OpenHardwareMonitor")
except Exception as e:
    log_warning(f"Failed to initialize WMI: {e}")
    w = None

def getSensorValue(sensor_type, sensor_name):
    if w is None:
        log_warning("OpenHardwareMonitor nu e deschis.")
        return None
    try:
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType.lower() == sensor_type.lower() and sensor_name.lower() in sensor.Name.lower():
                return sensor.Value
    except Exception as e:
        log_warning(f"Error: {sensor_type} - {sensor_name}: {e}")
    return None


def getCpuTemp():
    return getSensorValue('Temperature', 'CPU Package')

def getCpuLoad():
    return getSensorValue('Load', 'CPU Total')

def getGpuTemp():
    return getSensorValue('Temperature', 'GPU Core')

def getGpuLoad():
    return getSensorValue('Load', 'GPU Core')

def getMoboTemp():
    return getSensorValue('Temperature', 'Temperature #1')

def getMemLoad():
    return getSensorValue('Load', 'Memory')