import RPi.GPIO as GPIO
import time

# Mengatur mode penomoran pin
GPIO.setmode(GPIO.BCM)

# Mengatur pin GPIO 23 sebagai output
MOSFET_PIN = 23
GPIO.setup(MOSFET_PIN, GPIO.OUT)

try:
    # Mengaktifkan MOSFET
    GPIO.output(MOSFET_PIN, GPIO.HIGH)
    print("MOSFET menyala")
    
    # Menunggu 1 detik
    time.sleep(0.5)

    # Mematikan MOSFET
    GPIO.output(MOSFET_PIN, GPIO.LOW)
    print("MOSFET mati")

finally:
    # Membersihkan semua pengaturan GPIO
    GPIO.cleanup()
