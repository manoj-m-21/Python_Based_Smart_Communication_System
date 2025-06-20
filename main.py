# Python program to translate
# speech to text and text to speech
import speech_recognition as sr
import pyttsx3
import cv2
import numpy as np
import math
import pyttsx3
# Initialize the recognizer
r = sr.Recognizer()
# Function to convert text to
# speech
def text_to_speech(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
# Loop infinitely for user to
# speak
def speech_to_text():
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something:")
        # Adjust for ambient noise before listening
        recognizer.adjust_for_ambient_noise(source)

        # Listen for the user's speech
        audio = recognizer.listen(source)

        print("Transcribing...")

        try:
            # Use Google Web Speech API to convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
def gesture_to_text():
    cap = cv2.VideoCapture(0)

    while (1):

        try:  # an error comes if it does not find anything in window as it cannot find contour of max area
            # therefore this try error statement

            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            kernel = np.ones((3, 3), np.uint8)

            # define region of interest
            roi = frame[100:400, 100:400]

            cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 0)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # define range of skin color in HSV
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 200, 200], dtype=np.uint8)

            # extract skin colur imagw
            mask = cv2.inRange(hsv, lower_skin, upper_skin)

            # extrapolate the hand to fill dark spots within
            mask = cv2.dilate(mask, kernel, iterations=4)

            # blur the image
            mask = cv2.GaussianBlur(mask, (5, 5), 100)

            # find contours
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # find contour of max area(hand)
            cnt = max(contours, key=lambda x: cv2.contourArea(x))

            # approx the contour a little
            epsilon = 0.0005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # make convex hull around hand
            hull = cv2.convexHull(cnt)

            # define area of hull and area of hand
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)
            # find the percentage of area not covered by hand in convex hull
            arearatio = ((areahull - areacnt) / areacnt) * 100

            # find the defects in convex hull with respect to hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)

            # l = no. of defects
            l = 0

            # code for finding no. of defects due to fingers
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt = (100, 180)

                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                s = (a + b + c) / 2
                ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                # distance between point and convex hull
                d = (2 * ar) / a

                # apply cosine rule here
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d > 30:
                    l += 1
                    cv2.circle(roi, far, 3, [255, 0, 0], -1)

                # draw lines around hand
                cv2.line(roi, start, end, [0, 255, 0], 2)

            l += 1

            # print corresponding gestures which are in their ranges
            font = cv2.FONT_HERSHEY_SIMPLEX
            if l == 1:
                if areacnt < 2000:
                    cv2.putText(frame, 'Put hand in the box', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                else:
                    if arearatio < 12:
                        cv2.putText(frame, '0', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

                    elif arearatio < 17.5:
                        cv2.putText(frame, 'Best of luck', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                        engine = pyttsx3.init()
                        engine.setProperty("rate", 120)
                        engine.say("Best of Luck")
                        # engine.runAndWait()
                    else:
                        cv2.putText(frame, 'Ok', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                        engine = pyttsx3.init()
                        engine.setProperty("rate", 120)
                        engine.say("Ok")
                        # engine.runAndWait()

            elif l == 2:
                cv2.putText(frame, 'No', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                engine = pyttsx3.init()
                engine.setProperty("rate", 120)
                engine.say("No")
                # engine.runAndWait()

            elif l == 3:
                cv2.putText(frame, 'How are You', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                engine = pyttsx3.init()
                engine.setProperty("rate", 120)
                engine.say("How are you")
                # engine.runAndWait()


            elif l == 4:
                cv2.putText(frame, 'I am Fine', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                engine = pyttsx3.init()
                engine.setProperty("rate", 120)
                engine.say("I am Fine")
                # engine.runAndWait()

            elif l == 5:
                cv2.putText(frame, 'i am hungry', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                engine = pyttsx3.init()
                engine.setProperty("rate", 120)
                engine.say("i am hungry")
                # engine.runAndWait()

            else:
                cv2.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            # show the windows
            cv2.imshow('mask', mask)
            cv2.imshow('frame', frame)
        except:
            pass

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    while True:
        com_mode = input("Select 1 for Text To Speech \nSelect 2 for Speech To Text\nSelect 3 for Gesture to Text")
        if com_mode == "1":
            command = input("Enter Text To convert Speech:")
            text_to_speech(command)
        if com_mode == "2":
            print("Say Something to convert text")
            speech_to_text()
        if com_mode == "3":
            #print("Say Something to convert text")
            gesture_to_text()
