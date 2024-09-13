from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from functools import wraps
import os
import psycopg2
from psycopg2 import sql

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)

# 이벤트 상세 정보
event = {
    "name": "테크 혁신가 모임",
    "date": "2024-09-30",
    "time": "18:00",
    "location": "테크허브, 혁신 거리 123, 실리콘 밸리",
    "description": "최첨단 기술 강연과 업계 리더들과의 네트워킹을 위한 저녁 모임에 참여하세요!"
}

# Admin credentials (in a real-world scenario, use a more secure method)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            full_name VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html", event=event)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    full_name = data.get("fullName")

    if email and full_name:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO registrations (email, full_name) VALUES (%s, %s)", (email, full_name))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"success": True, "message": "등록이 성공적으로 완료되었습니다!"}), 200
        except psycopg2.IntegrityError:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "이미 등록된 이메일입니다."}), 400
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "등록 중 오류가 발생했습니다."}), 500
    else:
        return jsonify({"success": False, "message": "유효하지 않은 데이터가 제공되었습니다."}), 400

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template("admin_login.html", error="잘못된 로그인 정보입니다.")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

@app.route("/admin")
@login_required
def admin_panel():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT email, full_name FROM registrations")
    registrations = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin_panel.html", registrations=registrations)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
