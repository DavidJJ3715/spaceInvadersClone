import pyautogui
import platform

opSys = platform.system()

if opSys == "Darwin":
    pyautogui.keyDown('command')
    pyautogui.keyDown('k')
    pyautogui.keyUp('command')
    pyautogui.hotkey('ctrl', '`')
elif opSys == "Windows":
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', '`')