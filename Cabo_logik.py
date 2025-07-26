import random

# -----------------------------
# Phase 1: Schnick Schnack Schnuck
# -----------------------------
def schnick_schnack_schnuck():
    regeln = {"stein": "schere", "schere": "papier", "papier": "stein"}
    print("🪨✂️📄 Schnick Schnack Schnuck – Wer fängt an?")

    while True:
        spieler1 = input("Spieler 1, wähle (stein/schere/papier): ").lower()
        spieler2 = input("Spieler 2, wähle (stein/schere/papier): ").lower()

        if spieler1 not in regeln or spieler2 not in regeln:
            print("Ungültige Eingabe. Bitte nochmal.")
            continue
        print(f"Spieler 1 wählte: {spieler1}")
        print(f"Spieler 2 wählte: {spieler2}")

        if spieler1 == spieler2:
            print("Unentschieden – nochmal!")
        elif regeln[spieler1] == spieler2:
            print("🎉 Spieler 1 gewinnt und beginnt!")
            return 1
        else:
            print("🎉 Spieler 2 gewinnt und beginnt!")
            return 2

# -----------------------------
# Kartendeck & Spielstart
# -----------------------------
def erstelle_deck():
    return random.sample([0, 0] + [n for n in range(1, 13) for _ in range(4)] + [13, 13], 52)

def teile_karten_aus(deck):
    return [deck.pop() for _ in range(4)], [deck.pop() for _ in range(4)], deck

def karten_anzeigen(spieler, nr):
    print(f"\nSpieler {nr}, du darfst 2 Karten anschauen.")
    print(["🂠"] * len(spieler))
    gesehen = set()
    while len(gesehen) < 2:
        i = input("Welche Position? (0-3): ")
        if i.isdigit() and 0 <= int(i) <= 3 and int(i) not in gesehen:
            i = int(i)
            print(f"→ Karte {i}: {spieler[i]}")
            gesehen.add(i)
        else:
            print("Ungültige Eingabe oder bereits gesehen.")
    input("Drücke Enter zum Fortfahren.")
    print("\n" * 50)

def ziehe_karte(deck, ablage):
    if not deck:
        print("Ziehstapel leer. Ablage wird gemischt.")
        top = ablage.pop()
        deck[:] = ablage
        random.shuffle(deck)
        ablage[:] = [top]
    return deck.pop()

# -----------------------------
# Spielzug
# -----------------------------
def spielzug(spieler, nr, deck, ablage, gegner):
    print(f"🔁 Spieler {nr} ist am Zug.")
    print("Deine Karten: [" + " ".join(["🂠"] * len(spieler)) + "]")
    print(f"Ablagestapel zeigt: {ablage[-1]}")

    # Karte ziehen oder Ablage nehmen
    while True:
        quelle = input("Ziehen (z) oder Ablage nehmen (a)? ").lower()
        if quelle == "a":
            gez = ablage.pop()
            von_wo = "ablage"
            break
        elif quelle == "z":
            gez = ziehe_karte(deck, ablage)
            print(f"Du hast gezogen: {gez}")
            von_wo = "ziehstapel"
            break
        else:
            print("Bitte 'z' oder 'a' eingeben.")

    # Aktion wählen
    while True:
        wahl = input("Tauschen (t), ablegen (l), oder mehrere ablegen (m)? ").lower()
        if wahl == "t":
            idx = input("Welche deiner Karten tauschen? (0-{}): ".format(len(spieler) - 1))
            if idx.isdigit() and 0 <= int(idx) < len(spieler):
                idx = int(idx)
                alt = spieler[idx]
                spieler[idx] = gez
                ablage.append(alt)
                print(f"✓ Du hast getauscht: {alt} → {gez}")
                break
        elif wahl == "l":
            ablage.append(gez)
            print("✓ Karte wurde abgelegt.")
            if von_wo == "ziehstapel":
                if gez in [7, 8]:
                    pos = int(input("Eigene Karte ansehen (0–{}): ".format(len(spieler) - 1)))
                    print(f"→ Deine Karte: {spieler[pos]}")
                elif gez in [9, 10]:
                    pos = int(input("Gegnerkarte ansehen (0–{}): ".format(len(gegner) - 1)))
                    print(f"→ Gegnerkarte: {gegner[pos]}")
                elif gez in [11, 12]:
                    e = int(input("Deine Karte zum Tauschen (0–{}): ".format(len(spieler) - 1)))
                    f = int(input("Gegnerkarte tauschen (0–{}): ".format(len(gegner) - 1)))
                    spieler[e], gegner[f] = gegner[f], spieler[e]
                    print("✓ Karten wurden getauscht.")
            else:
                print("ℹ️ Keine Fähigkeit – Karte kam nicht vom Ziehstapel.")
            break
        elif wahl == "m":
            n = int(input("Wie viele Karten willst du mit abwerfen (1–{}): ".format(len(spieler))))
            positionen = []
            for i in range(n):
                p = input(f"Position {i+1}: ")
                if p.isdigit() and 0 <= int(p) < len(spieler):
                    pos = int(p)
                    if pos not in positionen:
                        positionen.append(pos)
            werte = [spieler[p] for p in positionen]
            if all(w == gez for w in werte):
                print("✅ Alles korrekt! Karten werden abgelegt.")
                for p in sorted(positionen, reverse=True):
                    ablage.append(spieler.pop(p))
                ablage.append(gez)
            else:
                print("❌ Falsch geraten – Strafkarte wird hinzugefügt.")
                spieler.append(gez)
                random.shuffle(spieler)
            break
        else:
            print("Ungültige Eingabe.")

    input("Drücke Enter für den nächsten Spieler.\n")
    print("\n" * 50)

# -----------------------------
# Kartenanzeige & Punkte
# -----------------------------
def zeige_karten(hand):
    return " ".join(f"[{str(wert).rjust(2)}]" for wert in hand)

def berechne_punkte(hand):
    return sum(hand)

# -----------------------------
# Hauptprogramm
# -----------------------------
def main():
    print("🎮 Willkommen bei CABO!")
    startspieler = schnick_schnack_schnuck()
    deck = erstelle_deck()
    s1, s2, deck = teile_karten_aus(deck)
    ablage = [deck.pop()]
    karten_anzeigen(s1, 1)
    karten_anzeigen(s2, 2)

    spieler = [s1, s2]
    namen = ["Spieler 1", "Spieler 2"]
    i = startspieler - 1
    cabo_spieler = None

    while True:
        gegner = spieler[1 - i]
        spielzug(spieler[i], i + 1, deck, ablage, gegner)
        cabo = input("Willst du 'Cabo!' rufen? (j/n): ").lower()
        if cabo == "j":
            cabo_spieler = i
            print(f"🚨 {namen[i]} ruft 'CABO!'")
            break
        i = 1 - i

    # Letzter Zug für den anderen Spieler
    print(f"{namen[1 - cabo_spieler]} darf noch einen Zug machen.")
    spielzug(spieler[1 - cabo_spieler], 2 if cabo_spieler == 0 else 1, deck, ablage, spieler[cabo_spieler])

    # Auswertung
    p1 = berechne_punkte(s1)
    p2 = berechne_punkte(s2)
    print("\n🔍 Runde beendet!\n")
    print(f"Spieler 1: {zeige_karten(s1)} → {p1} Punkte")
    print(f"Spieler 2: {zeige_karten(s2)} → {p2} Punkte")

    if p1 < p2:
        print("🏆 Spieler 1 gewinnt die Runde!")
    elif p2 < p1:
        print("🏆 Spieler 2 gewinnt die Runde!")
    else:
        verlierer = cabo_spieler + 1
        print(f"⚖️ Gleichstand – Cabo-Rufer verliert! 🟥 Spieler {verlierer}")

if __name__ == "__main__":
    main()
