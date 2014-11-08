
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import json
#to get the picture name
import time
#to call raspistill
from subprocess import call
#to get the most recent file name
import os

app = Flask(__name__)
app.config.from_object(__name__)
configuration=None
with open("conf.json", "r") as fp:
    configuration=json.loads(fp.read().replace('\n', ''))
imagedir=os.path.dirname(os.path.abspath(__file__))+'/static/'+configuration['image_directory']+'/'
@app.route('/')
def show_entries():
    filelist = os.listdir(imagedir)
    filelist = filter(lambda x: not os.path.isdir(x), filelist)
    filelist = filter(lambda x: (x[-3:] in ['jpg','png']), filelist)
    #get the newest image, or nothing
    if(len(filelist)>0):
        newest = max(filelist, key=lambda x: os.stat(imagedir+x).st_mtime)
        return render_template('index.html', path=configuration['image_directory']+'/'+newest)
    else:
        return render_template('index.html')

#take a picture and return the path
@app.route('/take_photo')
def do_photo():
    #raspistill -o fff.jpg
    picname=time.strftime("%Y%m%d_%H%M%S")+".jpg"
    filename = imagedir+picname
    #return render_template('image.html', path=filename)
    call(["/usr/bin/raspistill", "-o",filename])
    data = {'filename': configuration['image_directory']+'/'+picname}
    resp = jsonify(data)
    resp.status_code=200
    return resp

#show a page which will call the do_photo and load the picture on the client
@app.route('/show_current_picture')
def ask_photo():
     return render_template('askphoto.html')
if __name__ == '__main__':
    app.debug = True
    if(app.debug):
        print("WARNING: THE DEBUG MODE IS ON, THIS WILL GIVE A SHELL TO ANYONE VISITING AN ERROR PAGE! To remove this, set app.debug=False in the main.py script")
    app.run(host="0.0.0.0")
