import streamlit as st
import random

st.set_page_config(page_title="Cabo – Web Edition", page_icon="🃏")

# Spielerabfrage aus URL (?spieler=1 oder ?spieler=2)
spieler_param = st.query_params.get("spieler")
if spieler_param not in ["1", "2"]:
    st.error("❌ Du musst ?spieler=1 oder ?spieler=2 in der URL angeben.")
    st.stop()

aktueller_spieler = int(spieler_param)

# Titel
st.title("🃏 Cabo – Web Edition")

# Session-Init
if "namen_eingegeben" not in st.session_state:
    st.session_state.namen_eingegeben = False
if "name" not in st.session_state:
    st.session_state.name = ["Spieler 1", "Spieler 2"]

# Namenseingabe (nur für den aktuellen Spieler)
if not st.session_state.namen_eingegeben:
    st.header("👤 Name eingeben")
    eingabe_name = st.text_input("Dein Name", f"Spieler {aktueller_spieler}")
    if st.button("Bestätigen"):
        st.session_state.name[aktueller_spieler - 1] = eingabe_name
        st.session_state.namen_eingegeben = True
        st.experimental_rerun()
    st.stop()

# Deck & Hände initialisieren
if "deck" not in st.session_state:
    deck = random.sample([0, 0] + [n for n in range(1, 13) for _ in range(4)] + [13, 13], 52)
    st.session_state.deck = deck
    st.session_state.s1 = [deck.pop() for _ in range(4)]
    st.session_state.s2 = [deck.pop() for _ in range(4)]
    st.session_state.ablage = [deck.pop()]
    st.session_state.gesehen = [set(), set()]
    st.session_state.startspieler = None
    st.session_state.dran = None
    st.session_state.cabo_gerufen = False
    st.session_state.finale_runde = False

# Namen laden
s1_name, s2_name = st.session_state.name
hand = st.session_state.s1 if aktueller_spieler == 1 else st.session_state.s2
gegner = st.session_state.s2 if aktueller_spieler == 1 else st.session_state.s1
gesehen = st.session_state.gesehen[aktueller_spieler - 1]

# -----------------------------
# Schnick-Schnack-Schnuck
# -----------------------------
if st.session_state.startspieler is None:
    st.subheader("🪨 Schnick-Schnack-Schnuck")

    if "schnick" not in st.session_state:
        st.session_state.schnick = ["", ""]

    wahl = st.radio("Was wählst du?", ["stein", "papier", "schere"], key=f"wahl{aktueller_spieler}")
    if st.button("Bestätigen", key=f"ss_bestätigen{aktueller_spieler}"):
        st.session_state.schnick[aktueller_spieler - 1] = wahl

    if all(st.session_state.schnick):
        s1, s2 = st.session_state.schnick
        regeln = {"stein": "schere", "schere": "papier", "papier": "stein"}
        st.write(f"🧍‍♂️ {s1_name} wählte: **{s1}**")
        st.write(f"🧍‍♀️ {s2_name} wählte: **{s2}**")

        if s1 == s2:
            st.warning("⚖️ Unentschieden – bitte erneut wählen.")
            st.session_state.schnick = ["", ""]
            st.stop()
        elif regeln[s1] == s2:
            st.success(f"🎉 {s1_name} beginnt!")
            st.session_state.startspieler = 0
        else:
            st.success(f"🎉 {s2_name} beginnt!")
            st.session_state.startspieler = 1

        st.session_state.dran = st.session_state.startspieler
        st.experimental_rerun()
    else:
        st.stop()
# -----------------------------
# Kartenanzeige (2 Karten zu Beginn)
# -----------------------------
st.subheader(f"🎮 {st.session_state.name[aktueller_spieler - 1]} – du bist dran!")

if len(st.session_state.gesehen[aktueller_spieler - 1]) < 2:
    st.write("Du darfst dir 2 deiner Karten ansehen.")
    for i in range(4):
        if i in gesehen:
            st.markdown(f"**🃏 Karte {i}**: `{hand[i]}`")
        else:
            if st.button(f"Karte {i} ansehen", key=f"sehen_{i}_{aktueller_spieler}"):
                gesehen.add(i)
                st.experimental_rerun()
    st.stop()
else:
    st.info("🕵️ Karten wieder verdeckt.")
    karten_anzeige = ["🂠" for _ in hand]
    st.write("Deine Karten: " + " ".join(karten_anzeige))
# -----------------------------
# Spielzug
# -----------------------------
quelle = st.radio("Willst du ziehen oder die Ablage nehmen?", ["Ziehen", "Ablage"], key=f"quelle_{aktueller_spieler}")
if st.button("Karte nehmen", key=f"karte_{aktueller_spieler}"):
    if quelle == "Ablage":
        gez = ablage.pop()
        st.session_state.gezogen = gez
        st.session_state.von_wo = "ablage"
    else:
        gez = ziehe_karte(st.session_state.deck, ablage)
        st.session_state.gezogen = gez
        st.session_state.von_wo = "ziehstapel"
    st.experimental_rerun()

if "gezogen" in st.session_state:
    gez = st.session_state.gezogen
    st.write(f"📥 Du hast gezogen: **{gez}**")

    aktion = st.radio("Was willst du tun?", ["Tauschen", "Ablegen", "Mehrere ablegen"], key=f"aktion_{aktueller_spieler}")

    if aktion == "Tauschen":
        pos = st.number_input("Welche deiner Karten willst du tauschen?", 0, 3, 0, key=f"tausch_{aktueller_spieler}")
        if st.button("Tauschen bestätigen", key=f"tauschbestätigen_{aktueller_spieler}"):
            alt = hand[pos]
            hand[pos] = gez
            ablage.append(alt)
            del st.session_state["gezogen"]
            st.success(f"Tausch erfolgreich: {alt} → {gez}")
            st.experimental_rerun()

    elif aktion == "Ablegen":
        ablage.append(gez)
        if st.session_state.von_wo == "ziehstapel":
            if gez in [7, 8]:
                pos = st.number_input("Welche eigene Karte ansehen?", 0, 3, 0, key=f"sehen_eigene_{aktueller_spieler}")
                st.info(f"Karte {pos}: `{hand[pos]}`")
            elif gez in [9, 10]:
                pos = st.number_input("Welche Gegnerkarte ansehen?", 0, 3, 0, key=f"sehen_gegner_{aktueller_spieler}")
                st.info(f"Gegnerkarte {pos}: `{gegner[pos]}`")
            elif gez in [11, 12]:
                e = st.number_input("Deine Karte zum Tauschen", 0, 3, 0, key=f"tausch_du_{aktueller_spieler}")
                f = st.number_input("Gegnerkarte zum Tauschen", 0, 3, 0, key=f"tausch_gegner_{aktueller_spieler}")
                hand[e], gegner[f] = gegner[f], hand[e]
                st.success("Karten wurden getauscht.")
        else:
            st.info("Keine Fähigkeit – Karte kam nicht vom Ablagestapel.")
        del st.session_state["gezogen"]
        st.experimental_rerun()

    elif aktion == "Mehrere ablegen":
        pos_liste = st.text_input("Positionen mit gleichem Wert (z. B. 0,2)", key=f"multi_{aktueller_spieler}")
        if st.button("Abwerfen bestätigen", key=f"multi_button_{aktueller_spieler}"):
            try:
                indices = [int(p.strip()) for p in pos_liste.split(",")]
                werte = [hand[i] for i in indices]
                if all(w == gez for w in werte):
                    for p in sorted(indices, reverse=True):
                        ablage.append(hand.pop(p))
                    ablage.append(gez)
                    del st.session_state["gezogen"]
                    st.success("Karten korrekt abgelegt.")
                    st.experimental_rerun()
                else:
                    st.warning("Falscher Wert – Strafkarte erhalten.")
                    hand.append(gez)
                    random.shuffle(hand)
                    del st.session_state["gezogen"]
                    st.experimental_rerun()
            except:
                st.error("Fehlerhafte Eingabe.")
# -----------------------------
# Cabo rufen
# -----------------------------
if "cabo" not in st.session_state:
    if st.button("🚨 Cabo! rufen", key=f"cabo_{aktueller_spieler}"):
        st.session_state.cabo = aktueller_spieler
        st.success(f"{spieler_name} hat **Cabo!** gerufen!")

# -----------------------------
# Letzter Spielzug des Gegners
# -----------------------------
if "cabo" in st.session_state and aktueller_spieler != st.session_state.cabo and "letzter_zug" not in st.session_state:
    st.info("🚨 Du hast einen letzten Zug, weil dein Gegner Cabo gerufen hat!")
    st.session_state.letzter_zug = True
elif "cabo" in st.session_state and aktueller_spieler == st.session_state.cabo:
    st.warning("Bitte auf den letzten Spielzug des Gegners warten.")
    st.stop()

# -----------------------------
# Punkte berechnen & Gewinner
# -----------------------------
if "cabo" in st.session_state and "letzter_zug" in st.session_state and aktueller_spieler != st.session_state.cabo:
    p1 = berechne_punkte(st.session_state.spieler1)
    p2 = berechne_punkte(st.session_state.spieler2)

    st.subheader("🏁 Spiel beendet!")
    st.write(f"**{spieler1_name}**: {zeige_karten(st.session_state.spieler1)} → **{p1} Punkte**")
    st.write(f"**{spieler2_name}**: {zeige_karten(st.session_state.spieler2)} → **{p2} Punkte**")

    if p1 < p2:
        st.success(f"🏆 {spieler1_name} gewinnt die Runde!")
    elif p2 < p1:
        st.success(f"🏆 {spieler2_name} gewinnt die Runde!")
    else:
        verlierer = spieler1_name if st.session_state.cabo == 1 else spieler2_name
        st.error(f"⚖️ Gleichstand – Cabo-Rufer **{verlierer}** verliert!")

    # Neustart-Button
    if st.button("🔁 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
