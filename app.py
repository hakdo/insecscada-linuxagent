#!/usr/bin/env python3

from urllib import response
from flask import Flask, request, abort
import os

app = Flask(__name__)

sshkeypath = os.path.join(os.path.expanduser("~"), ".ssh/authorized_keys")

@app.route("/", methods=['GET', 'POST'])
def setwork():
    print(request.method)
    try:
        apikey = request.form.get("apikey")
        pubkey = request.form.get("pubkey")
        #apikey = request.args["apikey"]
        #pubkey = request.args["pubkey"]
        if apikey == os.environ["INSEC_AUTH"]:
            with open(sshkeypath, "a") as authfile:
                authfile.write("# Adding pubkey from web user\n")
                authfile.write(pubkey + "\n")
    except Exception as e:
        print("Exception: ", e)
        abort(401)
    duration = 8 #default work order duration - can change this dynamically later
    return "Hello"

@app.route("/removekey")
def removekey():
    try:
        apikey = request.args["apikey"]
        pubkey = request.args["pubkey"]
        if apikey == os.environ["INSEC_AUTH"]:
            with open(sshkeypath, "r") as authfile:
                mylines = authfile.readlines()
                keeplines = []
                for line in mylines:
                    print(line)
                    if line.strip("\n") != pubkey:
                        keeplines.append(line)
                    else:
                        if keeplines[-1][0] == "#":
                            keeplines.pop()
                print(keeplines)
            with open(sshkeypath, "w") as authfile:
                for line in keeplines:
                    authfile.write(line)
            return "donkey"
        else:
            return '<h1>403 Forbidden</h1>', 403
    except Exception as e:
        print("Exception", e)
        abort(401)


            


