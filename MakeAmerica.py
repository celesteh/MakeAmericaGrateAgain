import numpy as np
import cv2
import random
import setproctitle
import argparse
import time

parser = argparse.ArgumentParser(description='Run the video installation.')

parser.add_argument('-r', '--record', nargs='?', default=False, help='Path to an output file')
args = parser.parse_args()
should_record = args.record

setproctitle.setproctitle('makeamerica')

global create_output_file
if (should_record):
    create_output_file = True
    outfile = should_record
else:
    create_output_file = False

global keep_going
keep_going = True

window_name = "frame"
#cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#cv2.namedWindow(window_name, cv2.WINDOW_FULLSCREEN)
#cv2.setWindowProperty(window_name,  cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name,  0,1)


cap = cv2.VideoCapture('shower.mp4')
bombs = cv2.VideoCapture('bomb/bomb_loop.mp4')

width = bombs.get(cv2.CAP_PROP_FRAME_WIDTH)
height = bombs.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = int(width)
height= int(height)

fourcc = cv2.VideoWriter.fourcc(*'XVID')#*'XVID'
if create_output_file:
    out = cv2.VideoWriter(outfile,fourcc, 12.0, (width,height))
    #out = cv2.VideoWriter('gifs/output.avi',fourcc, 12.0, (width,height))



#cap = cv2.VideoCapture(0)
_,five_prev=cap.read()
_,four_prev=cap.read()
_,three_prev=cap.read()
_,two_prev = cap.read()
_,prev = cap.read()


delay=list()
size = (25 * 80)
print('Loading . . .')
global output
output=0

bomb_counter = random.randint(0, (bombs.get(cv2.CAP_PROP_FRAME_COUNT)-(size + 10)))
bombs.set(cv2.CAP_PROP_POS_FRAMES, bomb_counter)

for x in range(0, size):
    _,output=bombs.read()
    delay.append(output)
    #print('.')
    #cv2.waitKey(0)
#delay.append(three_prev)
#delay.append(two_prev)
#delay.append(prev)

count=0
source=0
change=random.randint(100, 200)
index=0
last=0

reccount = 0

frame_counter = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
# Too explicit at the start if we start further in
#frame_counter = max(0, random.randint(0, cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)-(size * 4)))
#cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_counter)

bomb_counter = bomb_counter + size+1

#upper_blue=np.array([211, 60, 41])
#lower_blue=np.array([209, 60, 20])
lower_blue=np.array([0, 0, 50])#16, 34, 50
upper_blue=np.array([70, 90, 255])#42, 72, 105#60,80,255



while(cap.isOpened() and bombs.isOpened() and ((not create_output_file) or out.isOpened()) and keep_going):

    #manage looping

    frame_counter += 1
    #If the last frame is reached, reset the capture and the frame_counter
    if frame_counter >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0 #Or whatever as long as it is the same as next line
        cap.set(cv2.cv.CAP_PROP_POS_FRAMES, 0)
        if create_output_file:
            keep_going=False
        #create_output_file = True #??

    bomb_counter += 1
    #If the last frame is reached, reset the capture and the frame_counter
    if bomb_counter >= bombs.get(cv2.CAP_PROP_FRAME_COUNT):
        bomb_counter = 0 #Or whatever as long as it is the same as next line
        bombs.set(cv2.CAP_PROP_POS_FRAMES, 0)


    # get porn frame for chromakeying, etc

    ret, frame = cap.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #filtered = cv2.addWeighted(two_prev, 0.7, prev,0.7,0)
    filtered=cv2.add(three_prev,two_prev)
    filtered = cv2.add(filtered,prev)
    filtered = cv2.add(filtered, frame)#cv2.addWeighted(filtered, 0.6, frame, 0.7, 0)

    #make a mask
    img=cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(img,240,255,cv2.THRESH_BINARY)
    _,inv=cv2.threshold(img,240,255,cv2.THRESH_BINARY_INV)
    # we've got a good looking filtered image now

    f1=cv2.addWeighted(frame, 0.5, prev, 0.5, 0)
    f2=cv2.addWeighted(two_prev,0.5, three_prev, 0.5, 0)
    f3=cv2.addWeighted(five_prev,0.5, four_prev,0.5, 0)
    f2 =cv2.addWeighted(f2,0.55, f3, 0.45, 0)
    #f2 = two_prev + three_prev
    fucking=cv2.addWeighted(f1, 0.7, f2, 0.3, 0)

    #hsv=cv2.cvtColor(fucking, cv2.COLOR_BGR2HSV)
    #mask=cv2.inRange(hsv,np.array([0,0,0]), upper_blue)
    rgb=cv2.cvtColor(fucking, cv2.COLOR_BGR2RGB)#fucking#frame
    mask=cv2.inRange(rgb, lower_blue,upper_blue)
    mask=cv2.bitwise_and(mask,inv)#should get rid of double ons
    inv_blues=cv2.bitwise_not(mask)

    _,boom=bombs.read()
    blues=cv2.bitwise_and(boom, boom, mask=mask)
    background=boom;

    #pick source for background
    if(count>change):
        source = np.random.choice([0, 1], 1, p=[0.055, 0.945])
        #print('picked', source)
        if(source==1):
            change=random.randint(25, 200)
            index=random.randint(0,(len(delay)/2))
        else:
            change=random.randint(10, 45)
        count=0
    else:
        count = count +1
        #index=index+1

    if(source==1):
        background=delay[index]

    boom_layer=cv2.bitwise_and(background, background, mask=thresh1)
    bang_layer=cv2.bitwise_and(fucking, fucking, mask=inv)

    bang_layer=cv2.bitwise_and(bang_layer, bang_layer, mask=inv_blues)

    saturated = cv2.cvtColor(bang_layer, cv2.COLOR_BGR2HSV)
    + np.array([0, 4, 37])
    #saturated = cv2.cvtColor(bang_layer, cv2.COLOR_BGR2RGB)
    #+ np.array([10, 0, -2])

    saturated= cv2.cvtColor(saturated, cv2.COLOR_HSV2BGR)

    img = cv2.add(boom_layer, saturated)#bang_layer

    img=cv2.add(img,blues)

    if (np.random.choice([True, False], 1, p=[0.005, 0.995])) or last > 0:
        if last ==0:
            last=random.randint(1,30)
        img=boom
        last = last -1

    output=img
    cv2.imshow(window_name,output)
    delay.append(output)

    if create_output_file:
        out.write(output)
        #reccount = reccount +1
        #if reccount > 2160:
        #    keep_going = False
    else:
        time.sleep(0.0001)

    delay=delay[1:size]
    five_prev=four_prev
    four_prev=three_prev
    three_prev=two_prev
    two_prev = prev
    prev = frame
    #time.sleep(0.08)
    if cv2.waitKey(random.randint(75,85)) & 0xFF == ord('q'):
        #break
        keep_going = False



if create_output_file:
    out.release()
    create_output_file = False
cap.release()
bombs.release()
cv2.destroyAllWindows()
print('Done')
