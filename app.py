
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Deteksi Kesegaran Ikan Tuna", layout="centered")

# API Roboflow
ROBOFLOW_API_URL = "https://infer.roboflow.com/ikan-segar-detector-l3abz/1?api_key=WwHvvZp1bpdvIZWZN63u"

def show_title():
    st.markdown("""
    <h1 style='text-align: center; color: #2C3E50;'>Deteksi Kesegaran Ikan Tuna</h1>
    <p style='text-align: center; font-size: 18px; color: #34495E;'>Aplikasi Berbasis Pemrosesan Citra</p>
    """, unsafe_allow_html=True)

def landing_page():
    show_title()
    st.image("assets/landing.png", use_container_width=True)

    uploaded_file = st.file_uploader("📤 Unggah Gambar Ikan Tuna", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image_bytes = uploaded_file.read()
        st.image(image_bytes, caption="📷 Gambar yang Diupload", use_container_width=True)
        with st.spinner("🔍 Mendeteksi..."):
            try:
                response = requests.post(ROBOFLOW_API_URL, files={"file": image_bytes})
                result = response.json()

                if "predictions" in result and len(result["predictions"]) > 0:
                    pred = result["predictions"][0]
                    label = pred["class"]
                    conf = round(pred["confidence"] * 100, 2)
                    st.success(f"Hasil Deteksi: ✅ <b>{label}</b> dengan confidence <b>{conf}%</b>", icon="✅")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("riwayat.csv", "a") as f:
                        f.write(f"{now},{uploaded_file.name},{label},{conf}\n")
                else:
                    st.warning("❗ Tidak ada objek yang terdeteksi.")
            except Exception as e:
                st.error(f"Gagal menghubungi API Roboflow: {e}")

def login_admin():
    st.subheader("🔐 Login Admin")
    user = st.text_input("Username", placeholder="Masukkan username")
    pwd = st.text_input("Password", placeholder="Masukkan password", type="password")
    if st.button("Login"):
        if user == "admin" and pwd == "admin123":
            st.success("Login berhasil!")
            st.session_state["login"] = True
        else:
            st.error("Username atau password salah.")

def lihat_riwayat():
    st.subheader("📊 Riwayat Deteksi")
    try:
        df = pd.read_csv("riwayat.csv")
        st.dataframe(df, use_container_width=True)
    except:
        st.info("Belum ada data riwayat.")

# Navigasi
menu = st.sidebar.selectbox("📁 Menu Navigasi", ["🏠 Beranda", "🔐 Login Admin", "📊 Riwayat Deteksi"])

if menu == "🏠 Beranda":
    landing_page()
elif menu == "🔐 Login Admin":
    login_admin()
elif menu == "📊 Riwayat Deteksi":
    if st.session_state.get("login"):
        lihat_riwayat()
    else:
        st.warning("Silakan login sebagai admin untuk mengakses riwayat.")
