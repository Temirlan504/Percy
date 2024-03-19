from flask import Flask, jsonify, render_template, Response
from picamera2 import Picamera2
import cv2
import RPi.GPIO as GPIO

app = Flask(__name__)

# Define GPIO pins
MOTOR1_PIN_1 = 17
MOTOR1_PIN_2 = 27

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR1_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR1_PIN_2, GPIO.OUT)

# Set PWM frequency and duty cycle
frequency = 1000  # Adjust frequency as needed (Hz)
duty_cycle = 100   # Adjust duty cycle as needed (0% - 100%)

# Create PWM instances
motor_pwm1 = GPIO.PWM(MOTOR1_PIN_1, frequency)
motor_pwm2 = GPIO.PWM(MOTOR1_PIN_2, frequency)

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


# Motor control routes
@app.route('/forward-start')
def forward_start():
    motor_pwm1.start(duty_cycle)
    return jsonify(message='Motor started')

@app.route('/forward-stop')
def forward_stop():
    motor_pwm1.stop()
    return jsonify(message='Motor stopped')

@app.route('/backward-start')
def reverse_start():
    motor_pwm2.start(duty_cycle)
    return jsonify(message='Motor started')

@app.route('/backward-stop')
def reverse_stop():
    motor_pwm2.stop()
    return jsonify(message='Motor stopped')


# Main function
if __name__ == '__main__':
    # Allow everyone to connect to this server on the local network
    app.run(host='0.0.0.0', port=5000, debug=False)
