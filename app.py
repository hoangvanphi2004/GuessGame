import os

import requests;
import openai 
from flask import Flask, redirect, render_template, request, url_for, session
from flask import g
import json

app = Flask(__name__)
app.secret_key = "superSecret 0o0 "
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    # initial session
    if session.get("pr") == None: session["pr"] = 3;
    
    # get input from user
    if request.method == "POST":
        if "reset" in request.form:
            session.clear();
            if session.get("pr") == None: session["pr"] = 3;
        else:
            input = request.form["input"];
            header = {
                'Authorization' : f'Bearer {os.getenv("OPENAI_API_KEY")}'
            }
            session["body"]["messages"].append({
                    "role": "user",
                    "content": input
                });
            response = json.loads(requests.post("https://api.openai.com/v1/chat/completions", headers = header, json = session["body"]).text);
            session["body"]["messages"].append({
                    "role": "assistant",
                    "content": response['choices'][0]['message']['content']
                });
            session.modified = True;
            return redirect(url_for("index", result = response['choices'][0]['message']['content']))
    
    # Initial stage or current
    if(session["pr"] == 3):
        header = {
            'Authorization' : f'Bearer {os.getenv("OPENAI_API_KEY")}'
        }
        session["body"] = {
            "model": "gpt-3.5-turbo",
            "messages": [
            {
                "role": "system",
                "content": "your work is guess what character am i thinking of."
            },
            {
                "role": "user",
                "content": "ask me something"
            }
            ]
        };
        response = json.loads(requests.post("https://api.openai.com/v1/chat/completions", headers = header, json = session["body"]).text);
        result = str(response['choices'][0]['message']['content']);
        session["body"]["messages"].append({
                "role": "assistant",
                "content": response['choices'][0]['message']['content']
            });
        session["pr"] = 4;
    else:
        result = request.args.get("result")
    return render_template("index.html", question = result)
