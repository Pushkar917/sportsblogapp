import os, time
# pip install pillow
from PIL import Image
from pathlib import Path
from PIL import ImageOps

from flask import url_for, current_app


def add_profile_pic(pic_upload, username):
    filename = pic_upload
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    username = username.replace(" ", "") + str(time.monotonic()).split(".")[0]
    storage_filename = str(username) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static/Profile_Pic', storage_filename)
    openingFile = os.path.join(current_app.root_path, 'static/Profile_Pic', filename)
    # Play Around with this size
    basewidth = 200
    # Open the picture and save it
    img = Image.open(openingFile)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(filepath)

    return storage_filename

