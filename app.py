from flask import Flask, jsonify, render_template, Response
from picamera2 import Picamera2
import cv2
import RPi.GPIO as GPIO
from smbus import SMBus
import time
from ads1115 import TemperatureSensor

app = Flask(__name__)

# Define GPIO pins
MOTOR1_PIN_1 = 17
MOTOR1_PIN_2 = 27

MOTOR2_PIN_1 = 22
MOTOR2_PIN_2 = 10

MOTOR3_PIN_1 = 9
MOTOR3_PIN_2 = 11

MOTOR4_PIN_1 = 5
MOTOR4_PIN_2 = 6

# I2C setup for ADC
ADC_i2c = SMBus(1) # I2C bus on GPIO2 (SDA) and GPIO3 (SCL)
temp_sensor = TemperatureSensor(ADC_i2c)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR1_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR1_PIN_2, GPIO.OUT)
GPIO.setup(MOTOR2_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR2_PIN_2, GPIO.OUT)
GPIO.setup(MOTOR3_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR3_PIN_2, GPIO.OUT)
GPIO.setup(MOTOR4_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR4_PIN_2, GPIO.OUT)

# Set PWM frequency and duty cycle
frequency = 1000  # Adjust frequency as needed (Hz)
duty_cycle = 50   # Adjust duty cycle as needed (0% - 100%)

# Create PWM instances
motor_pwm1 = GPIO.PWM(MOTOR1_PIN_1, frequency)
motor_pwm2 = GPIO.PWM(MOTOR1_PIN_2, frequency)

motor2_pwm1 = GPIO.PWM(MOTOR2_PIN_1, frequency)
motor2_pwm2 = GPIO.PWM(MOTOR2_PIN_2, frequency)

motor3_pwm1 = GPIO.PWM(MOTOR3_PIN_1, frequency)
motor3_pwm2 = GPIO.PWM(MOTOR3_PIN_2, frequency)

motor4_pwm1 = GPIO.PWM(MOTOR4_PIN_1, frequency)
motor4_pwm2 = GPIO.PWM(MOTOR4_PIN_2, frequency)


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
    adc_out_binary = temp_sensor.read(ADC_i2c)
    adc_out_decimal = int(adc_out_binary, 2)

    # Convert the ADC output to temperature
    # Derived from y=mx+b
    temperatureC = 0.015107 * adc_out_decimal + 11.5564

    return render_template(
        'index.html',
        temperature=round(temperatureC, 2)
    )


# Motor control routes
@app.route('/forward-start')
def forward_start():
    motor_pwm1.start(duty_cycle)
    motor2_pwm1.start(duty_cycle)
    motor3_pwm1.start(duty_cycle)
    motor4_pwm1.start(duty_cycle)
    return jsonify(message='Motor started')

@app.route('/forward-stop')
def forward_stop():
    motor_pwm1.stop()
    motor2_pwm1.stop()
    motor3_pwm1.stop()
    motor4_pwm1.stop()
    return jsonify(message='Motor stopped')

@app.route('/backward-start')
def reverse_start():
    motor_pwm2.start(duty_cycle)
    motor2_pwm2.start(duty_cycle)
    motor3_pwm2.start(duty_cycle)
    motor4_pwm2.start(duty_cycle)
    return jsonify(message='Motor started')

@app.route('/backward-stop')
def reverse_stop():
    motor_pwm2.stop()
    motor2_pwm2.stop()
    motor3_pwm2.stop()
    motor4_pwm2.stop()
    return jsonify(message='Motor stopped')

@app.route('/left-start')
def left_start():
    motor_pwm1.start(duty_cycle)
    motor2_pwm1.start(duty_cycle)

    motor3_pwm2.start(duty_cycle)
    motor4_pwm2.start(duty_cycle)
    return jsonify(message='Motor started')

@app.route('/left-stop')
def left_stop():
    motor_pwm1.stop()
    motor2_pwm1.stop()

    motor3_pwm2.stop()
    motor4_pwm2.stop()
    return jsonify(message='Motor stopped')


# Main function
if __name__ == '__main__':
    # Allow everyone to connect to this server on the local network
    app.run(host='0.0.0.0', port=5000, debug=False)
