import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Fizik sabitleri
g = 9.81
default_k = 0.47

st.set_page_config(page_title="Serbest Düşme Simülasyonu", layout="wide")
st.title("Serbest Düşme: Hava Direnci Simülasyonu")

# Kullanıcı girdileri
col1, col2 = st.columns([1,2])

with col1:
    mass = st.number_input("Cisim Kütlesi (kg)", min_value=0.01, max_value=10.0, value=0.05, step=0.01)
    h0 = st.number_input("Başlangıç Yüksekliği (m)", min_value=0.1, max_value=100.0, value=2.0, step=0.1)
    env = st.radio("Ortam Seçimi", ["Vakum (Hava Direnci Yok)", "Hava (Hava Direnci Var)"])

k = default_k if env == "Hava (Hava Direnci Var)" else 0.0

def simulate_fall(m, h0, k):
    dt = 0.001
    t = [0]
    y = [h0]
    v = [0]
    a = [g]
    while y[-1] > 0:
        a_new = g - (k/m)*v[-1] if k != 0 else g
        v_new = v[-1] + a_new*dt
        y_new = y[-1] - v_new*dt
        t.append(t[-1]+dt)
        v.append(v_new)
        y.append(max(y_new,0))
        a.append(a_new)
    return np.array(t), np.array(y), np.array(v), np.array(a)

t, y, v, a = simulate_fall(m, h0, k)

# Sonuç mesajı
time_to_ground = t[-1]
if k == 0:
    st.success(f"Vakumda yere ulaşma süresi: {time_to_ground:.2f} s. Tüm cisimler aynı anda düşer.")
else:
    st.success(f"Hava ortamında yere ulaşma süresi: {time_to_ground:.2f} s. Hafif cisimler daha yavaş düşer.")

# Grafikler
fig, axs = plt.subplots(3, 1, figsize=(8,10))
axs[0].plot(t, y, color='#1976d2'); axs[0].set_title("Zaman - Konum"); axs[0].set_xlabel("Zaman (s)"); axs[0].set_ylabel("Yükseklik (m)"); axs[0].grid(True)
axs[1].plot(t, v, color='#388e3c'); axs[1].set_title("Zaman - Hız"); axs[1].set_xlabel("Zaman (s)"); axs[1].set_ylabel("Hız (m/s)"); axs[1].grid(True)
axs[2].plot(t, a, color='#fbc02d'); axs[2].set_title("Zaman - İvme"); axs[2].set_xlabel("Zaman (s)"); axs[2].set_ylabel("İvme (m/s²)"); axs[2].grid(True)
fig.tight_layout(pad=3.0)

col2.pyplot(fig)
