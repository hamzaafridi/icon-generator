from flask import escape, abort
import io
import numpy as np
import cv2

ALLOWED_EXTENSIONS = ['png']

def iconGenerator(request):
    """HTTP Cloud Function to remove background and transform icon to different sizes
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    #check if the request is valid
    if request.method != "POST":
        if "image" not in  request.files:
            return abort(403)   

    img = request.files["image"]
    
    if not allowed_file(img.filename):
        return abort(403)
    
    #read image into memory and convert to opencv
    in_memory_file = io.BytesIO()
    img.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)

    #remove background
    mask = (img[...,0] != 255) & (img[...,1] != 255) & (img[...,2] != 255)
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = mask*255
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel.astype(np.uint8)))

    return 'bacground removed: shape({})!'.format(img_BGRA.shape)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS