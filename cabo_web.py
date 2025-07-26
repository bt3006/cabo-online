import streamlit as st
import random

# Spieler aus URL abfragen
spieler_param = st.query_params.get("spieler")
if spieler_param not in ["1", "2"]:
    st.error("❌ Bitte hänge ?spieler=1 oder ?spieler=2 an die URL an.")
    st.stop()

spieler_nummer = int(spieler_param)
st.set_page_config(page_title=f"Cabo für Spieler {spieler_nummer}", page_icon="🃏")

# Sidebar: nur der aktuelle Spieler gibt seinen Namen ein
st.sidebar.header("🧑 Spielername")
spieler_name = st.sidebar.text_input("Wie heißt du?", f"Spieler {spieler_nummer}")
st.session_state[f"name_{spieler_nummer}"] = spieler_name

# Begrüßung
st.title(f"🃏 Cabo für Spieler {spieler_nummer}")
st.success(f"🎮 Du bist: {spieler_name}")

# Hilfsfunktion: verdeckte Karten anzeigen
def verdeckt_anzeigen():
    return ["🂠"] * 4

# Initialisierung beim ersten Laden
if "spielgestartet" not in st.session_state:
    # Karten mischen und austeilen
    deck = random.sample([0, 0] + [n for n in range(1, 13) for _ in range(4)] + [13, 13], 52)
    st.session_state.deck = deck
    st.session_state.ablage = [deck.pop()]
    st.session_state.karten_spieler1 = [deck.pop() for _ in range(4)]
    st.session_state.karten_spieler2 = [deck.pop() for _ in range(4)]
    st.session_state.kenntnis_spieler1 = [False, False, False, False]
    st.session_state.kenntnis_spieler2 = [False, False, False, False]
    st.session_state.verstanden = {1: False, 2: False}
    st.session_state.spielgestartet = True

# Spiellogik für aktuellen Spieler
karten = st.session_state[f"karten_spieler{spieler_nummer}"]
kenntnis = st.session_state[f"kenntnis_spieler{spieler_nummer}"]
verstanden = st.session_state.verstanden[spieler_nummer]

# Anzeige vor "Verstanden"-Klick: zwei Karten sichtbar
if not verstanden:
    st.subheader("🃏 Deine Karten:")
    sichtbare_karten = []
    for i in range(4):
        if sum(kenntnis) < 2 and not kenntnis[i]:
            st.session_state[f"show_{i}"] = st.button(f"Karte {i + 1} ansehen")
            if st.session_state.get(f"show_{i}"):
                kenntnis[i] = True

        if kenntnis[i]:
            sichtbare_karten.append(f"[{karten[i]}]")
        else:
            sichtbare_karten.append("🂠")
    st.write(" ".join(sichtbare_karten))

    # Wenn zwei Karten aufgedeckt wurden, Button anzeigen
    if sum(kenntnis) == 2:
        if st.button("Verstanden – weiter"):
            st.session_state.verstanden[spieler_nummer] = True
            st.rerun()
else:
    # Nach "Verstanden" alles verdeckt
    st.subheader("🃏 Deine Karten:")
    st.write(" ".join(verdeckt_anzeigen()))
