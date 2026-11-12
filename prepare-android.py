#!/usr/bin/env python3
"""Passt das frisch erzeugte Android-Projekt an (läuft im GitHub-Build nach "npx cap add android"):
Symbole der App, Symbol der Benachrichtigungen, schwarzer Startbildschirm, Berechtigungen, Versionsnummern.
Aufruf: python3 prepare-android.py  (im Hauptordner des Repositorys)"""
import os
import pathlib
import re
import sys

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent
ANDROID = ROOT / "android"
MAIN = ANDROID / "app" / "src" / "main"
RES = MAIN / "res"


def warn(msg):
    print("WARNUNG: " + msg)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def icons():
    src = Image.open(ROOT / "icon.png").convert("RGB")
    legacy = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    for dens, px in legacy.items():
        d = RES / ("mipmap-" + dens)
        d.mkdir(parents=True, exist_ok=True)
        sq = src.resize((px, px), Image.LANCZOS)
        sq.save(d / "ic_launcher.png")
        # rund: Kreis ausschneiden
        big = px * 4
        mask = Image.new("L", (big, big), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, big - 1, big - 1], fill=255)
        mask = mask.resize((px, px), Image.LANCZOS)
        rnd = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        rnd.paste(sq, (0, 0), mask)
        rnd.save(d / "ic_launcher_round.png")
        # Vordergrund für das anpassbare Symbol: 108 dp, Motiv bleibt in der Sicherheitszone
        fpx = round(px * 108 / 48)
        fg = Image.new("RGB", (fpx, fpx), (0, 0, 0))
        inner = round(fpx * 0.80)
        fg.paste(src.resize((inner, inner), Image.LANCZOS), ((fpx - inner) // 2, (fpx - inner) // 2))
        fg.save(d / "ic_launcher_foreground.png")
    adaptive = ('<?xml version="1.0" encoding="utf-8"?>\n'
                '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                '    <background android:drawable="@color/ic_launcher_background"/>\n'
                '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
                '</adaptive-icon>\n')
    write(RES / "mipmap-anydpi-v26" / "ic_launcher.xml", adaptive)
    write(RES / "mipmap-anydpi-v26" / "ic_launcher_round.xml", adaptive)
    write(RES / "values" / "ic_launcher_background.xml",
          '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#000000</color>\n</resources>\n')
    # Symbole der Vorlage, die nicht zu unserem Foto-Foreground passen, ersetzen wir oben; alte Vordergrund-Dateien im Format .xml entfernen
    for old in RES.glob("drawable*/ic_launcher_foreground.xml"):
        old.unlink()


def notification_icon():
    write(RES / "drawable" / "ic_stat_trainingswoche.xml",
          '<?xml version="1.0" encoding="utf-8"?>\n'
          '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
          '    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">\n'
          '    <path android:strokeColor="#FFFFFF" android:strokeWidth="2" android:strokeLineCap="round"\n'
          '        android:pathData="M6.5,6.5L6.5,17.5M17.5,6.5L17.5,17.5M3.5,9L3.5,15M20.5,9L20.5,15M6.5,12L17.5,12"/>\n'
          '</vector>\n')


def splash():
    removed = 0
    for p in RES.glob("drawable*/splash.png"):
        p.unlink()
        removed += 1
    write(RES / "drawable" / "splash.xml",
          '<?xml version="1.0" encoding="utf-8"?>\n'
          '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">\n'
          '    <solid android:color="#000000"/>\n</shape>\n')
    print("Startbild: %d Vorlagen entfernt, schwarzer Hintergrund gesetzt" % removed)


def styles():
    p = RES / "values" / "styles.xml"
    if not p.exists():
        warn("styles.xml nicht gefunden")
        return
    s = p.read_text(encoding="utf-8")
    add = ('        <item name="android:statusBarColor">#000000</item>\n'
           '        <item name="android:navigationBarColor">#000000</item>\n')
    m = re.search(r'(<style name="AppTheme\.NoActionBar"[^>]*>)(.*?)(</style>)', s, re.S)
    if not m:
        warn("Stil AppTheme.NoActionBar nicht gefunden, Statusleiste bleibt in der Standardfarbe")
        return
    if "statusBarColor" in m.group(2):
        return
    s = s[:m.end(2)] + add + s[m.end(2):]
    p.write_text(s, encoding="utf-8")


def manifest():
    p = MAIN / "AndroidManifest.xml"
    s = p.read_text(encoding="utf-8")
    wanted = ["android.permission.POST_NOTIFICATIONS", "android.permission.RECEIVE_BOOT_COMPLETED"]
    lines = "".join('    <uses-permission android:name="%s" />\n' % w for w in wanted if w not in s)
    if not lines:
        return
    if "</application>" in s:
        s = s.replace("</application>", "</application>\n\n" + lines.rstrip("\n"), 1)
    else:
        s = s.replace("</manifest>", lines + "</manifest>", 1)
    p.write_text(s, encoding="utf-8")


def versions():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r'App\.version\s*=\s*"([0-9.]+)"', html)
    name = m.group(1) if m else "1.0"
    code = int(os.environ.get("GITHUB_RUN_NUMBER", "1"))
    p = ANDROID / "app" / "build.gradle"
    s = p.read_text(encoding="utf-8")
    s2 = re.sub(r"versionCode\s+\d+", "versionCode %d" % code, s, count=1)
    s2 = re.sub(r'versionName\s+"[^"]*"', 'versionName "%s"' % name, s2, count=1)
    if s2 == s:
        warn("versionCode und versionName wurden nicht gefunden")
    p.write_text(s2, encoding="utf-8")
    print("Version %s, Build %d" % (name, code))
    return name


def main():
    if not MAIN.exists():
        sys.exit("Fehler: Das Android-Projekt fehlt. Erst 'npx cap add android' ausführen.")
    icons()
    notification_icon()
    splash()
    styles()
    manifest()
    name = versions()
    out = os.environ.get("GITHUB_ENV")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write("APP_VERSION=%s\n" % name)


if __name__ == "__main__":
    main()
