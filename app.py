from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import tensorflow as tf
from twilio.rest import Client

app = Flask(__name__)
model = tf.keras.models.load_model('Missing.h5')
name = ["Found Missing", "Normal"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    img = Image.open(image)
    img = img.resize((64, 64))
    x = np.array(img)
    x = np.expand_dims(x, axis=0)

    # Predict the image
    pred = model.predict(x)
    pred_class = np.argmax(pred, axis=1)[0]

    if pred_class == 0:
        account_sid = 'ACc36f587b05c6cae6b4e87a0e72dbc9ed'
        auth_token = '6be1180990b5c13b870147323b7303fc'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to='+919177686868',
            from_='+14175282474',
            body='Found the Missing at 17.3984° N, 78.5583° E'
        )
        print(message.sid)
        result = "Found Missing"
        sms_status = "SMS Sent"
    else:
        result = "Normal"
        sms_status = ""

    return render_template('result.html', result=result, sms_status=sms_status)

if __name__ == '__main__':
    app.run(debug=True)
