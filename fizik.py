import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import time

# Fizik sabitleri
g = 9.81
default_k = 0.47

st.title("Serbest Düşme Simülasyonu")

# Kullanıcı girdileri
mass = st.number_input("Cisim Kütlesi (kg)", min_value=0.001, value=0.05, step=0.01)
height = st.number_input("Başlangıç Yüksekliği (m)", min_value=0.1, value=2.0, step=0.1)
env = st.radio("Ortam Seçimi", ["Vakum", "Hava"])
k = default_k if env == "Hava" else 0.0
start = st.button("Simülasyonu Başlat")

def simulate_fall(m, h0, k):
    dt = 0.01
    t = [0]; y = [h0]; v = [0]; a = [g]
    while y[-1] > 0:
        a_new = g - (k/m)*v[-1] if k != 0 else g
        v_new = v[-1] + a_new*dt
        y_new = y[-1] - v_new*dt
        t.append(t[-1] + dt)
        v.append(v_new)
        y.append(max(y_new, 0))
        a.append(a_new)
    return np.array(t), np.array(y), np.array(v), np.array(a)

if start:
    t, y, v, a = simulate_fall(mass, height, k)
    
    # Sonuç mesajı
    if k == 0:
        st.success(f"Vakumda yere ulaşma süresi: {t[-1]:.2f} s")
    else:
        st.success(f"Hava ortamında yere ulaşma süresi: {t[-1]:.2f} s")
    
    anim_placeholder = st.empty()
    
    # Animasyon (frame frame)
    for yi in y[::5]:  # Daha hızlı oynatma için 5 frame atla
        fig, ax = plt.subplots(figsize=(2,4))
        ax.plot(0, yi, 'ro', markersize=20)
        ax.set_xlim(-1,1)
        ax.set_ylim(0, height*1.1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Düşme Animasyonu")
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        img = Image.open(buf)
        anim_placeholder.image(img)
        plt.close(fig)
        time.sleep(0.01)
    
    # Grafikler
    fig2, ax2 = plt.subplots(figsize=(6,3))
    ax2.plot(t, y, label='Yükseklik')
    ax2.plot(t, v, label='Hız')
    ax2.plot(t, a, label='İvme')
    ax2.set_xlabel("Zaman (s)")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
