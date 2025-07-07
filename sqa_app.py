import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
from fpdf import FPDF

# Pastikan kaleido sudah ada di requirements.txt!
# pip install kaleido

# --- CSS Tampilan ---
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; }
        h1 { color: #2c3e50; text-align: center; }
        h2 { color: #34495e; text-align: center; }
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
        .info { white-space: pre; margin-left: 50px; font-family: monospace; }
        .grafik { text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- Judul ---
st.title("Penilaian Software Quality Assurance (SQA) - ISO 9126")

# --- Data Responden ---
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
    durasi = st.text_input("Sudah menggunakan berapa lama? (misal: 6 bulan)")

st.markdown("---")

# --- Section Helper ---
def section(title):
    st.markdown(f'<h2>{title}</h2>', unsafe_allow_html=True)

# --- Pertanyaan ---
section("1️⃣ FUNCTIONALITY")
f1 = st.slider("Fitur sesuai kebutuhan?", 1, 5, 3)
f2 = st.slider("Fungsi utama tanpa error?", 1, 5, 3)
f3 = st.slider("Fitur keamanan memadai?", 1, 5, 3)
f4 = st.slider("Integrasi fitur berjalan baik?", 1, 5, 3)

section("2️⃣ RELIABILITY")
r1 = st.slider("Jarang crash?", 1, 5, 3)
r2 = st.slider("Stabil digunakan lama?", 1, 5, 3)
r3 = st.slider("Mampu beban tinggi?", 1, 5, 3)
r4 = st.slider("Cepat pulih saat gangguan?", 1, 5, 3)

section("3️⃣ USABILITY")
u1 = st.slider("Antarmuka mudah dipahami?", 1, 5, 3)
u2 = st.slider("Navigasi jelas?", 1, 5, 3)
u3 = st.slider("Font & ikon nyaman?", 1, 5, 3)
u4 = st.slider("Tersedia panduan?", 1, 5, 3)

section("4️⃣ EFFICIENCY")
e1 = st.slider("Cepat dibuka?", 1, 5, 3)
e2 = st.slider("Baterai hemat?", 1, 5, 3)
e3 = st.slider("Data efisien?", 1, 5, 3)
e4 = st.slider("Bekerja di low-spec?", 1, 5, 3)

section("5️⃣ MAINTAINABILITY")
m1 = st.slider("Rutin update?", 1, 5, 3)
m2 = st.slider("Bug cepat diperbaiki?", 1, 5, 3)
m3 = st.slider("Update tidak menimbulkan masalah?", 1, 5, 3)
m4 = st.slider("Feedback ditindaklanjuti?", 1, 5, 3)

section("6️⃣ PORTABILITY")
p1 = st.slider("Berjalan di berbagai OS?", 1, 5, 3)
p2 = st.slider("Mudah dipasang di perangkat?", 1, 5, 3)
p3 = st.slider("Tampilan konsisten?", 1, 5, 3)
p4 = st.slider("Data aman saat pindah?", 1, 5, 3)

# --- Tombol Proses ---
if st.button("Lihat Hasil Penilaian"):
    if not nama or not durasi:
        st.warning("Mohon lengkapi data diri terlebih dahulu.")
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
        st.markdown(f"""
            <div class="info">
Nama           : {nama}
Usia           : {usia}
Aplikasi       : {aplikasi}
Durasi         : {durasi}

Skor Rata-rata : {rata_rata:.2f}
Status         : {status}
Rekomendasi    : {rekomendasi}
            </div>
        """, unsafe_allow_html=True)

        # --- Grafik ---
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
        fig = px.bar(df, x="Aspek", y="Skor", color="Skor", range_y=[0, 5],
                     title="Grafik Penilaian SQA")
        st.plotly_chart(fig)

        # --- Simpan grafik ke base64 TANPA tulis file ---
        img_bytes = fig.to_image(format="png")  # Perlu kaleido
        img_base64 = base64.b64encode(img_bytes).decode()

        # --- PDF dengan fpdf ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hasil Penilaian SQA - ISO 9126", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Nama           : {nama}", ln=True)
        pdf.cell(200, 10, txt=f"Usia           : {usia}", ln=True)
        pdf.cell(200, 10, txt=f"Aplikasi       : {aplikasi}", ln=True)
        pdf.cell(200, 10, txt=f"Durasi         : {durasi}", ln=True)
        pdf.cell(200, 10, txt=f"Skor Rata-rata : {rata_rata:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Status         : {status}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Rekomendasi    : {rekomendasi}")

        pdf_file = "Hasil_SQA.pdf"
        pdf.output(pdf_file)

        with open(pdf_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_file}">📥 Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

        # --- Tampilkan grafik inline dengan base64 di HTML (opsional) ---
        st.markdown(f'<div class="grafik"><img src="data:image/png;base64,{img_base64}" width="600"/></div>', unsafe_allow_html=True)
