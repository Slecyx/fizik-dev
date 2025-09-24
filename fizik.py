import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Fizik sabitleri
g = 9.81
default_k = 0.47  # Hava direnci

st.set_page_config(layout="wide", page_title="Serbest Düşme Simülasyonu")

# Layout: üç kolon
col1, col2, col3 = st.columns([1,1,1])

# --- Sol Panel: Girişler ---
with col1:
    st.header("Girişler")
    mass = st.number_input("Cisim Kütlesi (kg)", value=0.05, min_value=0.01, max_value=1.0, step=0.01)
    height = st.number_input("Başlangıç Yüksekliği (m)", value=2.0, min_value=0.1, max_value=20.0, step=0.1)
    env_option = st.radio("Ortam Seçimi:", ["Hava Direnci Yok (Vakum)", "Hava Direnci Var (Hava)"])
    start = st.button("Simülasyonu Başlat")

# --- Simülasyon Fonksiyonu ---
def simulate_fall(m, h0, k):
    dt = 0.01
    t = [0]
    y = [h0]
    v = [0]
    a = [g]
    while y[-1] > 0:
        if k == 0:
            a_new = g
        else:
            a_new = g - (k/m)*v[-1]
        v_new = v[-1] + a_new*dt
        y_new = y[-1] - v_new*dt
        t.append(t[-1]+dt)
        v.append(v_new)
        y.append(max(y_new,0))
        a.append(a_new)
    return np.array(t), np.array(y), np.array(v), np.array(a)

# --- Başlatma ---
if start:
    k = default_k if env_option=="Hava Direnci Var (Hava)" else 0.0
    t, y, v, a = simulate_fall(mass, height, k)
    
    time_to_ground = t[-1]
    if k==0:
        st.sidebar.success(f"Vakumda yere ulaşma süresi: {time_to_ground:.2f} s")
    else:
        st.sidebar.success(f"Hava ortamında yere ulaşma süresi: {time_to_ground:.2f} s")
    
    # --- Animasyon yerine basit çizim ---
    with col2:
        st.header("Düşme Animasyonu (Statik)")
        fig2, ax2 = plt.subplots(figsize=(3,6))
        ax2.plot(np.zeros_like(y), y, 'ro')  # kırmızı noktalar cisim
        ax2.set_xlim(-1,1)
        ax2.set_ylim(0, max(y)*1.1)
        ax2.set_ylabel("Yükseklik (m)")
        ax2.set_xticks([])
        st.pyplot(fig2)
    
    # --- Grafikler ---
    with col3:
        st.header("Grafikler")
        fig, axs = plt.subplots(3,1, figsize=(6,6))
        axs[0].plot(t, y, color='#1976d2'); axs[0].set_title("Zaman - Konum"); axs[0].set_xlabel("Zaman (s)"); axs[0].set_ylabel("Yükseklik (m)"); axs[0].grid(True)
        axs[1].plot(t, v, color='#388e3c'); axs[1].set_title("Zaman - Hız"); axs[1].set_xlabel("Zaman (s)"); axs[1].set_ylabel("Hız (m/s)"); axs[1].grid(True)
        axs[2].plot(t, a, color='#fbc02d'); axs[2].set_title("Zaman - İvme"); axs[2].set_xlabel("Zaman (s)"); axs[2].set_ylabel("İvme (m/s²)"); axs[2].grid(True)
        plt.tight_layout()
        st.pyplot(fig)
