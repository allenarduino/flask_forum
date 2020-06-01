from flask import Flask,render_template,session,redirect,request,flash,url_for,jsonify,make_response,json
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta
import os
import io
import html
import base64
import pymysql
import hashlib
import sqlite3
#import base64
import jwt

db=pymysql.connect(host='localhost',user='root',password='',database='Forum',cursorclass=pymysql.cursors.DictCursor)
cursor=db.cursor()


#db=sqlite3.connect('Forum.db',check_same_thread=False)

#cursor=db.cursor()






app=Flask(__name__)
CORS(app)

############Uploaded files eg. image
UPLOAD_FOLDER="./static"
ALLOWED_EXTENSIONS=set(["jpeg","jpg","png"])
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"]=ALLOWED_EXTENSIONS

app.secret_key="eeeeertbmbmmmmmmmmmmm"



@app.route("/admin", methods=["GET"])
def admin():
    if request.method=="GET":
        return render_template("adminsignup.html")
    












@app.route('/adminsignup',methods=["POST","GET"])
def adminsignup():
    if request.method=='POST':
        name=request.form["name"]
        email=request.form['email']
        password=request.form['password']
        sql="SELECT email from admin WHERE email=%s"
        data=email
        result=cursor.execute(sql,data)
        account=cursor.fetchone()
        
        
        if account:
            return jsonify({"error":"User with email already exists!"})
        else:
            admin_img="slider-1.jpg"
            coverphoto="dmitri-popov-326976.jpg"
            bio="My bio"
             
            sql="INSERT INTO admin(name,email,password,admin_img,coverphoto,bio) VALUES (%s,%s,%s,%s,%s,%s)"
            data=(name,email,password,admin_img,coverphoto,bio)
            
            cursor.execute(sql,data)
            db.commit()  
            
            return render_template("adminlogin.html")
              
        


@app.route('/adminlogin', methods=["POST","GET"])
def adminlogin():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        sql="SELECT* FROM admin WHERE email=%s AND password=%s"
        data=(email,password)
        cursor.execute(sql,data)
        account=cursor.fetchone()
        
        if account:
            admin_id=account["id"]
            session["admin_id"]=admin_id
            email=account["email"]
            return  render_template("adminprofile")
            

        else:
            
            return jsonify({"error":"Invalid credentials"})
       


#########################Users signup and login                           

@app.route("/join", methods=["GET"])
def join():
    if request.method=="GET":
        return render_template("signup.html")

@app.route("/loginpage",methods=["GET"])
def loginpage():
    if request.method=="GET":
        return render_template("login.html")




@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        sql="SELECT email from users WHERE email=%s"
        data=email
        result=cursor.execute(sql,data)
        account=cursor.fetchone()
        
        
        if account:
            return jsonify({"error":"User with email already exists!"})
        else:
            user_img="slider-1.jpg"
            coverphoto="slider-1-1600x900.jpg"
            bio="My bio"
             
            sql="INSERT INTO users(name,email,password,user_img,coverphoto,bio) VALUES (%s,%s,%s,%s,%s,%s)"
            data=(name,email,password,user_img,coverphoto,bio)
            
            cursor.execute(sql,data)
            db.commit()  
            
            return jsonify({"message":"You are sucessfully registered"})
              
        
                


@app.route('/login', methods=["POST","GET"])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        sql="SELECT* FROM users WHERE email=%s AND password=%s"
        data=(email,password)
        cursor.execute(sql,data)
        account=cursor.fetchone()
        
        
        if account:
            user_id=account["id"]
            session["user_id"]=user_id
            session.permanent=True
            email=account["email"]
            return jsonify({"message":"Sucessfully logged in"})
            

        else:
            return jsonify({"error":"Invalid Credentials"})
            
            
       

            
            
######################################Create post

@app.route("/createpostpage")
def createpostpage():
    if request.method=="GET":
        return render_template("createpost.html")







@app.route("/createpost/",methods=["POST","GET"])
def createpost():
    if request.method=="POST":
        title=request.form["title"]
        file=request.files["file"]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(file.filename)))
        post_img= file.filename 
        user_id=session["user_id"]

        sql="INSERT INTO posts(title,user_id,post_img) VALUES (%s,%s,%s)"
        data=(title,user_id,post_img)
        cursor.execute(sql,data)
        db.commit()
        return redirect(url_for("sucess"))



 
@app.route('/', methods=["GET"])
def showposts():
    if request.method=='GET':
        sql='SELECT posts.id,posts.title,posts.post_img,posts.created_at,posts.user_id,(SELECT COUNT(*) FROM comments WHERE comments.post_id=posts.id) as totalcomments,users.user_img,users.name,users.id FROM posts,users WHERE users.id=posts.user_id ORDER BY posts.created_at DESC'
        cursor.execute(sql)
        posts=cursor.fetchall()
        return render_template("home.html", posts=posts)        


        


#######################Profile

@app.route("/myprofile/", methods=["GET"])
def myprofile():
    if request.method=="GET":
        user_id=session['user_id']
        sql="SELECT users.name,users.coverphoto,users.user_img,users.bio FROM users WHERE users.id=%s"
        data=user_id
        cursor.execute(sql,data)
        profile=cursor.fetchall()
        return render_template("myprofile.html",profile=profile)
        


@app.route("/sucess",methods=["GET"])
def sucess():
    return render_template("sucess.html")





@app.route("/editprofilepage",methods=["GET"])
def editprofile():
    return render_template("editprofile.html")




@app.route("/update_profile_img/",methods=["POST"])
def update_profile_img():
    user_id=session['user_id']
    file=request.files["file"]
    file.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(file.filename)))
    user_img= file.filename 
              
    sql="UPDATE users SET user_img=%s WHERE users.id=%s"
    data=(user_img,user_id)
    cursor.execute(sql,data)
    db.commit
    return redirect(url_for("myprofile"))



@app.route("/update_coverphoto/",methods=["POST"])
def update_coverphoto():
    user_id=session['user_id']
    file=request.files["file"]
    file.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(file.filename)))
    coverphoto= file.filename 
              
    sql="UPDATE users SET coverphoto=%s WHERE users.id=%s"
    data=(coverphoto,user_id)
    cursor.execute(sql,data)
    db.commit
    return redirect(url_for("myprofile"))







@app.route("/update_name/",methods=["POST"])
def update_name():
    user_id=session['user_id']
    
    name=request.form["name"]          
    sql="UPDATE users SET name=%s WHERE users.id=%s"
    data=(name,user_id)
    cursor.execute(sql,data)
    db.commit
    return redirect(url_for("myprofile"))



@app.route("/update_bio/",methods=["POST"])
def update_bio():
    user_id=session['user_id']
    
    bio=request.form["bio"]          
    sql="UPDATE users SET bio=%s WHERE users.id=%s"
    data=(bio,user_id)
    cursor.execute(sql,data)
    db.commit
    return redirect(url_for("myprofile"))





@app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect(url_for("loginpage"))




########Single post
@app.route("/singlepost", methods=["GET"])
def singlepost():
    if request.method=="GET":
        post_id=request.args.get("postId")
        sql='SELECT* FROM posts,users WHERE posts.id=%s AND users.id=posts.user_id'
        data=post_id
        cursor.execute(sql,data)
        singlepost=cursor.fetchall()
        return render_template("singlepost.html",singlepost=singlepost)



########Delete post

@app.route("/deletepost", methods=["POST","GET"])
def deletepost():
    post_id=request.args.get("postId")
    sql="DELETE FROM posts WHERE posts.id=%s"
    data=(post_id)
    cursor.execute(sql,data)
    db.commit()
    return redirect(url_for("showposts"))



       

   

        
@app.route("/user",methods=["GET"])
def showprofile():
    if request.method=="GET":
        user_id=request.args.get("userId")
        sql="SELECT users.id,users.name,users.coverphoto,users.user_img,users.bio FROM users WHERE users.id=%s"
        data=user_id
        cursor.execute(sql,data)
        userprofile=cursor.fetchall()
        return render_template("userprofile.html",userprofile=userprofile)


@app.route("/createcomment",methods=["POST"])
def createcomment():
    if request.method=="POST":
        user_id=session["user_id"]
        post_id=request.args.get("postId")
        title=request.form["title"]
        sql="INSERT INTO comments(title,user_id,post_id) VALUES (%s,%s,%s)"
        data=(title,user_id,post_id)
        cursor.execute(sql,data)
        db.commit()
        return  redirect(url_for("commentsucess"))
    
@app.route("/commentsucess",methods=["GET"])
def commentsucess():
    if request.method=="GET":
        return render_template("commentsucess.html")

    
    

       




@app.route("/showcomments",methods=["GET"])
def showcomments():
    post_id=request.args.get("postId")
    sql="SELECT* FROM comments,users WHERE users.id=comments.user_id AND comments.post_id=%s"
    data=post_id
    cursor.execute(sql,data)
    comments=cursor.fetchall()
    return render_template("showcomments.html",comments=comments)





@app.route("/deletecomment")
def deletecomment():
    comment_id=request.args.get("commentId")
    sql="DELETE FROM comments WHERE comments.id=%s"
    data=comment_id
    cursor.execute(sql,data)
    db.commit()
    return redirect(url_for("showposts"))







if __name__=="__main__":
    app.run(debug='true')
