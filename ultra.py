import gpiozero
import time


def main_loop() -> None:
    b = gpiozero.Button(2)
    l = gpiozero.LED(3)
    l.off()
    time.sleep(0.5)
    last = b.is_pressed
    last_pulse_time = time.time()
    last_change_time = last_pulse_time
    while True:
        cur_time = time.time()
        if cur_time - last_pulse_time > 1.0:
            print('pulse')
            l.on()
            time.sleep(0.00001)
            l.off()
            last_pulse_time = cur_time

        p = b.is_pressed
        if last and not p:
            last = p
            pulse_start_time = cur_time
        elif p and not last:
            last = p
            print('fall', cur_time - pulse_start_time)

if __name__ == '__main__':
    main_loop()
