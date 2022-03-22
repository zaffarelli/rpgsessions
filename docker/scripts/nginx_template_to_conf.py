#!/usr/bin/python
import os

# Load nginx airshield_conf.template
targets = []
with open("../.env", 'r') as ref:
    lines = ref.readlines()
    for line in lines:
        if line.startswith('#') == False and '=' in line:
            words = line.split("=")
            targets.append({'key': words[0].replace('\n', '').strip(), 'value': words[1].replace('\n', '').strip()})
    print(targets)
    ref.close()

newlines = []
with open("../nginx/airshield_nginx.template", 'r') as template:
    lines = template.readlines()
    for line in lines:
        newline = line
        for target in targets:
            if target['key'] in line:
                newline = line.replace("___%s___" % target['key'], target['value'])
        newlines.append(newline)
    template.close()

with open("../nginx/airshield_nginx.conf", 'w') as conf:
    conf.writelines("".join(newlines))
    conf.close()

print("NGINX conf recreated")
