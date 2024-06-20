
# PortChecker

Ein Python-basiertes GUI-Tool zum Scannen von IP-Bereichen auf offene Ports. Das Tool verwendet `PyQt5` für die grafische Benutzeroberfläche und führt den Scan in parallelen Threads durch, um die Effizienz zu erhöhen.

## Voraussetzungen

Stelle sicher, dass die folgenden Abhängigkeiten installiert sind:

- [Python 3](https://www.python.org/downloads/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- `socket` (in der Standardbibliothek enthalten)

Du kannst die benötigten Python-Bibliotheken mit folgendem Befehl installieren:

```bash
pip install PyQt5
```

## Installation

1. Klone dieses Repository oder lade die ZIP-Datei herunter und entpacke sie.

2. Stelle sicher, dass das Skript ausführbar ist:

    ```bash
    chmod +x port_checker.py
    ```

## Verwendung

1. Starte das Skript:

    ```bash
    python port_checker.py
    ```

2. Gib einen IP-Bereich im Format `192.168.1.1-255` ein und klicke auf "Check".

3. Die Ergebnisse werden im Textbereich angezeigt. Offene Ports werden nach IP-Adresse, Portnummer und Hostname aufgelistet.

4. Um die Ergebnisse als CSV-Datei zu exportieren, klicke auf "Ergebnisse als CSV".

## Funktionen

- **IP-Bereich Scannen**: Scannt einen angegebenen IP-Bereich auf offene Ports von 1 bis 2023.
- **Paralleles Scannen**: Verwendet Threads, um mehrere Ports gleichzeitig zu scannen und die Scan-Geschwindigkeit zu erhöhen.
- **Ergebnisse Speichern**: Exportiert die Scan-Ergebnisse als CSV-Datei.
- **GUI**: Einfache Benutzeroberfläche mit PyQt5.

## Beispiel

### Beispielausführung mit einem IP-Bereich:

1. Geben Sie die Ziel-URL ein (z.B. `192.168.1.1-10`) und klicken Sie auf "Check".
2. Der Scanvorgang beginnt und die Ergebnisse werden im Textbereich angezeigt.
3. Klicken Sie auf "Ergebnisse als CSV", um die Ergebnisse als CSV-Datei zu speichern.

## Hinweise

- Stellen Sie sicher, dass `PyQt5` korrekt installiert ist.
- Das Skript sollte in einer sicheren und kontrollierten Umgebung verwendet werden.

## Haftungsausschluss

Dieses Tool sollte nur in einer sicheren und kontrollierten Umgebung verwendet werden. Unbefugtes Durchführen von Netzwerkscans ist illegal und strafbar. Der Autor übernimmt keine Verantwortung für Missbrauch oder Schäden, die durch die Nutzung dieses Tools entstehen.
