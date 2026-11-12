# Trainingswoche als Android-App

GitHub baut aus diesen Dateien automatisch eine Android-App (APK). Du brauchst dafür weder Android Studio noch einen eigenen Rechner.

## Einmalig einrichten

**1. Repository anlegen**
Auf github.com oben rechts auf „+“ → „New repository“. Name: `trainingswoche-app`, Sichtbarkeit **Public**, ohne Haken bei „Add a README“. „Create repository“.

**2. Signaturschlüssel hinterlegen (vor dem Hochladen!)**
Im neuen Repository: „Settings“ → links „Secrets and variables“ → „Actions“ → „New repository secret“. Zwei Geheimnisse anlegen, jeweils mit „Add secret“:
- Name: `KEYSTORE_BASE64`, Secret: der komplette Inhalt der Datei `KEYSTORE_BASE64.txt` (eine lange Zeile, alles markieren und kopieren)
- Name: `KEYSTORE_PASSWORD`, Secret: der Inhalt der Datei `KEYSTORE_PASSWORD.txt`
Dieser Schlüssel signiert deine App. Mit demselben Schlüssel lassen sich spätere Versionen über die alte installieren, ohne dass Daten verloren gehen. Heb `KEYSTORE_BASE64.txt`, `KEYSTORE_PASSWORD.txt` und `trainingswoche.p12` gut auf (zum Beispiel in einem Passwortmanager) und lade sie **nie** ins Repository hoch. Ein Secret kann man bei GitHub nach dem Speichern nicht mehr ansehen, nur neu setzen.

**3. Dateien hochladen**
Im Repository auf „uploading an existing file“ und alle Dateien und Ordner aus diesem Ordner hineinziehen, **auch den Ordner `.github`** (unter Windows: im Explorer „Ansicht → Anzeigen → Ausgeblendete Elemente“ einschalten). Dann ganz unten „Commit changes“.
Falls der Ordner `.github` nicht mitkommt: „Add file“ → „Create new file“, als Name `.github/workflows/build-apk.yml` eintippen (die Schrägstriche legen die Ordner an) und den Inhalt der Datei `build-apk.yml` aus diesem Ordner hineinkopieren, dann „Commit“.

**4. Warten**
Oben im Repository auf „Actions“. Dort läuft „APK bauen“ (etwa 5 bis 10 Minuten). Ein grüner Haken heißt fertig. Bei einem roten Kreuz: den Lauf öffnen, die rote Fehlermeldung kopieren und an Claude schicken.

**5. APK holen und installieren**
Auf der Startseite des Repositorys rechts auf „Releases“ → die neueste Version → `Trainingswoche-….apk` aufs Handy laden und öffnen. Android fragt einmal, ob dem Browser oder Dateimanager die Installation erlaubt ist („Aus dieser Quelle zulassen“). Google Play Protect kann warnen, weil die App nicht im Play Store ist: „Trotzdem installieren“.

**6. Benachrichtigungen**
Beim ersten Öffnen fragt Android nach der Erlaubnis für Benachrichtigungen: „Zulassen“. Unter Einstellungen → Benachrichtigungen in der App kannst du alles anpassen und mit „Test in 5 Sekunden“ prüfen. Kommen Meldungen verspätet oder gar nicht, dann in den Handy-Einstellungen unter Akku der App erlauben, im Hintergrund zu laufen (bei Huawei und Xiaomi zusätzlich „Autostart“).

**7. Daten aus der bisherigen Web-App übernehmen**
Die App hat einen eigenen Speicher, getrennt von der Web-App. In der Web-App: Einstellungen → Backup → „Backup speichern“ (auf dem Handy: in Google Drive oder an dich selbst mailen). In der Android-App: Einstellungen → Backup → Datei auswählen und einspielen.

## Neue Version einspielen
Neue `index.html` im Repository ersetzen („Add file“ → „Upload files“, gleiche Datei überschreiben). Der Build startet von selbst, danach liegt unter „Releases“ die neue APK. Einfach über die alte installieren, die Daten bleiben erhalten. Hat das Handy mehr als 14 Tage nicht geöffnet, laufen die geplanten Erinnerungen aus, bis du die App wieder öffnest.

## Für Freunde
Schick ihnen den Link zur „Releases“-Seite des Repositorys. Die Installation ist wie in Schritt 5. Android-Handys brauchen keine Konten, iPhones können die APK nicht nutzen.
