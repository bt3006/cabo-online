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
# Nächster Spieler am Zug
if st.session_state.am_zug != aktueller_spieler:
    st.info("⏳ Du bist nicht am Zug. Warte, bis du dran bist.")
    st.stop()

st.markdown("## Dein Zug")

# Karte ziehen oder Ablage nehmen
aktion = st.radio("Wähle eine Aktion:", ["Ziehen vom Stapel", "Oberste Karte vom Ablagestapel nehmen"])
if "gezogene_karte" not in st.session_state:
    if st.button("Karte nehmen"):
        if aktion == "Ziehen vom Stapel":
            if not st.session_state.deck:
                st.session_state.deck = st.session_state.ablagestapel[:-1]
                random.shuffle(st.session_state.deck)
                st.session_state.ablagestapel = [st.session_state.ablagestapel[-1]]
            gez = st.session_state.deck.pop()
            st.session_state.gezogene_karte = gez
            st.session_state.von_ablagestapel = False
        else:
            gez = st.session_state.ablagestapel.pop()
            st.session_state.gezogene_karte = gez
            st.session_state.von_ablagestapel = True
        st.rerun()

# Wenn Karte gezogen wurde – nächste Aktion
if "gezogene_karte" in st.session_state:
    gez = st.session_state.gezogene_karte
    st.success(f"Du hast gezogen: [{gez}]")

    wahl = st.radio("Was möchtest du tun?", ["Tauschen", "Ablegen", "Mehrere Karten abwerfen"])

    if wahl == "Tauschen":
        pos = st.number_input("Welche deiner Karten willst du tauschen? (0–3)", min_value=0, max_value=3, step=1)
        if st.button("Tauschen bestätigen"):
            alt = spieler_hand[pos]
            spieler_hand[pos] = gez
            st.session_state.ablagestapel.append(alt)
            st.session_state.gezogene_karte = None
            st.session_state.am_zug = 2 if aktueller_spieler == 1 else 1
            st.rerun()

    elif wahl == "Ablegen":
        st.session_state.ablagestapel.append(gez)
        # Wenn Karte vom Stapel und mit Fähigkeit
        if not st.session_state.von_ablagestapel and gez in [7, 8]:
            pos = st.number_input("Welche eigene Karte willst du anschauen? (0–3)", min_value=0, max_value=3, step=1)
            st.info(f"Deine Karte an Position {pos}: [{spieler_hand[pos]}]")
            if pos not in sichtbare_karten:
                sichtbare_karten.append(pos)

        elif not st.session_state.von_ablagestapel and gez in [9, 10]:
            st.warning("🔍 Gegnerkarte ansehen – noch nicht umgesetzt.")
        elif not st.session_state.von_ablagestapel and gez in [11, 12]:
            st.warning("♻️ Karten tauschen – noch nicht umgesetzt.")

        st.session_state.gezogene_karte = None
        st.session_state.am_zug = 2 if aktueller_spieler == 1 else 1
        st.rerun()

    elif wahl == "Mehrere Karten abwerfen":
        gleiche_pos = st.multiselect("Welche deiner Karten willst du abwerfen?", options=[0, 1, 2, 3])
        if len(gleiche_pos) >= 1:
            werte = [spieler_hand[i] for i in gleiche_pos]
            if all(w == gez for w in werte):
                st.success("✅ Alles korrekt! Karten werden abgelegt.")
                for i in sorted(gleiche_pos, reverse=True):
                    st.session_state.ablagestapel.append(spieler_hand.pop(i))
                st.session_state.ablagestapel.append(gez)
            else:
                st.error("❌ Nicht alle Karten passen – Strafkarte wird hinzugefügt.")
                spieler_hand.append(gez)
                random.shuffle(spieler_hand)
            st.session_state.gezogene_karte = None
            st.session_state.am_zug = 2 if aktueller_spieler == 1 else 1
            st.rerun()
