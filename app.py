import os
import requests
import datetime, time
from collections import deque
from collection import login_required
from flask import Flask, render_template, jsonify, request, session, redirect
from flask_socketio import SocketIO, emit


app = Flask(__name__)
#to create a seesion you most configure this secret key
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["DEBUG"]=True
socketio = SocketIO(app)
channelCreated = []
userslogged = []
channelMessages = dict()

@app.route("/")
@login_required
def index():
    #to track if a user is have an existing session
    user= session.get('username')
    return render_template("index.html",user=user, channels=channelCreated)

@app.route("/signin", methods=["GET","POST"])
def signin():
    session.clear()
    username = request.form.get("username")
    if request.method =="POST":
        if len(username) < 1 or username is '':
            return "error please enter a usernam"
        if username in userslogged:
            return "username already exist"
        userslogged.append(username)
        session['username'] = username
        user = session['username']
        #to remember the user even after they close thier browser
        session.permanent = True
        return redirect("/")
    else:
        return render_template("signin.html")

@app.route("/signout", methods=["POST"])
def signout():
    #to loggout
    try:
        userslogged.remove(session['username'])
    except ValueError:
        pass
        #delete cookie
    session.clear()
    return redirect("/")

@app.route("/create", methods=['GET','POST'])
def create():
    newChannel = request.form.get('channel')
    if request.method =="POST":
        if newChannel in channelCreated:
            return "error please try again,this channel exist"
        channelCreated.append(newChannel)
        #instatiate a deque object that allows us to add or remove items from left or right
        channelMessages[newChannel] = deque()
        user=session['username']
        return render_template("channels.html", channels=channelCreated, user=user)
    else:
        return "try again"

@app.route("/channel<channel>")
def channel(channel):
    user=session['username']
    return render_template("messages.html", user=user)

@socketio.on("new message")
def message(data):
    message = data["message"]
    user=session['username']
    emit("announce message", {"message":message, "user":user}, broadcast=True)

@socketio.on('joined')
def joined():
    user=session['username']
    emit("announce joined", {"user":user}, broadcast=True)

if __name__ =='__main__':
    socketio.run(app)
