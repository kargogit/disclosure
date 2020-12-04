from flask import Flask, render_template, request, redirect
import json
import re
import os

app = Flask( __name__ )
userData = {}
genreList = ["Entertainment", "Financial", "Politics", "Sports", "Technology", "Health", "Others"]
genderList = ["Male", "Female", "Other"]

@app.route( "/" )
def Index():
    newsData = json.load(  open( file = "ShowcaseDataset.json", mode = 'r', encoding = "utf-8", errors = "ignore" )  )
    if( userData ):
        return render_template( "UserIndex.html", newsData = newsData, userData = userData )
    else:
        return render_template( "FreshIndex.html", newsData = newsData )

@app.route( "/Register", methods = ["GET"] )
def getRegistrForm():
    return render_template( "Register.html" )

@app.route( "/Register", methods = ["POST"] )
def submitRegistrForm():
    global userData
    userData["firstName"] = request.form.get("firstName")
    if( not userData["firstName"] ):
        return render_template( "Failure.html", Parameter = "First Name" )
    userData["lastName"] = request.form.get("lastName")
    if( not userData["lastName"] ):
        return render_template( "Failure.html", Parameter = "Last Name" )
    userData["Email"] = request.form.get("Email")
    EmailMatch = re.search( "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$", userData["Email"] )
    if( not EmailMatch ):
        return render_template( "Failure.html", Parameter = "Email" )
    Password = request.form.get("Password")
    rePassword = request.form.get("rePassword")
    if(  Password and rePassword and ( Password == rePassword )  ):
        userData["Password"] = Password
    userData["DOB"] = request.form.get("DOB")
    if( not userData["DOB"] ):
        return render_template( "Failure.html", Parameter = "Date Of Birth" )
    userData["Gender"] = request.form.get("Gender")
    userData["allowedGenres"] = genreList
    userDataPath = os.path.join( r"UserAccounts", userData["Email"] + ".json" )
    with open( file = userDataPath, mode = 'w' ) as filePointer:
        json.dump( userData, filePointer )
    
    return redirect( "/" )

@app.route( "/Login", methods = ["GET"] )
def getLoginForm():
    return render_template( "Login.html" )

@app.route( "/Login", methods = ["POST"] )
def submitLoginForm():
    global userData
    Email = request.form.get("Email")
    Password = request.form.get("Password")
    userAccList = os.listdir( "UserAccounts" )
    userData = {}
    if( Email + ".json" in userAccList ):
        userDataPath = os.path.join( r"UserAccounts", Email + ".json" )
        userData = json.load(  open( file = userDataPath, mode = 'r', encoding = "utf-8", errors = "ignore" )  )
        if( userData["Password"] != Password ):
            userData = {}
    return redirect( "/" )

@app.route( "/Logout" )
def Logout():
    global userData
    userData = {}
    return redirect( "/" )

@app.route( "/UserSettings", methods = ["GET"] )
def getSettings():
    return render_template( "UserSettings.html", userData = userData, genreList = genreList, genderList = genderList )

@app.route( "/UserSettings", methods = ["POST"] )
def submitSettings():
    global userData
    userData["firstName"] = request.form.get( "firstName" )
    userData["lastName"] = request.form.get( "lastName" )
    userData["DOB"] = request.form.get( "DOB" )
    userData["Gender"] = request.form.get( "Gender" )
    userData["allowedGenres"] = request.form.getlist( "Genres" )
    newPassword = request.form.get( "newPassword" )
    if( newPassword ):
        oldPassword = request.form.get("oldPassword")
        if( userData["Password"] == oldPassword ):
            if(  newPassword == request.form.get( "reNewPassword" )  ):
                userData[ "Password" ] = newPassword
                userDataPath = os.path.join( r"UserAccounts", userData["Email"] + ".json" )
                with open( file = userDataPath, mode = 'w' ) as filePointer:
                    json.dump( userData, filePointer )
                return redirect( "/" )
        return render_template( "Failure.html", Parameter = "Password" )
    else:
        return redirect( "/" )