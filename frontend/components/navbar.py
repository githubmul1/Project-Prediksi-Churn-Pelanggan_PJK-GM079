import streamlit as st
from streamlit_option_menu import option_menu

def render_navbar():
    # UntukLogo dan Menu Navigasi 
    menu_col = st.columns([1])[0] 
    
    with menu_col:
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