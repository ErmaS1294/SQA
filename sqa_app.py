import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
import pdfkit
import platform

# Konfigurasi wkhtmltopdf sesuai OS
if platform.system() == "Windows":
    config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
else:
    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")

# --- CSS Tampilan ---
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; }
        .stButton>button {
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            margin-top: 20px;
        }
        .stButton>button:hover {
            background-color: #27ae60;
        }
        .stSlider { margin-bottom: 25px; }
        .judul { font-size: 28px; font-weight: bold; color: #2c3e50; text-align: center; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# --- Judul ---
st.markdown('<div class="judul">Penilaian Software Quality Assurance (SQA) - ISO 9126</div>', unsafe_allow_html=True)

# --- Informasi Pengisi ---
st.subheader("Data Responden")
col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("Nama Lengkap")
with col2:
    usia = st.number_input("Usia", min_value=10, max_value=100, step=1)

col3, col4 = st.columns(2)
with col3:
    aplikasi = st.selectbox(
        "Pilih Nama Aplikasi",
        ["Tokopedia", "Shopee", "Lazada", "Blibli", "GoJek", "Grab", "Traveloka", "Agoda", "Tiktok"]
    )
with col4:
    durasi = st.text_input("Sudah menggunakan berapa lama ? (bulan)")

st.markdown("---")

# --- Pertanyaan SQA ---
def section(title):
    st.markdown(f'<h2>{title}</h2>', unsafe_allow_html=True)

questions = []
scores = []

def add_slider(label):
    score = st.slider(label, 1, 5, 3)
    questions.append(label)
    scores.append(score)
    return score

section("1️⃣ FUNCTIONALITY (Fungsionalitas)")
f1 = add_slider("Apakah fitur-fitur aplikasi sesuai dengan kebutuhan Anda sehari-hari?")
f2 = add_slider("Apakah fungsi utama aplikasi berjalan dengan benar tanpa error?")
f3 = add_slider("Apakah aplikasi memiliki fitur keamanan yang memadai (login, OTP, enkripsi)?")
f4 = add_slider("Apakah integrasi antar fitur (pembayaran, notifikasi, chat) berjalan dengan baik?")
f5 = add_slider("Apakah aplikasi memberikan informasi atau output yang akurat?")

section("2️⃣ RELIABILITY (Keandalan)")
r1 = add_slider("Apakah aplikasi jarang mengalami error, hang, atau crash?")
r2 = add_slider("Apakah aplikasi tetap stabil digunakan dalam waktu lama?")
r3 = add_slider("Apakah aplikasi tetap berfungsi baik saat beban tinggi (misalnya saat promo besar)?")
r4 = add_slider("Apakah aplikasi cepat pulih jika terjadi gangguan sistem?")
r5 = add_slider("Apakah data pengguna tetap aman saat terjadi gangguan?")

section("3️⃣ USABILITY (Kemudahan Penggunaan)")
u1 = add_slider("Apakah tampilan antarmuka aplikasi mudah dipahami oleh pengguna baru?")
u2 = add_slider("Apakah navigasi menu jelas, konsisten, dan tidak membingungkan?")
u3 = add_slider("Apakah ukuran font, warna, ikon mudah dibaca di berbagai kondisi?")
u4 = add_slider("Apakah Anda merasa nyaman menggunakan aplikasi dalam waktu lama?")
u5 = add_slider("Apakah aplikasi menyediakan panduan/pusat bantuan jika pengguna mengalami kesulitan?")

section("4️⃣ EFFICIENCY (Efisiensi Kinerja)")
e1 = add_slider("Apakah aplikasi cepat dibuka dan tidak lambat saat digunakan?")
e2 = add_slider("Apakah konsumsi baterai aplikasi relatif hemat?")
e3 = add_slider("Apakah aplikasi tidak terlalu banyak menggunakan kuota data internet?")
e4 = add_slider("Apakah aplikasi tetap berjalan baik di perangkat dengan spesifikasi rendah?")
e5 = add_slider("Apakah respon aplikasi tetap cepat meski digunakan bersama aplikasi lain?")

section("5️⃣ MAINTAINABILITY (Pemeliharaan)")
m1 = add_slider("Apakah aplikasi rutin diperbarui untuk memperbaiki bug atau menambah fitur baru?")
m2 = add_slider("Apakah bug atau kesalahan yang Anda laporkan cepat diperbaiki oleh pengembang?")
m3 = add_slider("Apakah perubahan versi aplikasi tidak menimbulkan masalah baru?")
m4 = add_slider("Apakah saran atau masukan pengguna sering diakomodasi oleh pengembang?")
m5 = add_slider("Apakah catatan pembaruan (changelog) mudah ditemukan dan dipahami?")

section("6️⃣ PORTABILITY (Portabilitas)")
p1 = add_slider("Apakah aplikasi berjalan lancar di berbagai versi OS (Android, iOS)?")
p2 = add_slider("Apakah aplikasi mudah diunduh dan diinstal di berbagai perangkat?")
p3 = add_slider("Apakah tampilan aplikasi tetap konsisten di berbagai ukuran layar?")
p4 = add_slider("Apakah data tetap aman dan tersinkronisasi saat Anda berganti perangkat?")
p5 = add_slider("Apakah aplikasi mendukung berbagai bahasa sesuai kebutuhan pengguna?")

# --- Tombol Hasil ---
if st.button("Lihat Hasil Penilaian"):
    if not nama or not durasi:
        st.warning("Mohon lengkapi semua data diri terlebih dahulu.")
    else:
        total_skor = sum(scores)
        rata_rata = total_skor / len(scores)

        if rata_rata >= 4:
            status = "Layak"
            rekomendasi = "Aplikasi sangat layak digunakan. Pertahankan kualitas!"
        elif rata_rata >= 3:
            status = "Cukup Layak"
            rekomendasi = "Beberapa aspek perlu ditingkatkan."
        else:
            status = "Tidak Layak"
            rekomendasi = "Aplikasi butuh banyak perbaikan."

        st.success("Penilaian Berhasil!")

        st.subheader("📋 Hasil Penilaian SQA")
        st.write(f"**Nama Pengisi:** {nama}")
        st.write(f"**Usia:** {usia} tahun")
        st.write(f"**Aplikasi Dinilai:** {aplikasi}")
        st.write(f"**Durasi Penggunaan:** {durasi}")
        st.write(f"**Skor Rata-rata:** {rata_rata:.2f} / 5.00")
        st.write(f"**Status Kelayakan:** {status}")
        st.write(f"**Rekomendasi:** {rekomendasi}")

        st.markdown("---")
        st.subheader("📊 Rincian Jawaban dan Skor")
        for i in range(len(questions)):
            st.write(f"{i+1}. {questions[i]} — Skor: {scores[i]}")

        aspek = ["Functionality", "Reliability", "Usability", "Efficiency", "Maintainability", "Portability"]
        skor_aspek = [
            sum(scores[0:5]) / 5,
            sum(scores[5:10]) / 5,
            sum(scores[10:15]) / 5,
            sum(scores[15:20]) / 5,
            sum(scores[20:25]) / 5,
            sum(scores[25:30]) / 5,
        ]
        df = pd.DataFrame({"Aspek": aspek, "Skor": skor_aspek})

        fig = px.bar(df, x="Aspek", y="Skor", color="Skor", title="Grafik Penilaian SQA", range_y=[0,5])
        st.plotly_chart(fig)

        pio.write_image(fig, "grafik_sqa.png")
        with open("grafik_sqa.png", "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()

        html_detail = "".join([f"<p>{i+1}. {q} — Skor: {s}</p>" for i, (q, s) in enumerate(zip(questions, scores))])

        html_content = f"""
        <html>
        <head>
        <meta charset=\"UTF-8\">
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1, h2 {{ text-align: center; color: #333; }}
            .info {{ white-space: pre; margin-left: 50px; font-family: monospace; }}
            .grafik {{ text-align: center; margin-top: 20px; }}
        </style>
        </head>
        <body>
        <h1>Hasil Penilaian SQA - ISO 9126</h1>

        <h2>Informasi Pengisi</h2>
        <div class="info">
        Nama         : {nama}
        Usia         : {usia}
        Aplikasi     : {aplikasi}
        Durasi       : {durasi}
        </div>

        <h2>Hasil Penilaian</h2>
        <div class="info">
        Skor Rata-rata  : {rata_rata:.2f}
        Status          : {status}
        Rekomendasi     : {rekomendasi}
        </div>

        <h2>Rincian Jawaban</h2>
        <div class="info">
        {html_detail}
        </div>

        <h2>Grafik</h2>
        <div class="grafik">
            <img src="data:image/png;base64,{img_base64}" width="600"/>
        </div>
        </body>
        </html>
        """

        with open("hasil_sqa.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        pdfkit.from_file("hasil_sqa.html", "Hasil_SQA.pdf", configuration=config)

        with open("Hasil_SQA.pdf", "rb") as f:
            pdf_bytes = f.read()
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="Hasil_SQA_{aplikasi}_{nama}.pdf">📥 Download Hasil Penilaian PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
