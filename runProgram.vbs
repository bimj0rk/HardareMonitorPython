Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "D:\GitHub Repositories\Python\Personal\Python101\Project\HardareMonitorPython\HardareMonitorPython\runGUI.bat" & Chr(34), 0
WshShell.Run chr(34) & "D:\GitHub Repositories\Python\Personal\Python101\Project\HardareMonitorPython\HardareMonitorPython\runArduino.bat" & Chr(34), 0
Set WshShell = Nothing
