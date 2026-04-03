from flask import Flask, render_template, request, redirect, session
import joblib
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# =========================
# ENV SETUP
# =========================
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.koboillm.com/v1"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# =========================
# INIT APP
# =========================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret123")

# =========================
# LOAD MODEL (AMAN UNTUK SERVER)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "save_model", "model_svm_tuned.pkl")
tfidf_path = os.path.join(BASE_DIR, "save_model", "tfidf.pkl")

model = joblib.load(model_path)
tfidf = joblib.load(tfidf_path)

# =========================
# STORAGE USER + ROLE
# =========================
users = {
    "admin": {
        "password": "123",
        "role": "admin"
    }
}

# =========================
# STORAGE DATA
# =========================
data_hasil = []

# =========================
# FUNCTION AI
# =========================
def generate_recommendation(text, sentiment):

    if sentiment == "negatif":
        konteks = "Pengguna mengalami masalah."
    elif sentiment == "positif":
        konteks = "Pengguna merasa puas."
    else:
        konteks = "Pengguna netral."

    prompt = f"""
    Kamu adalah asisten AI untuk pengguna aplikasi.

    Teks:
    "{text}"

    Sentimen: {sentiment}
    Konteks: {konteks}

    Berikan saran singkat (2-3 kalimat), sederhana, dan ramah.

    Tambahkan di akhir:
    Contact WA: 083122898124
    Email: siskoma@sistemrekomendasi.com
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("ERROR API:", e)
        return "Rekomendasi tidak tersedia."

# =========================
# LOGIN
# =========================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]["password"] == password:
            session['user'] = username
            session['role'] = users[username]["role"]
            return redirect('/dashboard')

        return "Login gagal!"

    return render_template('login.html')

# =========================
# REGISTER
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return "Username sudah digunakan!"

        users[username] = {
            "password": password,
            "role": "user"
        }

        return redirect('/')

    return render_template('register.html')

# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    return render_template('dashboard.html')

# =========================
# PREDICT
# =========================
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        text = request.form['text']

        text_tfidf = tfidf.transform([text])
        pred = model.predict(text_tfidf)[0]

        rekomendasi = generate_recommendation(text, pred)

        now = datetime.now().strftime("%d-%m-%Y %H:%M")

        data_hasil.append({
            "text": text,
            "sentiment": pred,
            "rekomendasi": rekomendasi,
            "time": now,
            "user": session['user']
        })

        return render_template(
            'predict.html',
            prediction=pred,
            text=text,
            rekomendasi=rekomendasi
        )

    return render_template('predict.html')

# =========================
# LAPORAN
# =========================
@app.route('/laporan')
def laporan():
    if 'user' not in session:
        return redirect('/')

    return render_template('laporan.html', data=data_hasil)

# =========================
# DELETE
# =========================
@app.route('/delete/<int:index>')
def delete(index):
    if 'user' not in session:
        return redirect('/')

    if 0 <= index < len(data_hasil):
        data_hasil.pop(index)

    return redirect('/laporan')

# =========================
# EDIT (ADMIN ONLY)
# =========================
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if 'user' not in session:
        return redirect('/')

    if session.get('role') != 'admin':
        return "Akses ditolak!"

    if index >= len(data_hasil):
        return redirect('/laporan')

    if request.method == 'POST':
        text = request.form['text']
        rekomendasi_input = request.form['rekomendasi']

        text_tfidf = tfidf.transform([text])
        pred = model.predict(text_tfidf)[0]

        if rekomendasi_input.strip() == "":
            rekomendasi = generate_recommendation(text, pred)
        else:
            rekomendasi = rekomendasi_input

        data_hasil[index] = {
            "text": text,
            "sentiment": pred,
            "rekomendasi": rekomendasi,
            "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "user": session['user']
        }

        return redirect('/laporan')

    return render_template('edit.html', data=data_hasil[index], index=index)

# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# =========================
# RUN (RENDER READY)
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)