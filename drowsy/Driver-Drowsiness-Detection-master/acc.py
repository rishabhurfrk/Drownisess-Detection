import serial
from twilio.rest import Client

account_sid = 'AC2eea8dea18c9cb073f98305556094d99'
auth_token = '92edb147dd5dd7ec7a84c75069802c4d'
client = Client(account_sid, auth_token)

arduino = serial.Serial(port='COM10', baudrate=9600, timeout=0.1)

def send_sms(body):
    message = client.messages.create(
        from_='+12702880778',
        body=body,
        to='+919508465840'
    )
    print("SMS sent:", message.sid)

def detect_accident(accelerometer_data):
    # Check if any of the accelerometer data values exceed the threshold of 10
    for val in accelerometer_data:
        if val > 10:
            return True
    return False

while True:
    try:
        data = arduino.readline().decode('utf-8').strip()
        accelerometer_data = [float(val) for val in data.split() if val.strip().replace('.', '').replace('-', '').isdigit()]
        if accelerometer_data:
            if detect_accident(accelerometer_data):
                print("Accident Detected!")
                send_sms("Accident Detected!")
    except UnicodeDecodeError:
        # Handle decoding error from serial port
        print("Error decoding data from serial port")
        continue
    except ValueError:
        # Handle conversion error to float
        print("Error converting data to float")
        continue
