import streamlit as st
import random

st.set_page_config(page_title="Cabo – Web Edition", page_icon="🃏")

# Spieler aus URL abfragen
spieler_param = st.query_params.get("spieler")

if spieler_param not in ["1", "2"]:
    st.error("❌ Du musst ?spieler=1 oder ?spieler=2 in der URL angeben.")
    st.stop()

aktueller_spieler = int(spieler_param)

# Spielername individuell
st.sidebar.header(f"Einstellungen Spieler {aktueller_spieler}")
spieler_name = st.sidebar.text_input("👤 Dein Name", f"Spieler {aktueller_spieler}")
st.session_state[f"spieler{aktueller_spieler}_name"] = spieler_name

st.title(f"🃏 Cabo für {spieler_name}")

# Kartenanzeige: Sichtbare Positionen berücksichtigen
def zeige_karten_liste(karten, sichtbar_pos):
    output = []
    for i, k in enumerate(karten):
        if i in sichtbar_pos:
            output.append(f"[{str(k).rjust(2)}]")
        else:
            output.append("🂠")
    return " ".join(output)

# Deck initialisieren
if "deck" not in st.session_state:
    st.session_state.deck = random.sample([0, 0] + [n for n in range(1, 13) for _ in range(4)] + [13, 13], 52)

deck = st.session_state.deck

# Kartenhand initialisieren
hand_key = f"hand_{aktueller_spieler}"
sichtbar_key = f"sichtbar_{aktueller_spieler}"

if hand_key not in st.session_state:
    st.session_state[hand_key] = [deck.pop() for _ in range(4)]
    st.session_state[sichtbar_key] = []

    st.markdown("👀 Du darfst zwei deiner vier Karten anschauen:")
    erste = st.number_input("➀ Position der ersten Karte (0–3)", min_value=0, max_value=3, key="erste_karte")
    zweite = st.number_input("➁ Position der zweiten Karte (0–3)", min_value=0, max_value=3, key="zweite_karte")

    if st.button("✅ Karten anschauen"):
        sichtbar = [erste]
        if zweite != erste:
            sichtbar.append(zweite)
        st.session_state[sichtbar_key] = sichtbar
        st.rerun()

# Karten anzeigen
hand = st.session_state[hand_key]
sichtbare = st.session_state[sichtbar_key]

st.markdown("## 🎴 Deine Karten:")
st.write(zeige_karten_liste(hand, sichtbare))

# Sichtbarkeit nach Start wieder entfernen
if sichtbare and "erste_runde_abgeschlossen" not in st.session_state:
    if st.button("🕵️‍♂️ Verstanden, Karten verbergen"):
        st.session_state[sichtbar_key] = []
        st.session_state["erste_runde_abgeschlossen"] = True
        st.rerun()
