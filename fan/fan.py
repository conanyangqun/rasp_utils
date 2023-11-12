#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gpiozero
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")


class AutoFAN(object):
    def __init__(self, pin=14, temp_on=50, temp_off=40):
        self.pin = pin
        self.temp_on = temp_on
        self.temp_off = temp_off
        self.fan = gpiozero.OutputDevice(self.pin)
        self.temp_file = '/sys/class/thermal/thermal_zone0/temp'
        self.temp = 0.0

    def measure_temp(self):
        with open(self.temp_file) as f:
            self.temp = float(f.read()) / 1000

    def run(self):
        logging.info('温控风扇开启(高于{}摄氏度开启风扇，低于{}摄氏度关闭风扇)'.format(
            self.temp_on, self.temp_off
        ))
        while True:
            self.measure_temp()
            if self.temp > self.temp_on and not self.fan.is_active:
                # high temp and fan off
                logging.info('温度:{}摄氏度，开启风扇'.format(self.temp))
                self.fan.on()
            elif self.fan.is_active and self.temp < self.temp_off:
                logging.info('温度: {}摄氏度，关闭风扇'.format(self.temp))
                self.fan.off()
            else:
                pass
            time.sleep(5)

    def close(self):
        self.fan.close()


if __name__ == '__main__':
    fan = AutoFAN()
    try:
        fan.run()
    finally:
        fan.close()
