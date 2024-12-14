import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Fungsi untuk memuat data
def muat_data(nama_file):
    return pd.read_csv(f"datasets/{nama_file}")

# Sidebar navigasi
st.sidebar.title("Navigasi")
pilihan = st.sidebar.selectbox("Pilih Halaman", ["Beranda", "Visualisasi Data", "Analisis Waktu & Nilai Pembayaran", "Analisis Skor Ulasan & Pengiriman"])

# Halaman Beranda
if pilihan == "Beranda":
    st.title("Analisis Data Pesanan Ecommerce by Galih Sangra Adiyuga")
    st.write("""
    Aplikasi ini membantu menganalisis data pesanan ecommerce berdasarkan dua pertanyaan utama:

    1. Bagaimana waktu persetujuan pesanan memengaruhi nilai pembayaran?
    2. Apakah skor ulasan pelanggan berpengaruh terhadap tingkat pengiriman tepat waktu?
    """)

# Halaman Visualisasi Data
elif pilihan == "Visualisasi Data":
    st.title("Visualisasi Data")
    st.subheader("Distribusi Harga Produk")

    # Muat dataset order_items_dataset.csv
    data = muat_data("order_items_dataset.csv")

    # Histogram Harga Produk
    fig, ax = plt.subplots(figsize=(10, 6))
    data['price'].hist(bins=30, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title("Distribusi Harga Produk", fontsize=16)
    ax.set_xlabel("Harga", fontsize=12)
    ax.set_ylabel("Frekuensi", fontsize=12)
    
    st.pyplot(fig)  # Tampilkan grafik
    st.write("""
    **Keterangan:** Grafik ini menunjukkan distribusi harga produk pada dataset. Sebagian besar harga produk berada pada rentang rendah hingga sedang, mengindikasikan mayoritas produk cenderung terjangkau.
    """)

# Halaman Analisis Waktu & Nilai Pembayaran
elif pilihan == "Analisis Waktu & Nilai Pembayaran":
    st.title("Analisis Waktu Persetujuan & Nilai Pembayaran")

    # Muat dataset
    orders_data = muat_data("orders_dataset.csv")
    payments_data = muat_data("order_payments_dataset.csv")

    # Gabungkan dataset berdasarkan order_id
    merged_data = pd.merge(orders_data, payments_data, on="order_id", how="inner")

    # Pastikan kolom 'order_approved_at' dalam format datetime
    merged_data['order_approved_at'] = pd.to_datetime(merged_data['order_approved_at'])

    # Scatterplot waktu persetujuan vs nilai pembayaran
    fig = px.scatter(merged_data, x='order_approved_at', y='payment_value', 
                     title="Scatterplot Waktu Persetujuan vs Nilai Pembayaran",
                     labels={'order_approved_at': 'Waktu Persetujuan', 'payment_value': 'Nilai Pembayaran'})
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    **Keterangan:** Grafik ini mengeksplorasi hubungan antara waktu persetujuan pesanan dan nilai pembayaran. Pesanan yang disetujui lebih cepat cenderung memiliki nilai pembayaran yang lebih tinggi, menunjukkan kemungkinan adanya urgensi atau keinginan untuk pengiriman cepat.
    """)

# Halaman Analisis Skor Ulasan & Pengiriman
elif pilihan == "Analisis Skor Ulasan & Pengiriman":
    st.title("Analisis Skor Ulasan & Pengiriman Tepat Waktu")

    # Muat dataset
    orders = muat_data("orders_dataset.csv")
    reviews = muat_data("order_reviews_dataset.csv")

    # Tambahkan kolom on_time_delivery_rate
    orders['on_time_delivery'] = (
        pd.to_datetime(orders['order_delivered_customer_date']) <= 
        pd.to_datetime(orders['order_estimated_delivery_date'])
    ).astype(int)

    on_time_rate = orders.groupby('order_id')['on_time_delivery'].mean().reset_index()
    on_time_rate.rename(columns={'on_time_delivery': 'on_time_delivery_rate'}, inplace=True)

    # Gabungkan dengan dataset reviews
    data = reviews.merge(on_time_rate, on='order_id', how='left')

    # Hitung rata-rata tingkat pengiriman tepat waktu per skor ulasan
    avg_on_time_rate = data.groupby('review_score')['on_time_delivery_rate'].mean().reset_index()

    # Line chart skor ulasan vs rata-rata tingkat pengiriman tepat waktu
    fig = px.line(avg_on_time_rate, 
                  x='review_score', 
                  y='on_time_delivery_rate', 
                  markers=True,  # Tambahkan titik pada setiap data
                  title="Tren Rata-rata Tingkat Pengiriman Tepat Waktu berdasarkan Skor Ulasan",
                  labels={'review_score': 'Skor Ulasan', 'on_time_delivery_rate': 'Rata-rata Tingkat Pengiriman Tepat Waktu'})
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    **Keterangan:** Grafik ini menunjukkan tren rata-rata tingkat pengiriman tepat waktu untuk setiap skor ulasan. 
    Skor ulasan yang lebih tinggi biasanya menunjukkan tingkat pengiriman tepat waktu yang lebih baik.
    """)

