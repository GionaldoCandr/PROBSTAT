import matplotlib.pyplot as plt
from statistics import mean, median, mode
from matplotlib.widgets import Button
import pandas as pd

# === 1. DATA MANUAL (TERPISAH ANTARA WILAYAH & DKI) ===
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

data_dki = {
    "Kabupaten/Kota": ["DKI Jakarta"],
    "SD": [264],
    "SMP": [255],
    "SMA": [219],
    "SMK": [207],
    "Perguruan Tinggi": [129]
}

df = pd.DataFrame(data_wilayah)
df_dki = pd.DataFrame(data_dki)

# === 2. HITUNG STATISTIK UNTUK SETIAP JENJANG (HANYA WILAYAH) ===
statistik = []
jenjang_list = ["SD", "SMP", "SMA", "SMK", "Perguruan Tinggi"]

for jenjang in jenjang_list:
    nilai_wilayah = df[jenjang].tolist()
    nilai_dki = df_dki[jenjang].iloc[0]
    statistik.append({
        "Jenjang": jenjang,
        "Mean (Wilayah)": round(mean(nilai_wilayah), 2),
        "Median (Wilayah)": median(nilai_wilayah),
        "Modus (Wilayah)": mode(nilai_wilayah),
        "Total DKI": nilai_dki
    })

hasil_statistik = pd.DataFrame(statistik)
print("=== Statistik Fasilitas Sekolah per Jenjang ===")
print(hasil_statistik)

# === 3. SIMPAN KE FILE EXCEL ===
with pd.ExcelWriter("Analisis_Fasilitas_Sekolah_DKI.xlsx") as writer:
    df.to_excel(writer, sheet_name="Data Wilayah", index=False)
    df_dki.to_excel(writer, sheet_name="Data DKI", index=False)
    hasil_statistik.to_excel(writer, sheet_name="Statistik", index=False)

print("\n✅ File hasil disimpan sebagai 'Analisis_Fasilitas_Sekolah_DKI.xlsx'")

# === 4. HISTOGRAM INTERAKTIF (TANPA DKI) ===
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
index = 0

def plot_histogram(idx):
    ax.clear()
    jenjang = jenjang_list[idx]
    nilai_wilayah = df[jenjang].tolist()
    nilai_dki = df_dki[jenjang].iloc[0]

    # Plot histogram wilayah
    ax.bar(df["Kabupaten/Kota"], nilai_wilayah, color="cornflowerblue", edgecolor="black")
    ax.set_title(f"Fasilitas Sekolah Jenjang {jenjang} per Wilayah (2024)")
    ax.set_xlabel("Kabupaten / Kota")
    ax.set_ylabel("Jumlah Fasilitas")
    plt.xticks(rotation=30)

    # Ambil statistik
    mean_val = mean(nilai_wilayah)
    median_val = median(nilai_wilayah)
    try:
        modus_val = mode(nilai_wilayah)
    except:
        modus_val = "Tidak ada (semua unik)"

    # Tampilkan nilai statistik + pembanding DKI
    text_str = (
        f"Mean (Wilayah): {mean_val:.2f}\n"
        f"Median (Wilayah): {median_val}\n"
        f"Modus (Wilayah): {modus_val}\n"
        f"Total DKI: {nilai_dki}"
    )
    ax.text(0.98, 0.97, text_str,
            transform=ax.transAxes,
            fontsize=10,
            va='top', ha='right',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    fig.canvas.draw_idle()

plot_histogram(index)

class IndexTracker:
    def __init__(self):
        self.idx = 0
    def next(self, event):
        self.idx = (self.idx + 1) % len(jenjang_list)
        plot_histogram(self.idx)
    def prev(self, event):
        self.idx = (self.idx - 1) % len(jenjang_list)
        plot_histogram(self.idx)

callback = IndexTracker()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next →')
bprev = Button(axprev, '← Prev')
bnext.on_clicked(callback.next)
bprev.on_clicked(callback.prev)

plt.show()
# === 5. HISTOGRAM PERBANDINGAN TOTAL DKI ===
# Data DKI per jenjang
nilai_dki_list = df_dki[jenjang_list].iloc[0].tolist()

# Hitung statistik DKI
mean_dki = mean(nilai_dki_list)
median_dki = median(nilai_dki_list)
try:
    modus_dki = mode(nilai_dki_list)
except:
    modus_dki = "Tidak ada (semua unik)"

# Plot histogram total DKI per jenjang
fig2, ax2 = plt.subplots()
ax2.bar(jenjang_list, nilai_dki_list, color="orange", edgecolor="black")
ax2.set_title("Perbandingan Total DKI Jakarta per Jenjang (2024)")
ax2.set_xlabel("Jenjang Sekolah")
ax2.set_ylabel("Jumlah Fasilitas")
plt.xticks(rotation=30)

# Tampilkan statistik DKI
text_str_dki = (
    f"Mean (DKI): {mean_dki:.2f}\n"
    f"Median (DKI): {median_dki}\n"
    f"Modus (DKI): {modus_dki}"
)
ax2.text(0.98, 0.97, text_str_dki,
         transform=ax2.transAxes,
         fontsize=10,
         va='top', ha='right',
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

plt.show()
