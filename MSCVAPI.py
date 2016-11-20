########### Python 2.7 #############
import httplib, urllib, base64
import cv2
import imutils
import numpy as np
import datetime
import time
import serial
import re
def visionAPILink(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '14ac89f222ca4b3fa9158588fe6a7911',
    }

    params = urllib.urlencode({
        # Request parameters
        'visualFeatures': 'Categories,Tags,Description,Faces,ImageType,Color',
        'language': 'en',
    })
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, '{"url":"'+url+'"}', headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def visionAPIImg(img):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '14ac89f222ca4b3fa9158588fe6a7911',
    }

    params = urllib.urlencode({
        # Request parameters
        'visualFeatures': 'Categories,Tags,Description,Faces,ImageType,Color',
        'language': 'en',
    })
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, img, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data

def isRecycable(JSON):
    result = re.findall('"name":"(.*?)","', JSON)
    tagsresult = re.findall('{"tags":(.*?)],', JSON)
    isrecycable=0
    for item in tagsresult:
        temp = re.findall('"(.*?)"', item)
        print len(temp)
        for tempitem in temp:
            if tempitem != "":
                if any(tempitem in s for s in keywords):
                    print tempitem
                    isrecycable = 1
                    break
    for item in result:
        if any(item in s for s in keywords):
            print item
            isrecycable=1
            break

    return isrecycable


def cameraLoop(camera):
    # initialize the first frame in the video stream
    firstFrame = None
    testOccupied = "false"
    firstOccupied = 0
    testOccupiedCounter = 0;
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"
        frame = frame[25:500, 110:475]
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 1000:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text

            # (x, y, w, h) = cv2.boundingRect(c)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

        # draw the text and timestamp on the frame
        # cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the loop
        if key == ord("q"):
            camera.release()
            cv2.destroyAllWindows()
            exit()
        if (firstOccupied == 0) & (text == "Occupied") & (testOccupied != "testing"):
            firstOccupied = 1;
        if firstOccupied == 1:
            testOccupied = "testing"
            testOccupiedCounter = 0
            firstOccupiedFrame = gray
            firstOccupied = 0;
        if testOccupied == "testing":
            frameDelta = cv2.absdiff(firstOccupiedFrame, gray)
            thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)
            temptestOccupiedCheck = "true"
            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) > 500:
                    temptestOccupiedCheck = "false"
                    break

            if temptestOccupiedCheck == "false":
                testOccupiedCounter = 0;
                testOccupied = "false";
                firstOccupied = 0;
            else:
                testOccupiedCounter = testOccupiedCounter + 1

        # if text== "Occupied":
        #     stablecounter = stablecounter+1
        if (text == "Occupied") & (testOccupiedCounter == 50):
            cv2.imshow("test", frame)
            cv2.imwrite("test.jpg", frame)
            with open("test.jpg", "rb") as imageFile:
                f = imageFile.read()
                b = bytearray(f)
            imageFile.close();
            data = visionAPIImg(b)
            digit = isRecycable(data)
            print digit
            arduino.write(str(digit))
            break

            # cleanup the camera and close any open windows
keywords=["bottle","can","drink_","glass","beverage","cup","drink_can","glass","newspaper","paper","book","envelope","card"]



arduino = serial.Serial('COM4',9600, timeout=.1)
time.sleep(2)
while True:
    camera = cv2.VideoCapture(0)
    cameraLoop(camera)
    camera.release()
    time.sleep(5)
    # key = cv2.waitKey(1) & 0xFF
    #
    # # if the `q` key is pressed, break from the lop
    # if key == ord("q"):
    #     break
cv2.destroyAllWindows()
