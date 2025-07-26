import streamlit as st
import random

# Seiteneinstellungen
st.set_page_config(page_title="Cabo Online", page_icon="🃏")

# Spieler-Parameter aus der URL lesen
spieler_param = st.query_params.get("spieler")
if spieler_param not in ["1", "2"]:
    st.error("❌ Bitte verwende ?spieler=1 oder ?spieler=2 in der URL.")
    st.stop()
aktueller_spieler = int(spieler_param)

# Spielername nur für aktuellen Spieler abfragen
st.sidebar.header("Spielereinstellungen")
if f"name_{aktueller_spieler}" not in st.session_state:
    st.session_state[f"name_{aktueller_spieler}"] = st.sidebar.text_input(f"👤 Dein Name (Spieler {aktueller_spieler})", f"Spieler {aktueller_spieler}")

# Initiales Spielsetup
if "deck" not in st.session_state:
    deck = [0, 0] + [n for n in range(1, 13) for _ in range(4)] + [13, 13]
    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.ablagestapel = [deck.pop()]
    st.session_state.s1 = [deck.pop() for _ in range(4)]
    st.session_state.s2 = [deck.pop() for _ in range(4)]
    st.session_state.s1_visible = []
    st.session_state.s2_visible = []
    st.session_state.startphase = True
    st.session_state.cabo_gerufen = False
    st.session_state.am_zug = 1  # Spieler 1 beginnt

# Spielerhände
spieler_hand = st.session_state.s1 if aktueller_spieler == 1 else st.session_state.s2
sichtbare_karten = st.session_state.s1_visible if aktueller_spieler == 1 else st.session_state.s2_visible

# Kartenanzeige
def zeige_karten(hand, sichtbar):
    return " ".join(f"[{wert}]" if i in sichtbar else "[🂠]" for i, wert in enumerate(hand))

# Startphase: 2 Karten auswählen
if st.session_state.startphase:
    st.write("🎯 Wähle zwei deiner Karten zum Anschauen:")
    auswahl = st.multiselect("Position auswählen (0-3)", options=[0, 1, 2, 3], max_selections=2, key="auswahl_start")

    if len(auswahl) == 2:
        sichtbar = st.session_state.s1_visible if aktueller_spieler == 1 else st.session_state.s2_visible
        sichtbar.extend(auswahl)
        st.session_state.startphase = False
        st.rerun()
    else:
        st.stop()

# Anzeige der Hand
st.markdown(f"## Deine Karten:")
st.write(zeige_karten(spieler_hand, sichtbare_karten))

# Weitere Spiellogik (ziehen, tauschen etc.) folgt im nächsten Schritt
