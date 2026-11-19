import streamlit as st

# ==========================================================
# TUGAS BESAR: APLIKASI PERHITUNGAN BIAYA LAUNDRY KILOAN
# ==========================================================

st.set_page_config(
    page_title="Aplikasi Biaya Laundry",
    page_icon="🧺",
    layout="centered"
)


# ---------------------- FUNGSI PROGRAM ----------------------

def hitung_biaya(nim, berat):
    """Menghitung tarif, diskon, biaya normal, potongan, dan total bayar."""
    digit_terakhir = int(nim[-1])
    tarif_per_kg = 5000 + (digit_terakhir * 500)

    jumlah_digit_genap = sum(1 for digit in nim if int(digit) % 2 == 0)
    persen_diskon = jumlah_digit_genap  # Setiap digit genap bernilai diskon 1%

    biaya_normal = berat * tarif_per_kg
    potongan = biaya_normal * persen_diskon / 100
    total_bayar = biaya_normal - potongan

    return {
        "tarif": tarif_per_kg,
        "jumlah_genap": jumlah_digit_genap,
        "diskon": persen_diskon,
        "biaya_normal": biaya_normal,
        "potongan": potongan,
        "total_bayar": total_bayar
    }


def rupiah(nilai):
    """Mengubah angka menjadi format mata uang Rupiah."""
    return "Rp " + f"{nilai:,.0f}".replace(",", ".")


def reset_form():
    """Mengosongkan input dan hasil perhitungan."""
    st.session_state.nim = ""
    st.session_state.berat = 1
    st.session_state.hasil = None
    st.session_state.pesan_error = ""


# ---------------------- INISIALISASI SESSION ----------------------

if "nim" not in st.session_state:
    st.session_state.nim = ""

if "berat" not in st.session_state:
    st.session_state.berat = 1

if "hasil" not in st.session_state:
    st.session_state.hasil = None

if "pesan_error" not in st.session_state:
    st.session_state.pesan_error = ""


# ---------------------- TAMPILAN APLIKASI ----------------------

st.title("🧺 Laundry Kiloan")
st.write("Aplikasi sederhana untuk menghitung biaya laundry kiloan.")

st.divider()

st.subheader("Data Pelanggan")

nim = st.text_input(
    "NIM (harus 10 digit angka)",
    key="nim",
    max_chars=10,
    placeholder="Contoh: 2411001347"
)

berat = st.number_input(
    "Berat cucian (kg)",
    key="berat",
    step=1
)

kolom_hitung, kolom_reset = st.columns(2)

with kolom_hitung:
    tombol_hitung = st.button(
        "🧮 Hitung Biaya",
        type="primary",
        use_container_width=True
    )

with kolom_reset:
    st.button(
        "🔄 Reset",
        on_click=reset_form,
        use_container_width=True
    )


# ---------------------- PROSES VALIDASI DAN PERHITUNGAN ----------------------

if tombol_hitung:
    st.session_state.hasil = None
    st.session_state.pesan_error = ""

    # Validasi NIM: harus tepat 10 karakter dan semuanya angka.
    if len(nim) != 10 or not nim.isdigit():
        st.session_state.pesan_error = (
            "NIM tidak valid. NIM harus terdiri dari tepat 10 digit angka."
        )

    # Validasi berat: harus bilangan bulat positif.
    elif berat <= 0 or not float(berat).is_integer():
        st.session_state.pesan_error = (
            "Berat cucian tidak valid. Berat harus berupa bilangan bulat lebih dari 0 kg."
        )

    else:
        st.session_state.hasil = hitung_biaya(nim, int(berat))


# ---------------------- MENAMPILKAN HASIL ----------------------

if st.session_state.pesan_error:
    st.error(st.session_state.pesan_error)

if st.session_state.hasil is not None:
    hasil = st.session_state.hasil

    st.divider()
    st.subheader("📋 Rincian Perhitungan")

    st.write(f"**NIM:** {nim}")
    st.write(f"**Berat cucian:** {int(berat)} kg")

    kolom1, kolom2 = st.columns(2)

    with kolom1:
        st.metric("Tarif per kg", rupiah(hasil["tarif"]))
        st.metric("Persen diskon", f'{hasil["diskon"]}%')
        st.metric("Biaya normal", rupiah(hasil["biaya_normal"]))

    with kolom2:
        st.metric("Jumlah digit genap", f'{hasil["jumlah_genap"]} digit')
        st.metric("Potongan", rupiah(hasil["potongan"]))
        st.metric("Total bayar", rupiah(hasil["total_bayar"]))

    st.success(f"Total yang harus dibayar: **{rupiah(hasil['total_bayar'])}**")

st.divider()
st.caption(
    "Rumus: Tarif/kg = Rp5.000 + (digit terakhir NIM × Rp500). "
    "Diskon = jumlah digit genap pada NIM × 1%."
)
