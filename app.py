import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageFilter
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

# 🏷️ Label kelas
CLASS_NAMES = ['Fire', 'None', 'Smoke', 'Smoke and Fire']

# 🧠 Memuat model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("best_scenario_3_lr1.keras")  # Ganti dengan model kamu

# 🔍 Fungsi prediksi
def predict(image, model):
    image = image.resize((224, 224))
    img_array = np.array(image)
    img_array = preprocess_input(img_array)
    img_array = tf.convert_to_tensor(img_array, dtype=tf.float32)
    img_array = tf.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)[0]
    return predictions

# 🌐 Konfigurasi halaman
st.markdown("""
<div style='text-align: center;'>
    <h1 style='font-size: 3em;'>🔥 SiJaga API</h1>
    <h4>Sistem Deteksi Dini Kebakaran Hutan</h4>
</div>
""", unsafe_allow_html=True)

# 📷 Logo
@st.cache_data
def load_logo():
    img = Image.open("SI_JAGA-removebg-preview.png")
    return img.filter(ImageFilter.SHARPEN)

# 📚 Sidebar
with st.sidebar:
    st.image(load_logo(), width=250)
    st.markdown("---")
    st.subheader("ℹ️ Penjelasan Kelas")
    st.markdown("""
    - **🔥 Fire**: Hanya api yang terlihat jelas.
    - **💨 Smoke**: Hanya asap tanpa api terlihat.
    - **🔥💨 Smoke and Fire**: Terdapat Asap dan Api
    - **✅ None**: Tidak ada asap maupun api.
    """)
    st.markdown("---")
    st.subheader("📸 Ketentuan Gambar")
    st.markdown("""
    - Format: **.jpg**, **.jpeg**, **.png**  
    - Fokus pada objek (api/asap)  
    - Hindari gambar gelap/buram  
    - Jangan gunakan gambar dengan watermark
    """)

# 📤 Upload gambar
# 📤 Upload gambar
st.markdown("""
    <h4 style='text-align:center; margin-top: 25px; color: #333;'>📤 Silakan Upload Gambar</h4>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader(
    label="",
    type=["jpg", "jpeg", "png"],
    help="Format gambar yang didukung: JPG, JPEG, PNG"
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, use_container_width=True)


        # 🔮 Prediksi
        model = load_model()
        predictions = predict(image, model)

        # 🔢 Urutkan berdasarkan confidence
        sorted_indices = np.argsort(predictions)[::-1]
        sorted_labels = [CLASS_NAMES[i] for i in sorted_indices]
        sorted_confidences = [float(predictions[i]) for i in sorted_indices]

        top_label = sorted_labels[0]
        top_confidence = sorted_confidences[0] * 100

        # 📦 Hasil klasifikasi
    

        st.subheader("📊 Hasil Klasifikasi:")
        st.success(f"Prediksi: **{top_label}** dengan Score Confidence **{top_confidence:.2f}%**")

        # 🚨 Peringatan cepat
        if top_label == "Smoke and Fire":
            st.error("🚨 Kebakaran besar terdeteksi! Segera hubungi tim pemadam dan evakuasi area!")
        elif top_label == "Fire":
            st.error("🔥 Api terdeteksi! Harap segera panggil tim pemadam.")
        elif top_label == "Smoke":
            st.warning("⚠️ Asap terdeteksi. Perlu investigasi lebih lanjut.")
        elif top_label == "None":
            st.info("✅ Tidak ada tanda-tanda kebakaran terdeteksi.")

        st.markdown("</div>", unsafe_allow_html=True)

        # 📋 Detail Tindakan
        st.markdown("### 🌲🚨 Tindakan Penanggulangan Kebakaran Hutan")

        if top_label == "Smoke and Fire":
            st.markdown("""
            - 🚒 Kerahkan armada pemadam kebakaran hutan.  
            - 🧭 Evakuasi warga sekitar.  
            - 🛰️ Koordinasi dengan BPBD & BNPB.  
            - ⛑️ Sediakan bantuan medis & logistik.  
            - 📡 Aktifkan komunikasi darurat.
            """)
        elif top_label == "Fire":
            st.markdown("""
            - 🚒 Hubungi tim pemadam terdekat.  
            - 📍 Lokalisasi titik api.  
            - 🧯 Gunakan alat pemadam ringan.  
            - ☎️ Laporkan ke dinas kebakaran.  
            - 👷‍♂️ Gunakan APD lengkap.
            """)
        elif top_label == "Smoke":
            st.markdown("""
            - 🔍 Cek lokasi sumber asap.  
            - 📞 Hubungi tim lapangan.  
            - 🚁 Gunakan drone pemantau.  
            - 🧯 Siapkan alat pemadam portabel.
            """)
        elif top_label == "None":
            st.markdown("""
            - 🚫 Jangan membakar lahan.  
            - 🗑️ Jangan buang puntung rokok sembarangan.  
            - 📸 Pantau kondisi via drone/satelit.  
            - 📡 Gunakan sistem peringatan dini.
            """)

        # 📈 Tampilkan semua confidence
        for label, conf in zip(sorted_labels, sorted_confidences):
            percent = conf * 100
            st.write(f"**{label}**: {percent:.2f}%")
            st.progress(float(conf))

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses gambar: {e}")

# 📎 Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Dibuat oleh <strong>Ardhan Azhra Azmi</strong> 🔥</p>", unsafe_allow_html=True)
