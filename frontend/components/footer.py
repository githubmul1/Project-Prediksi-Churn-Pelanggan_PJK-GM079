import streamlit as st

def render_footer():
    st.write("---") # Garis pemisah

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Prediksi Churn Pelanggan**")
        st.caption("Aplikasi berbasis data untuk memprediksi retensi pelanggan.")
        
    with col2:
        st.markdown("**Navigasi Cepat**")
        st.caption("• Dashboard\n• Form Prediksi\n• Tentang Aplikasi")
        
    with col3:
        st.markdown("**Tim PJK-GM079**")
        st.caption("© 2026 Hak Cipta Dilindungi.")