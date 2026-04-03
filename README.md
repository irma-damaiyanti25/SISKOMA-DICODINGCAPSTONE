# SISKOMA DICODING CAPSTONE

## Deskripsi Proyek

Project ini merupakan aplikasi berbasis **Flask** yang mengintegrasikan **Machine Learning (SVM + TF-IDF)** dan **Large Language Model (LLM)** untuk melakukan analisis sentimen serta memberikan rekomendasi otomatis berbasis AI.

Pengguna dapat melakukan input teks, kemudian sistem akan:

1. Memprediksi sentimen (positif, negatif, netral)
2. Menghasilkan rekomendasi cerdas menggunakan LLM

---

## Teknologi yang Digunakan

* Python 3
* Flask
* Scikit-learn (SVM, TF-IDF)
* Joblib
* OpenAI API (custom LLM OPEN AI)
* Gunicorn
* Railway (Deployment)
* HTML, CSS

---

## Struktur Project

```bash
.
├── dataset/              # Dataset training
├── model/                # Script training model
├── save_model/           # Model hasil training (.pkl)
│   ├── model_svm_tuned.pkl
│   └── tfidf.pkl
├── static/css/           # Styling
├── templates/            # HTML Templates
├── app.py                # Main Flask App
├── requirements.txt
├── .gitignore
├── .slugignore
```

---

## Cara Kerja Sistem

1. Input teks dari user
2. Teks diubah menggunakan **TF-IDF**
3. Diprediksi menggunakan **model SVM yang sudah di hyperparameter tuning**
4. Hasil sentimen dikirim ke **LLM**
5. LLM menghasilkan rekomendasi berbasis konteks

Implementasi:

* Model ML diupload menggunakan `joblib`
* LLM menggunakan OpenAI-compatible API custom API

Implementasi LLM: 

---

## Integrasi LLM (OpenAI Compatible)

Project ini menggunakan API berbasis OpenAI dengan konfigurasi custom endpoint:

```python
client = OpenAI(
    api_key=API_KEY,
    base_url="--"
)
```

Fungsi utama:

```python
def generate_recommendation(text, sentiment):
```

LLM digunakan untuk:

* Memberikan rekomendasi otomatis
* Menyusun kalimat yang natural
* Menambahkan informasi kontak

---

## Fitur Sistem untuk Admin

* Login & Register user
* Role-based access (Admin)
* Prediksi sentimen
* Rekomendasi otomatis berbasis AI
* Penyimpanan hasil prediksi
* Edit & delete data (admin only)
* Dashboard & laporan hasil

## Fitur Sistem User

* Login & Register user
* Role-based access (User)
* Prediksi sentimen
* Rekomendasi otomatis berbasis AI
* Penyimpanan hasil prediksi
* delete data
* Dashboard & laporan hasil

---

## Cara Menjalankan Secara Lokal

1. Clone repository

```bash
git clone https://github.com/imaCode95/SISKOMA-DICODINGCAPSTONE.git
cd SISKOMA-DICODINGCAPSTONE
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Setup environment variable

```bash
OPENAI_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

4. Jalankan aplikasi

```bash
python app.py
```

---

## Deployment (Railway)

Aplikasi telah dideploy menggunakan Railway.

```bash

https://siskoma-dicodingcapstone-production.up.railway.app/

```

---

## Endpoint Utama

* `/` → Login
* `/register` → Registrasi
* `/dashboard` → Dashboard
* `/predict` → Prediksi + rekomendasi AI
* `/laporan` → Data hasil
* `/edit/<id>` → Edit data (admin)
* `/delete/<id>` → Hapus data

---

## Academic Paper & Referensi (IEEE)

[1] F. Chollet, *Deep Learning with Python*, Manning Publications, 2018.
[2] Scikit-learn, “Machine Learning in Python,” 2024. [Online]. Available: https://scikit-learn.org/
[3] OpenAI, “GPT Models Documentation,” 2024. [Online]. Available: https://platform.openai.com/
[4] Flask Documentation, “Flask Official Documentation,” 2024. [Online]. Available: https://flask.palletsprojects.com/
[5] T. Joachims, “Text Categorization with Support Vector Machines,” 1998.
[6] C. D. Manning et al., “Introduction to Information Retrieval,” Cambridge University Press, 2008.
[7] Railway, “Railway Documentation,” 2024. [Online]. Available: https://docs.railway.app/

---
## Link Demo Website
* link : http://youtube.com/watch?v=QGjKoPneoN0&feature=youtu.be

---
## Link Presentasi
* link : https://www.youtube.com/watch?v=-lF2jGgpTBg
* link slide presentasi : https://www.canva.com/design/DAHFyk-htZ0/2Bz_b4wXKCUpmqiPnlNYmw/edit


## Author

Irma Damaiyanti

---

## Catatan

Project ini menggabungkan **Machine Learning** dan **Large Language Model (LLM)** untuk menghasilkan sistem rekomendasi berbasis sentimen yang lebih cerdas, interaktif, dan informatif.
