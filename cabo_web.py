import streamlit as st

# Spieler anhand der URL erkennen (z. B. ?spieler=1 oder ?spieler=2)
spieler_param = st.query_params.get("spieler")
if spieler_param not in ["1", "2"]:
    st.error("❌ Bitte hänge ?spieler=1 oder ?spieler=2 an die URL an.")
    st.stop()

aktueller_spieler = int(spieler_param)
st.set_page_config(page_title="Cabo – Web Edition", page_icon="🧠")

# Spieler-Namen über Sidebar eingeben
st.sidebar.header("👥 Spieler")
spieler1_name = st.sidebar.text_input("Name Spieler 1", "Spieler 1")
spieler2_name = st.sidebar.text_input("Name Spieler 2", "Spieler 2")

# Session State speichern
st.session_state.spieler1_name = spieler1_name
st.session_state.spieler2_name = spieler2_name

# Begrüßung
st.title("🃏 Cabo – Web Edition")
st.success(f"🎮 Du bist: {spieler1_name if aktueller_spieler == 1 else spieler2_name}")

# Beispielkarten (später durch echte Logik ersetzen!)
spieler1_hand = [3, 8, 1, 12]
spieler2_hand = [7, 4, 5, 0]

# Nur eigene Hand anzeigen
if aktueller_spieler == 1:
    st.subheader(f"🃏 {spieler1_name} – deine Karten")
    st.write(spieler1_hand)
elif aktueller_spieler == 2:
    st.subheader(f"🃏 {spieler2_name} – deine Karten")
    st.write(spieler2_hand)

