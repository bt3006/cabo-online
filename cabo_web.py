import streamlit as st

st.set_page_config(page_title="Cabo – Web Edition", page_icon="🧠")

# Titel der App
st.title("🃏 Cabo – Web Edition")

# Sidebar für Spielereingabe
st.sidebar.header("Spielereinstellungen")
spieler1_name = st.sidebar.text_input("👤 Name Spieler 1", "Spieler 1")
spieler2_name = st.sidebar.text_input("👤 Name Spieler 2", "Spieler 2")

# Im Session-State speichern (optional, falls später weiterverwendet)
st.session_state.spieler1_name = spieler1_name
st.session_state.spieler2_name = spieler2_name
