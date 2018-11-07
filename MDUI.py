import cv2
import webbrowser

def detect_video():
    camera = cv2.VideoCapture(0)
    history = 10    # 训练帧数
    wid = camera.get(3)    # 1280:video resolution
    hgh = camera.get(4)    # 720:video resolution
    rectLoc1 =[(int(wid*0.70),int(hgh*0.65)), (int(wid*0.95),int(hgh*0.93))]
    textOrg1 =(int(wid*0.72),int(hgh*0.80))
    textOrg01 =(int(wid*0.72),int(hgh*0.92))

    rectLoc2 =[(int(wid*0.70),int(hgh*0.07)), (int(wid*0.95),int(hgh*0.35))]
    textOrg2 =(int(wid*0.72),int(hgh*0.22))
    textOrg02 = (int(wid*0.72),int(hgh*0.34))

    rectLoc3 = [(int(wid * 0.05), int(hgh * 0.10)), (int(wid * 0.20), int(hgh * 0.30))]
    textOrg3 = (int(wid * 0.07), int(hgh * 0.20))
    textOrg03 = (int(wid * 0.07), int(hgh * 0.29))

    #print(rectLoc1 )
    #print(rectLoc2 )
    #print(rectLoc3 )

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
        cv2.putText(frame,"show course",textOrg2,1,2,(255,255,255),3)

        cv2.rectangle(frame, rectLoc3[0], rectLoc3[1], (255, 255, 255), 5)
        cv2.putText(frame, "EXIT", textOrg3, 2, 2, (255, 255, 255), 3)


        for c in contours:
            # 获取矩形框边界坐标
            rect = cv2.boundingRect(c)
            xp=int(rect[0] + rect[2])
            yp=int(rect[1] + rect[3])
            #print(xp,yp)
            area = cv2.contourArea(c)
            if MINCON < area < MAXCON:
                cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
                if rectContains(rectLoc3,(xp, yp)):  #job3
                    global j3cntr
                    j3cntr+=1
                elif rectContains(rectLoc2,(xp, yp)):#job2
                    global j2cntr
                    j2cntr+=1
                elif rectContains(rectLoc1,(xp, yp)):#job1
                    global j1cntr
                    j1cntr+=1
            cv2.circle(frame,(xp,yp),3,(0,0,255),1)
            cv2.putText(frame, str('%.3f'%(j1cntr/THRESHOLD)), textOrg01, 2, 1, (0, 255, 255), 3)  #show the current percentage to thershold
            cv2.putText(frame, str('%.3f'%(j2cntr/THRESHOLD)), textOrg02, 2, 1, (0, 255, 255), 3)  #show the current percentage to thershold
            cv2.putText(frame, str('%.3f'%(j3cntr/THRESHOLD)), textOrg03, 2, 1, (0, 255, 255), 3)  #show the current percentage to thershold



            if j3cntr >= THRESHOLD:
                job3()
                j3cntr = 0
                j2cntr = 0
                j1cntr = 0
            elif j2cntr >= THRESHOLD:
                job2()
                j3cntr = 0
                j2cntr = 0
                j1cntr = 0
            elif j1cntr >= THRESHOLD:
                job1()
                j3cntr = 0
                j2cntr = 0
                j1cntr = 0


        cv2.imshow("detection", frame)
        #cv2.imshow("back", dilated)
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    camera.release()

def job1():
    #time.sleep(1)
    print("LOL it work!  1")

def job2():
    #time.sleep(1)
    webbrowser.open('https://www.cs.nccu.edu.tw/~whliao/hci2018/',2)

def job3():
    #time.sleep(1)
    print("LOL it work!  3")


def rectContains(rectLoc,pt):#return true if point is in rectangle
    if rectLoc[0][0] < pt[0] < rectLoc[1][0] and rectLoc[0][1] < pt[1] < rectLoc[1][1]:
        return True
    else :
        return False


if __name__ == '__main__':
    webbrowser.open('https://www.cs.nccu.edu.tw/~whliao/hci2018/',2)

    global THRESHOLD
    THRESHOLD = 40
    global j1cntr,j2cntr,j3cntr
    j1cntr = 0
    j2cntr = 0
    j3cntr = 0
    global MINCON,MAXCON
    MINCON = 500
    MAXCON = 60000
    detect_video()
