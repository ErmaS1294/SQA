import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
import pdfkit
import platform

# Konfigurasi wkhtmltopdf sesuai OS
if platform.system() == "Windows":
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
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

section("1️⃣ FUNCTIONALITY (Fungsionalitas)")
f1 = st.slider("Apakah fitur aplikasi sesuai dengan kebutuhan pengguna?", 1, 5, 3)
f2 = st.slider("Apakah fungsi utama aplikasi berjalan tanpa error?", 1, 5, 3)
f3 = st.slider("Apakah aplikasi memiliki fitur keamanan yang memadai?", 1, 5, 3)
f4 = st.slider("Apakah integrasi fitur berjalan baik?", 1, 5, 3)

section("2️⃣ RELIABILITY (Keandalan)")
r1 = st.slider("Apakah aplikasi jarang mengalami crash?", 1, 5, 3)
r2 = st.slider("Apakah aplikasi stabil digunakan lama?", 1, 5, 3)
r3 = st.slider("Apakah mampu menangani beban tinggi?", 1, 5, 3)
r4 = st.slider("Apakah cepat pulih saat gangguan?", 1, 5, 3)

section("3️⃣ USABILITY (Kemudahan Penggunaan)")
u1 = st.slider("Apakah antarmuka mudah dipahami?", 1, 5, 3)
u2 = st.slider("Apakah navigasi menu jelas?", 1, 5, 3)
u3 = st.slider("Apakah font & ikon nyaman dibaca?", 1, 5, 3)
u4 = st.slider("Apakah tersedia panduan?", 1, 5, 3)

section("4️⃣ EFFICIENCY (Efisiensi Kinerja)")
e1 = st.slider("Apakah aplikasi cepat dibuka?", 1, 5, 3)
e2 = st.slider("Apakah konsumsi baterai hemat?", 1, 5, 3)
e3 = st.slider("Apakah penggunaan data efisien?", 1, 5, 3)
e4 = st.slider("Apakah bekerja di perangkat low-spec?", 1, 5, 3)

section("5️⃣ MAINTAINABILITY (Pemeliharaan)")
m1 = st.slider("Apakah aplikasi rutin diperbarui?", 1, 5, 3)
m2 = st.slider("Apakah bug cepat diperbaiki?", 1, 5, 3)
m3 = st.slider("Apakah update tidak menimbulkan masalah baru?", 1, 5, 3)
m4 = st.slider("Apakah feedback ditindaklanjuti?", 1, 5, 3)

section("6️⃣ PORTABILITY (Portabilitas)")
p1 = st.slider("Berjalan di berbagai OS?", 1, 5, 3)
p2 = st.slider("Mudah dipasang di perangkat?", 1, 5, 3)
p3 = st.slider("Tampilan konsisten di berbagai layar?", 1, 5, 3)
p4 = st.slider("Data aman saat pindah perangkat?", 1, 5, 3)

# --- Tombol Hasil ---
if st.button("Lihat Hasil Penilaian"):
    if not nama or not durasi:
        st.warning("Mohon lengkapi semua data diri terlebih dahulu.")
    else:
        total_skor = sum([
            f1, f2, f3, f4,
            r1, r2, r3, r4,
            u1, u2, u3, u4,
            e1, e2, e3, e4,
            m1, m2, m3, m4,
            p1, p2, p3, p4
        ])
        rata_rata = total_skor / 24

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

        # Grafik
        aspek = ["Functionality", "Reliability", "Usability", "Efficiency", "Maintainability", "Portability"]
        skor_aspek = [
            (f1+f2+f3+f4)/4,
            (r1+r2+r3+r4)/4,
            (u1+u2+u3+u4)/4,
            (e1+e2+e3+e4)/4,
            (m1+m2+m3+m4)/4,
            (p1+p2+p3+p4)/4
        ]
        df = pd.DataFrame({"Aspek": aspek, "Skor": skor_aspek})

        fig = px.bar(df, x="Aspek", y="Skor", color="Skor",
                     title="Grafik Penilaian SQA",
                     range_y=[0,5])
        st.plotly_chart(fig)

        # Tambahkan link download PDF (proses seperti script awal kamu)
        # ...



    # --- Simpan grafik & encode Base64 ---
    pio.write_image(fig, "grafik_sqa.png")
    with open("grafik_sqa.png", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    # --- Buat HTML dengan gambar embed Base64 ---
    html_content = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ text-align: center; color: #333; }}
        h2 {{ text-align: center; color: #333; }}
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

    <h2>Grafik</h2>
    <div class="grafik">
        <img src="data:image/png;base64,{img_base64}" width="600"/>
    </div>
    </body>
    </html>
    """

    # Simpan HTML
    with open("hasil_sqa.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Generate PDF
    pdfkit.from_file("hasil_sqa.html", "Hasil_SQA.pdf", configuration=config)

    # Buat link download PDF
    with open("Hasil_SQA.pdf", "rb") as f:
        pdf_bytes = f.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="Hasil_SQA_{aplikasi}_{nama}.pdf">📥 Download Hasil Penilaian PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
