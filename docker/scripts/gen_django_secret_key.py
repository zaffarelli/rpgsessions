#!/usr/bin/python
import secrets
new_secret = "".join([secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$^&*(-_=+)") for i in range(50)])
with open('./secrets/django_secret_key.txt', 'w') as f:
    f.write(new_secret)
    f.close()
