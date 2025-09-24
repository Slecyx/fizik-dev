import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import time

st.set_page_config(layout="wide")  # Geniş ekran kullanımı

# Fizik sabitleri
g = 9.81
default_k = 0.47

# Layout: 3 kolon
col1, col2, col3 = st.columns([2, 3, 3])  # oranlar: solda 2, orta 3, sağ 3

# ====== SOL KOLON: Kullanıcı Girdileri ======
with col1:
    st.header("Simülasyon Ayarları")
    mass = st.number_input("Cisim Kütlesi (kg)", min_value=0.001, value=0.05, step=0.01)
    height = st.number_input("Başlangıç Yüksekliği (m)", min_value=0.1, value=2.0, step=0.1)
    env = st.radio("Ortam Seçimi", ["Vakum", "Hava"])
    start = st.button("Simülasyonu Başlat")

# ====== ORTA KOLON: Düşme Animasyonu ======
anim_placeholder = col2.empty()

# ====== SAĞ KOLON: Grafikler ======
graph_placeholder = col3.empty()

def simulate_fall(m, h0, k):
    dt = 0.01
    t = [0]; y = [h0]; v = [0]; a = [g]
    while y[-1] > 0:
        a_new = g - (k/m)*v[-1] if k != 0 else g
        v_new = v[-1] + a_new*dt
        y_new = y[-1] - v_new*dt
        t.append(t[-1]+dt)
        v.append(v_new)
        y.append(max(y_new,0))
        a.append(a_new)
    return np.array(t), np.array(y), np.array(v), np.array(a)

if start:
    k = default_k if env == "Hava" else 0.0
    t, y, v, a = simulate_fall(mass, height, k)

    # Sonuç mesajı
    if k == 0:
        st.success(f"Vakumda yere ulaşma süresi: {t[-1]:.2f} s")
    else:
        st.success(f"Hava ortamında yere ulaşma süresi: {t[-1]:.2f} s")

    # ===== Animasyon =====
    for yi in y[::5]:  # frame atlama, hızlı oynatma
        fig, ax = plt.subplots(figsize=(3,6))  # orta kolon için orantılı
        ax.plot(0, yi, 'ro', markersize=20)
        ax.set_xlim(-1,1)
        ax.set_ylim(0, height*1.1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Düşme Animasyonu")
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        anim_placeholder.image(img)
        plt.close(fig)
        time.sleep(0.01)

    # ===== Grafikler =====
    fig2, ax2 = plt.subplots(3,1, figsize=(5,6))
    ax2[0].plot(t, y, color='#1976d2')
    ax2[0].set_title("Yükseklik (m)")
    ax2[0].grid(True)
    ax2[1].plot(t, v, color='#388e3c')
    ax2[1].set_title("Hız (m/s)")
    ax2[1].grid(True)
    ax2[2].plot(t, a, color='#fbc02d')
    ax2[2].set_title("İvme (m/s²)")
    ax2[2].grid(True)
    fig2.tight_layout(pad=2.0)
    graph_placeholder.pyplot(fig2)
