import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from xhtml2pdf import pisa
import re

# --- Styling ---
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; }
        h1 { color: #2c3e50; }
        .judul {
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #2ecc71;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #27ae60;
        }
    </style>
""", unsafe_allow_html=True)

# --- Judul ---
st.markdown('<div class="judul">Penilaian Software Quality Assurance (SQA) - ISO 9126</div>', unsafe_allow_html=True)

# --- Data Responden ---
st.subheader("Data Responden")
col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("Nama Lengkap")
with col2:
    usia = st.number_input("Usia", min_value=10, max_value=100, step=1)

col3, col4 = st.columns(2)
with col3:
    aplikasi = st.selectbox("Pilih Nama Aplikasi", ["Tokopedia", "Shopee", "Lazada", "Blibli", "GoJek", "Grab", "Traveloka", "Agoda", "Tiktok"])
with col4:
    durasi = st.number_input("Sudah menggunakan berapa lama? (bulan)", min_value=1, max_value=240, step=1)

st.markdown("---")

# --- Fungsi dan Pertanyaan ---
def section(title):
    st.markdown(f'<h2>{title}</h2>', unsafe_allow_html=True)

questions = []
scores = []

def add_slider(label):
    score = st.slider(label, 1, 5, 3)
    questions.append(label)
    scores.append(score)
    return score

# --- Pertanyaan per Aspek ---
section("1️⃣ FUNCTIONALITY")
add_slider("Apakah fitur-fitur aplikasi sesuai dengan kebutuhan Anda sehari-hari?")
add_slider("Apakah fungsi utama aplikasi berjalan dengan benar tanpa error?")
add_slider("Apakah aplikasi memiliki fitur keamanan yang memadai (login, OTP, enkripsi)?")
add_slider("Apakah integrasi antar fitur (pembayaran, notifikasi, chat) berjalan dengan baik?")
add_slider("Apakah aplikasi memberikan informasi atau output yang akurat?")

section("2️⃣ RELIABILITY")
add_slider("Apakah aplikasi jarang mengalami error, hang, atau crash?")
add_slider("Apakah aplikasi tetap stabil digunakan dalam waktu lama?")
add_slider("Apakah aplikasi tetap berfungsi baik saat beban tinggi?")
add_slider("Apakah aplikasi cepat pulih jika terjadi gangguan sistem?")
add_slider("Apakah data pengguna tetap aman saat terjadi gangguan?")

section("3️⃣ USABILITY")
add_slider("Apakah tampilan antarmuka aplikasi mudah dipahami oleh pengguna baru?")
add_slider("Apakah navigasi menu jelas, konsisten, dan tidak membingungkan?")
add_slider("Apakah ukuran font, warna, ikon mudah dibaca?")
add_slider("Apakah Anda merasa nyaman menggunakan aplikasi dalam waktu lama?")
add_slider("Apakah aplikasi menyediakan panduan/pusat bantuan jika mengalami kesulitan?")

section("4️⃣ EFFICIENCY")
add_slider("Apakah aplikasi cepat dibuka dan tidak lambat saat digunakan?")
add_slider("Apakah konsumsi baterai aplikasi relatif hemat?")
add_slider("Apakah aplikasi tidak terlalu banyak menggunakan kuota data?")
add_slider("Apakah aplikasi tetap berjalan baik di perangkat spesifikasi rendah?")
add_slider("Apakah respon aplikasi tetap cepat meski digunakan bersama aplikasi lain?")

section("5️⃣ MAINTAINABILITY")
add_slider("Apakah aplikasi rutin diperbarui?")
add_slider("Apakah bug yang Anda laporkan cepat diperbaiki?")
add_slider("Apakah perubahan versi tidak menimbulkan masalah baru?")
add_slider("Apakah masukan pengguna sering diakomodasi?")
add_slider("Apakah catatan pembaruan mudah ditemukan dan dipahami?")

section("6️⃣ PORTABILITY")
add_slider("Apakah aplikasi berjalan lancar di berbagai OS?")
add_slider("Apakah aplikasi mudah diunduh dan diinstal?")
add_slider("Apakah tampilan aplikasi konsisten di berbagai ukuran layar?")
add_slider("Apakah data tetap aman dan tersinkronisasi saat ganti perangkat?")
add_slider("Apakah aplikasi mendukung berbagai bahasa?")

# --- Hasil ---
if st.button("Lihat Hasil Penilaian"):
    if not nama:
        st.warning("Mohon lengkapi nama terlebih dahulu.")
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

        st.subheader("📋 Hasil Penilaian")
        st.write(f"**Nama:** {nama}")
        st.write(f"**Usia:** {usia} tahun")
        st.write(f"**Aplikasi:** {aplikasi}")
        st.write(f"**Durasi Penggunaan:** {durasi} bulan")
        st.write(f"**Skor Rata-rata:** {rata_rata:.2f}")
        st.write(f"**Status Kelayakan:** {status}")
        st.write(f"**Rekomendasi:** {rekomendasi}")

        aspek = ["Functionality", "Reliability", "Usability", "Efficiency", "Maintainability", "Portability"]
        skor_aspek = [sum(scores[i*5:(i+1)*5]) / 5 for i in range(6)]

        # --- Grafik Matplotlib ---
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(aspek, skor_aspek, color='skyblue')
        ax.set_ylim(0, 5)
        ax.set_title("Grafik Penilaian SQA")
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()

        # --- Buat HTML ---
        html_detail = "".join([f"<p>{i+1}. {q} — Skor: {s}</p>" for i, (q, s) in enumerate(zip(questions, scores))])
        html_content = f"""
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1, h2 {{ text-align: center; }}
            .info p {{ line-height: 1.6; }}
        </style>
        </head>
        <body>
        <h1>Hasil Penilaian SQA - ISO 9126</h1>

        <h2>Informasi Responden</h2>
        <div class="info">
            <p><strong>Nama:</strong> {nama}</p>
            <p><strong>Usia:</strong> {usia} tahun</p>
            <p><strong>Aplikasi:</strong> {aplikasi}</p>
            <p><strong>Durasi:</strong> {durasi} bulan</p>
        </div>

        <h2>Rangkuman</h2>
        <div class="info">
            <p><strong>Skor Rata-rata:</strong> {rata_rata:.2f}</p>
            <p><strong>Status:</strong> {status}</p>
            <p><strong>Rekomendasi:</strong> {rekomendasi}</p>
        </div>

        <h2>Grafik</h2>
        <div style="text-align:center;">
            <img src="data:image/png;base64,{img_base64}" width="500"/>
        </div>

        <h2>Rincian Jawaban</h2>
        <div class="info">{html_detail}</div>
        </body>
        </html>
        """

        # --- Fungsi PDF ---
        def convert_html_to_pdf(source_html):
            result = BytesIO()
            pisa_status = pisa.CreatePDF(source_html, dest=result)
            return result.getvalue() if not pisa_status.err else None

        pdf_bytes = convert_html_to_pdf(html_content)
        if pdf_bytes:
            b64_pdf = base64.b64encode(pdf_bytes).decode()
            download_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Hasil_SQA_{nama}.pdf">📥 Download Hasil Penilaian (PDF)</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.error("❌ Gagal membuat PDF.")


<style>
    body {
        font-family: Arial, sans-serif;
        margin: 20px 40px;  /* margin atas bawah 20px, kiri kanan 40px */
        line-height: 1.2;    /* spasi antar baris rapat */
        font-size: 12pt;
    }
    h1, h2 {
        text-align: center;
        color: #333;
        margin-bottom: 10px;
    }
    .info, .detail {
        margin-left: 20px;
        margin-bottom: 10px;
    }
    p {
        margin: 5px 0;
    }
    .grafik {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>

