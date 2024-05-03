import pyautogui
import platform

#? Basic file that runs after using the "make" command
#?      After running program: Clears the screen and puts away the terminal

opSys = platform.system() #Determine what platfor the user is using

if opSys == "Darwin": #MacOS
    pyautogui.keyDown('command')
    pyautogui.keyDown('k')
    pyautogui.keyUp('command')
    pyautogui.hotkey('ctrl', '`')
elif opSys == "Windows": #Windows
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', '`')