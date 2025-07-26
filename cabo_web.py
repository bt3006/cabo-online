import streamlit as st
import random

st.set_page_config(page_title="Cabo – Web", page_icon="🃏")

# Spieler aus URL bestimmen
spieler_param = st.query_params.get("spieler")
if spieler_param not in ["1", "2"]:
    st.error("Bitte ?spieler=1 oder ?spieler=2 in der URL angeben.")
    st.stop()
aktueller_spieler = int(spieler_param)

# Name nur für aktuellen Spieler
st.sidebar.header(f"Spieler {aktueller_spieler}")
name = st.sidebar.text_input("Dein Name", f"Spieler {spieler_param}")
st.session_state[f"name_{aktueller_spieler}"] = name
st.title(f"🃏 Cabo für {name}")

# Sichtbare Karten anzeigen
def zeige_karten(karten, sichtbar):
    out = []
    for i, karte in enumerate(karten):
        if i in sichtbar:
            out.append(f"[{str(karte).rjust(2)}]")
        else:
            out.append("🂠")
    return " ".join(out)

# Initialisiere Spiel nur einmal
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.deck = random.sample([0, 0] + [n for n in range(1, 13) for _ in range(4)] + [13, 13], 52)
    st.session_state.ablage = [st.session_state.deck.pop()]
    st.session_state.hand_1 = [st.session_state.deck.pop() for _ in range(4)]
    st.session_state.hand_2 = [st.session_state.deck.pop() for _ in range(4)]
    st.session_state.sichtbar_1 = []
    st.session_state.sichtbar_2 = []
    st.session_state.startspieler = random.choice([1, 2])
    st.session_state.dran = st.session_state.startspieler
    st.session_state.cabo_gerufen = False
    st.session_state.cabo_spieler = None
    st.session_state.erste_runde = True

# Sichtbare Karten initial zeigen
sichtbar_key = f"sichtbar_{aktueller_spieler}"
hand_key = f"hand_{aktueller_spieler}"
hand = st.session_state[hand_key]
sichtbar = st.session_state[sichtbar_key]

if st.session_state.erste_runde and not sichtbar:
    st.markdown("👀 Du darfst zwei Karten ansehen")
    erste = st.number_input("Karte 1 (0–3)", 0, 3, key="k1")
    zweite = st.number_input("Karte 2 (0–3)", 0, 3, key="k2")
    if st.button("Anschauen"):
        st.session_state[sichtbar_key] = [erste] if erste == zweite else [erste, zweite]
        st.rerun()
    st.stop()

# Kartenanzeige
sichtbar = st.session_state[sichtbar_key]
st.markdown("### Deine Karten:")
st.write(zeige_karten(hand, sichtbar))

if st.session_state.erste_runde and sichtbar and st.button("Verstanden – weiter"):
    st.session_state[sichtbar_key] = []
    st.session_state.erste_runde = False
    st.rerun()
    st.stop()

# Nur dran, wenn aktueller Spieler an der Reihe
if st.session_state.dran != aktueller_spieler:
    st.info(f"Warte auf {st.session_state[f'name_{st.session_state.dran}']}")
    st.stop()

# Ablagestapel zeigen
ablage_top = st.session_state.ablage[-1]
st.markdown(f"🃫 Ablagestapel: **{ablage_top}**")

# Karte ziehen
if "gezogene_karte" not in st.session_state:
    if st.button("🂠 Karte vom Ziehstapel ziehen"):
        karte = st.session_state.deck.pop()
        st.session_state.gezogene_karte = karte
        st.experimental_rerun()

# Ablage nehmen
if "gezogene_karte" not in st.session_state:
    if st.button("♻️ Karte von Ablagestapel nehmen"):
        karte = st.session_state.ablage.pop()
        st.session_state.gezogene_karte = karte
        st.experimental_rerun()

# Wenn Karte gezogen wurde, Aktionen zeigen
if "gezogene_karte" in st.session_state:
    karte = st.session_state.gezogene_karte
    st.markdown(f"🃏 Du hast gezogen: **{karte}**")

    aktion = st.radio("Was möchtest du tun?", ["Tauschen", "Ablegen", "Mehrere abwerfen"])

    if aktion == "Tauschen":
        pos = st.number_input("Position in deiner Hand (0–3)", 0, len(hand)-1)
        if st.button("Tauschen bestätigen"):
            alt = hand[pos]
            hand[pos] = karte
            st.session_state.ablage.append(alt)
            del st.session_state.gezogene_karte
            st.session_state.dran = 2 if aktueller_spieler == 1 else 1
            st.rerun()

    elif aktion == "Ablegen":
        st.session_state.ablage.append(karte)
        # Spezialfähigkeiten
        if karte in [7, 8]:
            pos = st.number_input("Eigene Karte ansehen (0–3)", 0, 3)
            st.success(f"→ Karte: {hand[pos]}")
        elif karte in [9, 10]:
            gegner = 2 if aktueller_spieler == 1 else 1
            gegner_hand = st.session_state[f"hand_{gegner}"]
            pos = st.number_input("Gegnerkarte ansehen (0–3)", 0, 3)
            st.info(f"→ Gegnerkarte: {gegner_hand[pos]}")
        elif karte in [11, 12]:
            eigene = st.number_input("Eigene Karte zum Tauschen (0–3)", 0, 3)
            gegner = 2 if aktueller_spieler == 1 else 1
            gegner_hand = st.session_state[f"hand_{gegner}"]
            geg = st.number_input("Gegnerkarte (0–3)", 0, 3)
            hand[eigene], gegner_hand[geg] = gegner_hand[geg], hand[eigene]
            st.success("✓ Karten wurden getauscht.")
        else:
            st.info("Keine Spezialfähigkeit.")
        if st.button("Zug beenden"):
            del st.session_state.gezogene_karte
            st.session_state.dran = 2 if aktueller_spieler == 1 else 1
            st.rerun()

    elif aktion == "Mehrere abwerfen":
        st.warning("❗ Noch nicht implementiert.")

# CABO rufen
if not st.session_state.cabo_gerufen:
    if st.button("🚨 Cabo!"):
        st.session_state.cabo_gerufen = True
        st.session_state.cabo_spieler = aktueller_spieler
        st.session_state.dran = 2 if aktueller_spieler == 1 else 1
        st.experimental_rerun()

# Letzter Zug & Auswertung
if st.session_state.cabo_gerufen and st.session_state.dran == st.session_state.cabo_spieler:
    h1 = st.session_state.hand_1
    h2 = st.session_state.hand_2
    p1 = sum(h1)
    p2 = sum(h2)

    st.markdown("## 🧮 Ergebnis")
    st.markdown(f"Spieler 1: {zeige_karten(h1, list(range(4)))} → **{p1} Punkte**")
    st.markdown(f"Spieler 2: {zeige_karten(h2, list(range(4)))} → **{p2} Punkte**")

    if p1 < p2:
        st.success("🏆 Spieler 1 gewinnt!")
    elif p2 < p1:
        st.success("🏆 Spieler 2 gewinnt!")
    else:
        st.warning(f"⚖️ Gleichstand – Cabo-Rufer verliert! Spieler {st.session_state.cabo_spieler}")
