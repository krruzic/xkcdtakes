import sqlite3
from flask import g
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

import requests

DATABASE = 'reviews.db'
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM comics WHERE comic_id IN (SELECT comic_id FROM comics ORDER BY RANDOM() LIMIT 3)")
    rows = cur.fetchall()
    return render_template('home.html',rows=rows)

@app.route("/comic/<string:num>", methods=['GET'])
def getComic(num,h=""):
    if h=="":
        h = request.args.get("h")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from comics where comic_number = ?",[(num)])
    row = cur.fetchone()
    print(h)
    return render_template('comic.html',row=row,head=h)

@app.route("/add_comic", methods=['POST'])
def addComic():
    comic_num = request.form['comic']
    review_text= request.form['review_text']
    sub_text = request.form['sub_text']
    rating = request.form['rating']
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        print("test")
        cur.execute("SELECT EXISTS(SELECT 1 FROM comics WHERE comic_number=?)",[(comic_num)])
        print("fug")
        if cur.fetchone():
            print("exists!")
            return redirect(url_for('getComic',num=comic_num,h="COMIC ALREADY REVIEWED"))

    r  = requests.get("https://xkcd.com/"+comic_num+"/info.0.json")
    data = r.json()
    title = data["safe_title"]
    link = data["img"]
    print(data)
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO comics 
            (comic_number,title,review_text,sub_text,link,rating) 
            VALUES (?,?,?,?,?,?)""",
            (comic_num,title,review_text,sub_text,link,rating))
        conn.commit()
    return redirect(url_for('getComic',num=comic_num,h="HERE'S YOUR SHITTY COMIC"))


@app.route("/add", methods=['GET'])
def add():
    return render_template('add.html')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)
