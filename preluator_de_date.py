import wmi
import platform
import psutil
import py3nvml

def log_warning(message):
    print(f"WARNING: {message}")

if platform.system() == 'Windows':
    try:
        w = wmi.WMI(namespace=r"root\OpenHardwareMonitor")
    except Exception as e:
        log_warning(f"Failed to initialize WMI: {e}")
        w = None

    def getSensorValue(sensor_type, sensor_name):
        if w is None:
            log_warning("OpenHardwareMonitor is not available.")
            return None
        try:
            sensors = w.Sensor()
            print("\nAvailable sensors:")
            for sensor in sensors:
                print(f"Name: {sensor.Name}, Type: {sensor.SensorType}, Value: {sensor.Value}")
                if sensor.SensorType.lower() == sensor_type.lower() and sensor_name.lower() in sensor.Name.lower():
                    return sensor.Value
            log_warning(f"Sensor not found: {sensor_name} ({sensor_type})")
        except Exception as e:
            log_warning(f"Error fetching sensor value for {sensor_type} - {sensor_name}: {e}")
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

# Work in progress for Linux based systems
# elif platform.system() == 'Linux':
#     def getCpuTemp():
#         return psutil.sensors_temperatures()['coretemp'][0].current

#     def getCpuLoad():
#         return psutil.cpu_percent()

#     def getMemLoad():
#         return psutil.virtual_memory().percent

#     def getGpuTemp():
#         return py3nvml.grab_gpus()[0].temperature

#     def getGpuLoad():
#         return py3nvml.grab_gpus()[0].load