# -*- coding: utf-8 -*-

import os

for root, dirs, files in os.walk('/Users/admin/PythonTest/123'):
    for dir in dirs:
        print('-'+dir)
    for filename in files:
        print('---'+filename)
    print('+++'+root)