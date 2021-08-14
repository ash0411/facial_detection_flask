from flask import Flask, render_template,Response,request
import cv2
import datetime, time
import os,sys
import numpy as np
from    threading import Thread
global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0
# making shot directory to save files
try:
    os.mkdir('shots')
except OSError as error:
    print('Not able to make a directory')
    pass
app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
 while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            global grey,neg,capture,face
            detector=cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
            faces=detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if grey:
                frame = gray
            if neg:
                frame = cv2.bitwise_not(frame)
            if face:
                for (x,y,w,h) in faces:
                    crop_frame = frame[x:x+w,y:y+h]
                    frame = crop_frame
            if capture:
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)   
             #Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
@app.route('/')
def index():
    return render_template('index_img.html')
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/tasks',methods=['GET','POST'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'capture':
            global capture
            capture = 1
        elif request.form.get('grey') == 'grey':
            global grey
            grey = not grey
        elif request.form.get('negative')=='negative':
            global neg
            neg = not neg
        elif request.form.get('face_only') == 'face_only':
            global face
            face = not face
            if(face):
                time.sleep(4)
        elif request.form.get('stop') == 'stop/start':
            if switch == 1:
                switch = 0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch = 1
        elif request.form.get('rec') == 'start/stop recording':
            global rec, out
            rec = not rec
            # if(rec):
            #     now=datetime.datetime.now() 
            #     fourcc = cv2.VideoWriter_fourcc(*'XVID')
            #     out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
            #     #Start new thread for recording the video
            #     thread = Thread(target = record, args=[out,])
            #     thread.start()
            # elif(rec==False):
            #     out.release()
    elif request.method == 'GET':
        return render_template('index_img.html')
    return render_template('index_img.html')




if __name__ == '__main__':
    app.run()