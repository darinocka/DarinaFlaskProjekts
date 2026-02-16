from flask import Flask, render_template, redirect, request
import requests
import random
import sqlite3
import atexit

app = Flask(__name__)

genres = ["Action", "Adult", "Adventure", "Anime", "Children", "Comedy", "Crime", "DIY", "Drama", "Espionage", "Family", "Fantasy", "Food", "History",
"Horror", "Legal", "Medical", "Music", "Mystery", "Nature", "Romance", "Science-Fiction", "Sports", "Supernatural", "Thriller", "Travel", "War", "Western"]

def get_tv(x):
    response = requests.get("https://api.tvmaze.com/shows")
    if response.status_code != 200:
        return None
    show = response.json()
    filtered = [show for show in show if x in show["genres"]]
    if not filtered:
        return None
    return random.choice(filtered)

@app.route("/")
def index():
    return render_template("index.html", genres=genres)

@app.route("/dati", methods=["POST"])
def dati():
    name = request.form.get("name")
    if not name:
        return render_template("error.html")

    return render_template("izvele.html", name=name, genres=genres)

@app.route("/izvele", methods=["POST", "GET"])
def izvele():
    if request.method == "GET":
        return render_template("izvele.html", name="", genres=genres)
    
    name = request.form.get("name")
    genre = request.form.get("genre")

    if not genre:
        return render_template("error.html")

    if genre not in genres:
        return render_template("error.html")

    show = get_tv(genre)

    if not show:
        return render_template("error.html")

    return render_template("dati.html", name=name, show=show, genre=genre)

@app.route("/pievienot", methods=["POST"])
def pievienot():
    show_name = request.form.get("show_name")
    genre = request.form.get("genre")

    if not show_name or not genre:
        return render_template("error.html")

    conn = sqlite3.connect("./projekts/datubaze.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lietotaji (genre, show) VALUES (?, ?)", (genre, show_name))
    conn.commit()
    conn.close()

    return redirect("/saraksts")

@app.route("/another", methods=["POST"])
def another():
    genre = request.form.get("genre")
    name = request.form.get("name")

    if not genre:
        return render_template("error.html")

    show = get_tv(genre)

    if not show:
        return render_template("error.html")

    return render_template("dati.html", name=name, show=show, genre=genre)

@app.route("/saraksts")
def saraksts():
    conn = sqlite3.connect("./projekts/datubaze.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, show, genre FROM lietotaji")
    rows = cursor.fetchall()
    conn.close()

    return render_template("saraksts.html", shows=rows)


@app.route("/delete/<int:show_id>")
def delete_show(show_id):
    conn = sqlite3.connect("./projekts/datubaze.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lietotaji WHERE id = ?", (show_id,))
    conn.commit()
    conn.close()

    return redirect("/saraksts")


@app.route("/error")
def error():
    return render_template("error.html")

def clear_database():
    conn = sqlite3.connect("./projekts/datubaze.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lietotaji")
    conn.commit()
    conn.close()
atexit.register(clear_database)

if __name__ == "__main__":
    app.run(debug=True)