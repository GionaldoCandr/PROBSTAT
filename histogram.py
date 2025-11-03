# =========================================================
# HISTOGRAM & DIAGRAM BATANG FASILITAS PENDIDIKAN DKI JAKARTA (2024)
# =========================================================

import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, median, mode
from scipy.stats import gaussian_kde
import pandas as pd

# === 1. DATA FASILITAS PENDIDIKAN PER KABUPATEN/KOTA ===
data_wilayah = {
    "Kabupaten/Kota": [
        "Kep. Seribu",
        "Jakarta Selatan",
        "Jakarta Timur",
        "Jakarta Pusat",
        "Jakarta Barat",
        "Jakarta Utara"
    ],
    "SD": [6, 63, 65, 43, 56, 31],
    "SMP": [5, 61, 64, 40, 54, 31],
    "SMA": [3, 55, 55, 31, 44, 31],
    "SMK": [1, 47, 57, 30, 46, 26],
    "Perguruan Tinggi": [0, 43, 33, 23, 18, 12]
}

df = pd.DataFrame(data_wilayah)

# === 2. HITUNG TOTAL FASILITAS TIAP WILAYAH ===
df["Total Fasilitas"] = df[["SD", "SMP", "SMA", "SMK", "Perguruan Tinggi"]].sum(axis=1)

print("=== Total Fasilitas Pendidikan per Wilayah ===")
print(df[["Kabupaten/Kota", "Total Fasilitas"]])

# === 3. HITUNG STATISTIK ===
total_fasilitas = df["Total Fasilitas"].tolist()

mean_val = mean(total_fasilitas)
median_val = median(total_fasilitas)
try:
    modus_val = mode(total_fasilitas)
except:
    modus_val = "Tidak ada"

print(f"\nMean: {mean_val:.2f}")
print(f"Median: {median_val}")
print(f"Modus: {modus_val}")

# === 4. BUAT DIAGRAM BATANG (PERBANDINGAN ANTAR WILAYAH) ===
plt.figure(figsize=(10, 6))
plt.bar(df["Kabupaten/Kota"], df["Total Fasilitas"], color="cornflowerblue", edgecolor="black")
plt.title("Diagram Batang Jumlah Total Fasilitas Pendidikan per Wilayah\nProvinsi DKI Jakarta Tahun 2024",
          fontsize=12, fontweight='bold')
plt.xlabel("Kabupaten / Kota")
plt.ylabel("Jumlah Total Fasilitas Pendidikan")
plt.xticks(rotation=30)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Tambahkan teks nilai di atas batang
for i, val in enumerate(df["Total Fasilitas"]):
    plt.text(i, val + 2, str(val), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# === 5. BUAT HISTOGRAM NUMERIK (SESUAI TEORI STATISTIK) ===
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(
    total_fasilitas,
    bins=5,                    # jumlah interval
    color='skyblue',
    edgecolor='black',
    alpha=0.6,
    label='Histogram (Frekuensi)'
)

# Estimasi kurva distribusi (KDE)
kde = gaussian_kde(total_fasilitas)
x_vals = np.linspace(min(total_fasilitas), max(total_fasilitas), 200)
y_vals = kde(x_vals)
y_vals_scaled = y_vals * (max(n) / max(y_vals))
plt.plot(x_vals, y_vals_scaled, color='blue', linewidth=2, label='Estimasi Kurva (Diskalakan)')

# Garis mean & median
plt.axvline(mean_val, color='red', linestyle='--', linewidth=1.8, label=f'Mean: {mean_val:.2f}')
plt.axvline(median_val, color='green', linestyle='--', linewidth=1.8, label=f'Median: {median_val}')

# Label mean & median
plt.text(mean_val + 1, max(n) * 0.9, 'Mean', color='red')
plt.text(median_val + 1, max(n) * 0.8, 'Median', color='green')

# Tambahkan judul, label, dan legenda
plt.title("Histogram Total Fasilitas Pendidikan per Wilayah\nProvinsi DKI Jakarta Tahun 2024",
          fontsize=12, fontweight='bold')
plt.xlabel("Jumlah Total Fasilitas Pendidikan (SD–PT)")
plt.ylabel("Frekuensi (Jumlah Kabupaten/Kota)")
plt.legend()

# Tambahkan statistik di kanan atas
text_str = (
    f"Mean: {mean_val:.2f}\n"
    f"Median: {median_val}\n"
    f"Mode: {modus_val}"
)
plt.text(
    0.98, 0.95, text_str,
    transform=plt.gca().transAxes,
    fontsize=10,
    va='top', ha='right',
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

plt.tight_layout()
plt.show()
