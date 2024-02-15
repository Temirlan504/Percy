from flask import Flask, render_template, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

# Picamera setup
picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={
            "format": 'XRGB8888',
            "size": (1640, 1232)
        }
    )
)
picam2.start()

# Generate frames from camera input
def generate_frames():
    while True:
        im = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', im)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Route for video feed processing
@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# Render 'Home' page
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Allow everyone to connect to this server on the local network
    app.run(host='0.0.0.0', port=5000, debug=False)
