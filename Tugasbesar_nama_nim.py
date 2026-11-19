
import streamlit as st
import textwrap
from pathlib import Path

# ==========================================
# NIGHTWASH - LAUNDRY KILOAN
# ==========================================

st.set_page_config(
    page_title="NIGHTWASH | Laundry Kiloan",
    page_icon="🧺",
    layout="wide"
)

# ==========================================
# FUNGSI HTML
# ==========================================

def html(kode):
    st.markdown(
        textwrap.dedent(kode).strip(),
        unsafe_allow_html=True
    )


# ==========================================
# DESAIN CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top right, #183b65, transparent 35%),
        linear-gradient(145deg, #07111f, #101f35);
    color: white;
}

.block-container {
    max-width: 1050px;
    padding-top: 25px;
    padding-bottom: 40px;
}

/* HEADER */

.hero {
    background: linear-gradient(120deg, #10233e, #075b96);
    padding: 30px;
    border-radius: 22px;
    border: 1px solid #3299df;
    box-shadow: 0 8px 25px #00000055;
    margin-bottom: 22px;
}

.hero h1 {
    color: white;
    font-size: 43px;
    font-weight: 900;
    letter-spacing: 3px;
    margin: 0;
}

.hero p {
    color: #c5e6ff;
}

/* PANEL */

.panel {
    background: linear-gradient(145deg, #172b45, #0e1b2e);
    border: 1px solid #315778;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 5px 18px #00000030;
}

.panel h3 {
    color: #e4f3ff;
}

/* ANIME */

.anime-box {
    background:
        radial-gradient(circle, #235b8d, #10233e);
    border: 1px solid #4595ce;
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    min-height: 250px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.anime-character {
    font-size: 85px;
    margin: 10px;
}

.anime-box h3 {
    color: #8fd0ff;
    letter-spacing: 2px;
}

.anime-box p {
    color: #c0d9f0;
}

/* INPUT */

.stTextInput label,
.stNumberInput label {
    color: #e4f3ff !important;
    font-weight: bold !important;
}

.stTextInput input,
.stNumberInput input {
    background: #091729 !important;
    color: white !important;
    border: 1px solid #3987c2 !important;
    border-radius: 10px !important;
}

/* TOMBOL */

div.stButton > button {
    background: linear-gradient(100deg, #0864a7, #159de5);
    color: white;
    border: 1px solid #55baff;
    border-radius: 11px;
    min-height: 48px;
    font-weight: 800;
}

div.stButton > button:hover {
    background: linear-gradient(100deg, #1488d0, #39b5ff);
    color: white;
    border: 1px solid white;
}

/* METRIC */

[data-testid="stMetric"] {
    background: #0b1a2d;
    border: 1px solid #315779;
    border-radius: 13px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #b9d6ef !important;
}

[data-testid="stMetricValue"] {
    color: #66c2ff !important;
    font-weight: 800;
}

/* TOTAL BAYAR */

.total-box {
    background: linear-gradient(120deg, #07518c, #087fbd);
    border: 1px solid #68c8ff;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    margin-top: 15px;
    box-shadow: 0 5px 25px #007ac555;
}

.total-box h3 {
    color: #d9efff;
}

.total-box h1 {
    color: white;
    font-size: 42px;
    font-weight: 900;
    margin: 8px;
}

.total-box p {
    color: #d9efff;
}

/* FOOTER */

.footer {
    text-align: center;
    padding: 25px;
    margin-top: 30px;
    border-top: 1px solid #294969;
    color: #91b2d1;
    font-size: 13px;
}

.footer strong {
    color: #68bdff;
    font-size: 17px;
}

/* RUMUS */

[data-testid="stExpander"] {
    background: #14263d;
    border: 1px solid #315779;
    border-radius: 12px;
}

[data-testid="stExpander"] summary {
    color: white;
    font-weight: bold;
}

/* HP */

@media(max-width: 640px) {
    .hero {
        padding: 22px;
    }

    .hero h1 {
        font-size: 34px;
    }

    .anime-character {
        font-size: 65px;
    }

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNGSI PERHITUNGAN
# ==========================================

def rupiah(nilai):
    return "Rp " + f"{nilai:,.0f}".replace(",", ".")


def hitung_biaya(nim, berat):

    # Tarif berdasarkan digit terakhir NIM
    tarif = 5000 + (int(nim[-1]) * 500)

    # Menghitung seluruh digit genap
    jumlah_genap = sum(
        1 for digit in nim
        if int(digit) % 2 == 0
    )

    # Persentase diskon
    diskon = jumlah_genap

    # Menghitung biaya
    biaya_normal = berat * tarif

    potongan = biaya_normal * diskon / 100

    total = biaya_normal - potongan

    return {
        "tarif": tarif,
        "jumlah_genap": jumlah_genap,
        "diskon": diskon,
        "normal": biaya_normal,
        "potongan": potongan,
        "total": total
    }


# ==========================================
# SESSION STATE
# ==========================================

if "hasil" not in st.session_state:
    st.session_state.hasil = None

if "error" not in st.session_state:
    st.session_state.error = ""


def reset_aplikasi():
    st.session_state.nim = ""
    st.session_state.berat = 0
    st.session_state.hasil = None
    st.session_state.error = ""


# ==========================================
# HEADER APLIKASI
# ==========================================

html("""
<div class="hero">
    <p>PREMIUM LAUNDRY SERVICE</p>
    <h1>🌙 NIGHTWASH</h1>
    <h3 style="color:#b6e1ff;">LAUNDRY KILOAN</h3>
    <p>
        Bersih maksimal, praktis, dan terpercaya.
    </p>
    <p>⚡ SMART LAUNDRY CALCULATION SYSTEM</p>
</div>
""")


# ==========================================
# BAGIAN ANIME
# ==========================================

# Jika gambar anime tersedia di GitHub,
# aplikasi akan menampilkan gambar tersebut.

if Path("anime_laundry.png").exists():

    st.image(
        "anime_laundry.png",
        use_container_width=True
    )

else:

    html("""
    <div class="anime-box">
        <div class="anime-character">🧑🏻‍🦱🧥</div>
        <h3>NIGHTWASH CREW</h3>
        <p>Your Clothes, Our Priority.</p>
        <div style="font-size:35px;">🧺 ✦ 🌙</div>
    </div>
    """)


st.write("")


# ==========================================
# FORM INPUT
# ==========================================

html("""
<div class="panel">
    <h3>👤 DATA PELANGGAN</h3>
    <p style="color:#aac8e5;">
        Masukkan NIM dan berat cucian untuk
        menghitung biaya laundry.
    </p>
</div>
""")

nim = st.text_input(
    "NIM (10 digit angka)",
    max_chars=10,
    placeholder="Contoh: 2411001347",
    key="nim"
)

berat = st.number_input(
    "Berat Cucian (kg)",
    min_value=0,
    step=1,
    key="berat"
)


# ==========================================
# TOMBOL
# ==========================================

col1, col2 = st.columns(2)

with col1:

    tombol_hitung = st.button(
        "⚡ HITUNG BIAYA",
        use_container_width=True
    )

with col2:

    st.button(
        "↻ RESET",
        on_click=reset_aplikasi,
        use_container_width=True
    )


# ==========================================
# VALIDASI INPUT
# ==========================================

if tombol_hitung:

    st.session_state.hasil = None
    st.session_state.error = ""

    if len(nim) != 10 or not nim.isdigit():

        st.session_state.error = (
            "NIM tidak valid! Harus tepat 10 digit angka."
        )

    elif berat <= 0:

        st.session_state.error = (
            "Berat cucian harus lebih dari 0 kg!"
        )

    else:

        data = hitung_biaya(nim, int(berat))

        st.session_state.hasil = {
            "nim": nim,
            "berat": int(berat),
            "data": data
        }


# ==========================================
# PESAN KESALAHAN
# ==========================================

if st.session_state.error:
    st.error(st.session_state.error)


# ==========================================
# HASIL PERHITUNGAN
# ==========================================

if st.session_state.hasil:

    hasil = st.session_state.hasil

    data = hasil["data"]

    st.markdown("---")

    html("""
    <div class="panel">
        <h3>📊 RINCIAN PERHITUNGAN</h3>
        <p style="color:#aac8e5;">
            Hasil perhitungan biaya laundry pelanggan.
        </p>
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"NIM: {hasil['nim']}")

    with col2:
        st.info(f"Berat: {hasil['berat']} kg")

    kiri, kanan = st.columns(2)

    with kiri:

        st.metric(
            "💰 Tarif per kg",
            rupiah(data["tarif"])
        )

        st.metric(
            "📦 Biaya normal",
            rupiah(data["normal"])
        )

        st.metric(
            "🔢 Jumlah digit genap",
            f"{data['jumlah_genap']} digit"
        )

    with kanan:

        st.metric(
            "🏷️ Persen diskon",
            f"{data['diskon']}%"
        )

        st.metric(
            "✂️ Potongan",
            rupiah(data["potongan"])
        )

        st.metric(
            "🧾 Berat cucian",
            f"{hasil['berat']} kg"
        )

    # TOTAL PEMBAYARAN

    html(f"""
    <div class="total-box">
        <h3>💎 TOTAL PEMBAYARAN</h3>
        <h1>{rupiah(data["total"])}</h1>
        <p>
            Terima kasih telah menggunakan NIGHTWASH.
        </p>
    </div>
    """)


# ==========================================
# RUMUS PERHITUNGAN
# ==========================================

with st.expander("📖 LIHAT RUMUS PERHITUNGAN"):

    st.markdown("""
    **1. Tarif per kg**

    Rp5.000 + (digit terakhir NIM × Rp500)

    **2. Persen diskon**

    Jumlah digit genap dalam NIM × 1%

    **3. Biaya normal**

    Berat cucian × tarif per kg

    **4. Potongan**

    Persen diskon × biaya normal

    **5. Total bayar**

    Biaya normal − potongan
    """)


# ==========================================
# FOOTER
# ==========================================

html("""
<div class="footer">
    <strong>🌙 NIGHTWASH LAUNDRY</strong>
    <br><br>
    PYTHON & STREAMLIT PROJECT
    <br><br>
    Premium Laundry Calculation System
    <br>
    © 2026
</div>
""")
