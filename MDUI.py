import cv2
import time


def detect_video():
    camera = cv2.VideoCapture(0)
    history = 10    # 训练帧数
    wid = camera.get(3)    # 1280:video resolution
    hgh = camera.get(4)    # 720:video resolution
    rectLoc1 =[(int(wid*0.70),int(hgh*0.65)), (int(wid*0.95),int(hgh*0.93))]
    textOrg1 =(int(wid*0.72),int(hgh*0.80))
    textOrg01 =(int(wid*0.72),int(hgh*0.))


    rectLoc2 =[(int(wid*0.70),int(hgh*0.35)), (int(wid*0.95),int(hgh*0.07))]
    textOrg2 =(int(wid*0.72),int(hgh*0.25))

    rectLoc3 = [(int(wid * 0.05), int(hgh * 0.10)), (int(wid * 0.20), int(hgh * 0.30))]
    textOrg3 = (int(wid * 0.10), int(hgh * 0.25))
    textOrg03 = (int(wid * 0.10), int(hgh * 0.25))

    bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)  # 背景减除器，设置阴影检测
    bs.setHistory(history)

    frames = 0

    while True:
        res, frame = camera.read()

        if not res:
            break

        fg_mask = bs.apply(frame)   # 获取 foreground mask

        if frames < history:
            frames += 1
            continue

        # 对原始帧进行膨胀去噪
        th = cv2.threshold(fg_mask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
        th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
        # 获取所有检测框
        image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.rectangle(frame,rectLoc1[0],rectLoc1[1], (255, 255, 255), 5)
        cv2.putText(frame,"JOB1",textOrg1,2,2,(255,255,255),3)

        cv2.rectangle(frame,rectLoc2[0],rectLoc2[1], (255, 255, 255), 5)
        cv2.putText(frame,"JOB2",textOrg2,2,2,(255,255,255),3)

        cv2.rectangle(frame, rectLoc3[0], rectLoc3[1], (255, 255, 255), 5)
        cv2.putText(frame, "ESC", textOrg3, 2, 2, (255, 255, 255), 3)


        for c in contours:
            # 获取矩形框边界坐标
            rect = cv2.boundingRect(c)
            # 计算矩形框的面积
            area = cv2.contourArea(c)
            if MINCON < area < MAXCON:
                cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
                if rectContains(rectLoc3,(int((rect[0] + rect[2])/2), int((rect[1] + rect[3])/2))):  #job3
                    global j3cntr
                    j3cntr+=1

            cv2.putText(frame, str('%.3f'%(j3cntr/THRESHOLD)), textOrg03, 2, 1, (0, 255, 255), 3)  #show the current percentage to thershold

            if (j3cntr >= THRESHOLD):
                job3()
                j3cntr = 0



        cv2.imshow("detection", frame)
        #cv2.imshow("back", dilated)
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    camera.release()

def job3():
    global cntr
    cntr += 1
    #time.sleep(1)
    print("LOL it work!",cntr)


def rectContains(rect,pt):#return true if point is in rectangle
    logic = rect[0][0] < pt[0] < rect[1][0] and rect[0][1] < pt[1] < rect[1][1]
    return logic


if __name__ == '__main__':
    global THRESHOLD,j3cntr,cntr
    j3cntr = 0
    THRESHOLD = 100
    cntr = 0
    global MINCON,MAXCON
    MINCON = 5000
    MAXCON = 60000
    detect_video()
