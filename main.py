import time
import pyautogui as pyautogui
from cnocr import CnOcr

ocr = CnOcr(det_model_name='naive_det')
cur = [1, 2]
nex = [1, 2]
dict = {}
pre = 0
count = 0
errorCount = 0
lock = 0
NUMBER_OF_PROBLEM = 30

print('ready')

while True:
    try:
        # 识别下一个数字
        leftPicNext = pyautogui.screenshot(region=(175, 425, 60, 40))   # 左侧的下一个数字
        rightPicNext = pyautogui.screenshot(region=(320, 425, 60, 40))  # 右侧的下一个数字
        leftPicNext.save('leftNext.png')
        rightPicNext.save('rightNext.png')
        leftOutNext = ocr.ocr_for_single_line('./leftNext.png')
        rightOutNext = ocr.ocr_for_single_line('./rightNext.png')
        leftNext = leftOutNext['text']
        rightNext = rightOutNext['text']
        nex[0] = int(leftNext)
        nex[1] = int(rightNext)

        # 识别题号
        jud = pyautogui.screenshot(region=(225, 63, 100, 32))  # 题目区域
        jud.save('jud.png')
        IndexOut = ocr.ocr_for_single_line('./jud.png')
        jud = IndexOut['text']
        jud = jud.split('/')
        number = int(jud[0])

        if number == 1:
            leftPic = pyautogui.screenshot(region=(125, 310, 85, 58))  # 左侧的当前数字
            rightPic = pyautogui.screenshot(region=(315, 310, 85, 58))
            leftPic.save('left.png')
            rightPic.save('right.png')
            leftOut = ocr.ocr_for_single_line('./left.png')
            rightOut = ocr.ocr_for_single_line('./right.png')
            left = leftOut['text']
            right = rightOut['text']
            cur[0] = int(left)
            cur[1] = int(right)
            dict[number] = [cur[0], cur[1]]     # 第一次保存当前数字
        dict[number + 1] = [nex[0], nex[1]]     # 其余时候保存下一组数字

        if number != pre:   # 保证每题只画一次
            print(f'第{number}题:', dict[number][0], dict[number][1])
            if dict[number][0] > dict[number][1]:
                pyautogui.moveTo(229, 675, duration=0)
                pyautogui.drag(100, 50, 0.1, button='left')
                pyautogui.drag(-150, 70, 0.1, button='left')
            else:
                pyautogui.moveTo(229, 675, duration=0)
                pyautogui.drag(-100, 50, 0.1, button='left')
                pyautogui.drag(150, 70, 0.1, button='left')
            pre = number
            count = 0
        else:
            count += 1  # 若count > 3则视为出错了

        if count > 3:
            if dict[number][0] < dict[number][1]:
                pyautogui.moveTo(229, 675, duration=0)
                pyautogui.drag(100, 50, 0.1, button='left')
                pyautogui.drag(-150, 70, 0.1, button='left')
            else:
                pyautogui.moveTo(229, 675, duration=0)
                pyautogui.drag(-100, 50, 0.1, button='left')
                pyautogui.drag(150, 70, 0.1, button='left')
        if number >= NUMBER_OF_PROBLEM:
            count = 0
            lock = 1
    except Exception as e:
        errorCount += 1
        if errorCount > 100 and lock == 1:
            pyautogui.moveTo(274, 828, duration=2)
            pyautogui.click()
            pyautogui.moveTo(408, 970, duration=2)
            pyautogui.click()
            pyautogui.moveTo(283, 906, duration=2)
            pyautogui.click()
            errorCount = 0
            lock = 0
