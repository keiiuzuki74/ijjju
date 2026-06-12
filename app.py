from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Server Online"

@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (name, email, code)
        VALUES (%s,%s,%s)
    """, (
        data["name"],
        data["email"],
        data["code"]
    ))

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)