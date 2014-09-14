from lib.config import *
from lib.camera import * 
from lib.switches import * 

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

import time

app = Flask(__name__)
conf = Config("camera.conf")
switches = Switches()
pic = PIC(conf.get_dictionary())


app.config.from_object(__name__)

@app.route('/')
def show_entries():

    filelist = os.listdir(os.getcwd())
    filelist = filter(lambda x: not os.path.isdir(x), filelist)
    filelist = filter(lambda x: (x[-3:] in ['jpg','png']), filelist)
    #pass the newest image or nothing
    if(len(filelist)>0):
        newest = max(filelist, key=lambda x: os.stat(x).st_mtime)
        return render_template('index.html', path=newest)
    else:
        return render_template('index.html')


@app.route('/take_photo')
def do_photo():
    filename = pic.get_picture()
    filename = filename.replace(conf.get_dictionary()['directory']+"/","")
#    return render_template('image.html', path=filename)

    data = {'filename': filename}
    resp = jsonify(data)
    resp.status_code =200
    return resp

@app.route('/take_cv')
def do_cv2():
    filename = pic.get_cv()
    filename = filename.replace(conf.get_dictionary()['directory']+"/","")
    return render_template('image.html', path=filename)


@app.route('/take_video')
def do_video():
    filename = pic.get_video()
    return render_template('video.html', path=filename)

if __name__ == '__main__':
    app.debug = True
    if(app.debug):
	print("WARNING: THE DEBUG MODE IS ON, THIS WILL GIVE A SHELL TO ANYONE VISITING AN ERROR PAGE! To remove this, set app.debug=False in the main.py script")
    app.run(host="0.0.0.0")
