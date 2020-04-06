#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from MyQR import myqr
import os
version, level, qr_name = myqr.run(
    words='https://weixin.qq.com/g/AQ4qK-F6wX2NGmq2',
    version=1,
    level='L',
    picture='/Users/shiwan/Documents/Development/kg/scrawler/QR-Code/southeast.jpg',
    colorized=True,
    contrast=1.0,
    brightness=1.0,
    save_name='中信建投aws.png',
    save_dir=os.getcwd()
)
