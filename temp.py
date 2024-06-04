import Adafruit_DHT

def get_suhu(gpio_pin):
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)
    if humidity is not None and temperature is not None:
        # return 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        return '{0:0.1f}'.format(temperature)
    else:
        return 'Failed to get reading. Try again!'