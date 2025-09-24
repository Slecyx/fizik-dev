import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Fizik sabitleri
g = 9.81
default_k = 0.47  # Hava direnci

st.set_page_config(page_title="Serbest Düşme Simülasyonu", layout="wide")
st.title("Serbest Düşme Simülasyonu")

# Yan panel: girdiler
with st.sidebar:
    mass = st.number_input("Cisim Kütlesi (kg)", min_value=0.001, value=0.05, step=0.01)
    height = st.number_input("Başlangıç Yüksekliği (m)", min_value=0.1, value=2.0, step=0.1)
    env = st.radio("Ortam Seçimi", ["Vakum (Hava Direnci Yok)", "Hava (Hava Direnci Var)"])
    k = default_k if env.startswith("Hava") else 0.0
    start = st.button("Simülasyonu Başlat")

# Simülasyon fonksiyonu
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
    time_to_ground = t[-1]

    # Sonuç mesajı
    if k == 0:
        st.success(f"Vakumda yere ulaşma süresi: {time_to_ground:.2f} s.\nTüm cisimler aynı anda yere ulaşır.")
    else:
        st.success(f"Hava ortamında yere ulaşma süresi: {time_to_ground:.2f} s.\nHafif cisimler daha yavaş düşer.")

    # Animasyon + grafikler
    fig, axs = plt.subplots(2, 1, figsize=(6,8))
    plt.tight_layout(pad=3.0)
    
    # Animasyon grafiği
    anim_ax = axs[0]
    anim_ax.set_xlim(-0.5, 0.5)
    anim_ax.set_ylim(0, height*1.1)
    ball, = anim_ax.plot(0, height, 'ro', markersize=20)
    anim_ax.set_title("Düşme Animasyonu")
    anim_ax.get_xaxis().set_visible(False)
    
    def animate(i):
        ball.set_data(0, y[i])
        return ball,

    ani = animation.FuncAnimation(fig, animate, frames=len(y), interval=20, blit=True)
    
    # Grafikler
    axs[1].plot(t, y, color='blue', label='Yükseklik (m)')
    axs[1].plot(t, v, color='green', label='Hız (m/s)')
    axs[1].plot(t, a, color='orange', label='İvme (m/s²)')
    axs[1].set_xlabel("Zaman (s)")
    axs[1].set_ylabel("Değerler")
    axs[1].legend()
    axs[1].grid(True)
    
    st.pyplot(fig)
