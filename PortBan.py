import argparse
import datetime
import os
import uuid
import logging
import yaml
import requests
import re
import flask
from flask import request

ip = "0.0.0.0"
app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

def readYaml():
    with open("config.yaml", "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


@app.route('/<aaa>')
def home(aaa):
    path = aaa
    client_ip = request.remote_addr
    if re.match("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",client_ip):
        if path in rules:
            rule = rules.get(path)
            port = rule.get("port")
            prompt = rule.get("prompt")
            allow_access(client_ip,port)
            wlog("{} ip: [{}] 已被加入 [{}] 白名单".format(getTime(),client_ip,prompt))
            return "你的ip: [{}] 已被加入 [{}] 白名单，端口: {}".format(client_ip,prompt,port)


        return "This is not your website, don't open it casually, you can accompany your wife and children when you have time. What? You don't have a girlfriend? Then you must be rich, don't you?"
    else:
        return "Oh, God, what are you doing? Oh, God, look what this bitch is thinking, get your stupid mouse off your burpsuite interface, you son of a bitch, don't touch your head, I can't figure out what this chicken is thinking."

def wlog(nr):
    with open("log.txt","a") as f:
        f.write(nr + "\n")
        f.close()

def getIP():
    url = "http://myip.ipip.net"
    req = requests.get(url)
    return re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", req.text)[0]

def getuuid():
    return str(uuid.uuid4())

def getTime():
    return str(datetime.datetime.now())[0:19] + " "

def parRunle(rules):
    newDice = {}
    for i in rules:
        path = i.get("path")
        if path == None:
            path = getuuid()
        newDice[path] = {"prompt":i.get("prompt"),"port":i.get("port"),"release":i.get("release")}
    return newDice

def allow_access(ip,port):
    comm = "iptables -I INPUT -p tcp --dport {} -s {} -j ACCEPT".format(port, ip)
#    print(comm)
    os.system(comm)

def banned_all(port):
    comm = "iptables -A INPUT -p tcp --dport {} -j DROP".format(port)
#    print(comm)
    os.system(comm)

def checkRelease(rules):
    for i in rules:
        rule = rules[i]
        banned_all(rule.get('port'))
        if rule.get("release") != None:
            for x in rule.get("release"):
                allow_access(x,rule.get('port'))

if __name__ == '__main__':
    yamlDict = readYaml()
    webport = yamlDict.get("webport")
    init = yamlDict.get("init")
    os.system(init)
    rules = parRunle(yamlDict.get("rules"))
#    print(rules)
    checkRelease(rules)
    myip = getIP()
    for i in rules:
        rule = rules.get(i)
        print("{}{}: http://{}:{}/{}".format(rule.get("prompt"),rule.get("port"),myip,webport,i))
    app.run(host="0.0.0.0",port=webport)




