import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Fizik sabitleri
g = 9.81
default_k = 0.47  # Hava direnci katsayısı

st.set_page_config(page_title="Serbest Düşme Simülasyonu", layout="wide")

st.title("Serbest Düşme Simülasyonu: Hava Direnci")

# Kullanıcı girdileri
mass = st.sidebar.number_input("Cisim Kütlesi (kg)", min_value=0.001, value=0.05, step=0.01)
height = st.sidebar.number_input("Başlangıç Yüksekliği (m)", min_value=0.1, value=2.0, step=0.1)
env = st.sidebar.radio("Ortam Seçimi", ["Vakum (Hava Direnci Yok)", "Hava (Hava Direnci Var)"])
k = default_k if env.startswith("Hava") else 0.0

st.sidebar.markdown(
    """
    **Açıklama:**
    - Vakumda tüm cisimler aynı anda düşer.
    - Hava ortamında hafif cisim daha yavaş düşer.
    - Hava direnci lineer (F=-kv) olarak modellenmiştir.
    - Gerçekçi değerler için: Kütle 0.01-0.2 kg, yükseklik 1-10 m arası önerilir.
    """
)

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
        t.append(t[-1] + dt)
        v.append(v_new)
        y.append(max(y_new, 0))
        a.append(a_new)
    return np.array(t), np.array(y), np.array(v), np.array(a)

# Simülasyonu başlat
if st.button("Simülasyonu Başlat"):
    t, y, v, a = simulate_fall(mass, height, k)

    # Sonuç
    time_to_ground = t[-1]
    if k == 0:
        st.success(f"Vakumda yere ulaşma süresi: {time_to_ground:.2f} s.\nTüm cisimler aynı anda yere ulaşır.")
    else:
        st.success(f"Hava ortamında yere ulaşma süresi: {time_to_ground:.2f} s.\nHafif cisimler daha yavaş düşer.")

    # Animasyon benzeri basit görselleştirme (çubuk)
    st.subheader("Düşme Animasyonu (Basit)")
    for i in range(0, len(y), max(1, len(y)//100)):
        st.text("⬤" + " " * int((height - y[i]) * 10))

    # Grafikler
    st.subheader("Grafikler")
    fig, axs = plt.subplots(3, 1, figsize=(8, 10))
    axs[0].plot(t, y, color='#1976d2'); axs[0].set_title("Zaman - Konum"); axs[0].set_xlabel("Zaman (s)"); axs[0].set_ylabel("Yükseklik (m)"); axs[0].grid(True)
    axs[1].plot(t, v, color='#388e3c'); axs[1].set_title("Zaman - Hız"); axs[1].set_xlabel("Zaman (s)"); axs[1].set_ylabel("Hız (m/s)"); axs[1].grid(True)
    axs[2].plot(t, a, color='#fbc02d'); axs[2].set_title("Zaman - İvme"); axs[2].set_xlabel("Zaman (s)"); axs[2].set_ylabel("İvme (m/s²)"); axs[2].grid(True)
    fig.tight_layout(pad=4.0)
    st.pyplot(fig)
