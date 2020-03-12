# keras_server.py

# Python program to expose a ML model as flask REST API
import tensorflow as tf
# import the necessary modules
import numpy as np
import io
from flask import render_template
# import the necessary packages
from keras.models import load_model
# from pyimagesearch import config
import imutils
import cv2

# Create Flask application and initialize Keras model
model1 = None


# Function to Load the model
def load_model1():
    # global variables, to be used in another function
    global model1
    model1 = load_model('ML/python_code/Python code/KYC Detect/mdl_wts_1.hdf5')
    global graph
    graph = tf.get_default_graph()


# Every ML/DL model has a specific format
# of taking input. Before we can predict on
# the input image, we first need to preprocess it.
def prepare_image(image, target):
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize the image to the target dimensions
    image = image.resize(target)

    # PIL Image to Numpy array
    image = img_to_array(image)

    # Expand the shape of an array,
    # as required by the Model
    image = np.expand_dims(image, axis=0)

    # preprocess_input function is meant to
    # adequate your image to the format the model requires
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image


def predict(image):
    data = {}  # dictionary to store result
    data["success"] = False
    # Check if image was properly sent to our endpoint
    print('1', type(image))

    nparr = np.fromstring(image, np.uint8)
    print('2', nparr, type(nparr))
    image = cv2.imdecode(nparr, flags=1)  # cv2.IMREAD_COLOR
    #             image = Image.open(io.BytesIO(image))
    print('3', type(image), image)
    #             image = image.convert("RGB")
    #             print('3',type(image))
    #             output = image.copy()
    #             output = imutils.resize(output, width=400)
    #             # our model was trained on RGB ordered images but OpenCV represents
    # images in BGR order, so swap the channels, and then resize to
    # 224x224 (the input dimensions for VGG16)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    print('final image', image)
    # convert the image to a floating point data type and perform mean
    # subtraction
    # load the trained model from disk
    CLASSES = ["aadhar", "DL", "pan"]
    print("[INFO] loading model...", model1)
    # pass the image through the network to obtain our predictions
    with graph.as_default():
        # preds = model.predict(image)
        preds = model1.predict(np.expand_dims(image, axis=0))[0]
    i = np.argmax(preds)
    label = CLASSES[i]
    # draw the prediction on the output image
    text = "{}: {:.2f}%".format(label, preds[i] * 100)
    # cv2.putText(output, text, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 2)

    if (preds[i] * 100) > 90:
        print(label, preds[i] * 100)
    else:
        print('Other')
    print(text)
    data["success"] = True
    dict_data = {}
    dict_data['preds'] = preds[i] * 100;
    dict_data['label'] = label
    return dict_data




