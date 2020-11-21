import pyautogui
import time

while 1:
    currentX, currentY = pyautogui.position()
    print(currentX, currentY)
    time.sleep(1)