import streamlit as st
from streamlit_option_menu import option_menu

def render_navbar():
    # UntukLogo dan Menu Navigasi 
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Mencoba menampilkan logo 
        try:
            st.image("frontend/assets/logo.png", width=120)
        except:
            # Fallback jika logo belum ada
            st.markdown("### 📊 CHURN-APP")
            
    with col2:
        # Menu Navigasi Horizontal
        selected = option_menu(
            menu_title=None, 
            options=["Dashboard", "Prediksi Churn", "Tentang Aplikasi"],
            icons=["house", "calculator", "info-circle"], 
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#ff4b4b", "font-size": "16px"}, 
                "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#ff4b4b"},
            }
        )
    return selected