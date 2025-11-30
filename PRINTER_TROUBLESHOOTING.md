# Printer Discovery Troubleshooting

## Problem: Keine Drucker werden gefunden

### 1. CUPS Service prüfen
```bash
sudo systemctl status cups
sudo systemctl start cups
sudo systemctl enable cups
```

### 2. USB-Drucker prüfen
```bash
# Prüfe ob USB-Geräte erkannt werden
lsusb

# Prüfe CUPS Device-Erkennung
lpinfo -v

# Erwartetes Output für USB-Drucker:
# direct usb://HP/ENVY%206400?serial=...
```

**Typische Ausgabe:**
```
direct usb://HP/ENVY%206400?serial=ABC123
network dnssd://HP%20Envy%206400._ipp._tcp.local/
network ipp://printer.local/ipp/print
```

### 3. Berechtigungen prüfen
```bash
# User muss in der Gruppe 'lp' und 'lpadmin' sein
sudo usermod -a -G lp $USER
sudo usermod -a -G lpadmin $USER

# Logout und wieder einloggen erforderlich!
# Oder Service als root starten (nicht empfohlen für Production)
```

### 4. CUPS Web Interface prüfen
```bash
# CUPS Admin Interface aktivieren (falls deaktiviert)
sudo cupsctl --remote-admin --share-printers

# Zugriff via Browser: http://raspberry-ip:631
# Unter "Administration" > "Add Printer" sollten USB-Drucker sichtbar sein
```

### 5. USB-Drucker neu anstecken
```bash
# CUPS Log in Echtzeit anschauen
sudo tail -f /var/log/cups/error_log

# Drucker abstecken und wieder anstecken
# Im Log sollte erscheinen: "USB printer detected..."
```

### 6. CUPS Backend prüfen
```bash
# Prüfe ob USB-Backend verfügbar ist
ls -la /usr/lib/cups/backend/usb

# Sollte ausführbar sein (-rwxr-xr-x)
# Falls nicht:
sudo chmod +x /usr/lib/cups/backend/usb
```

### 7. Avahi für Netzwerk-Drucker
```bash
# Für AirPrint/Wireless-Erkennung
sudo systemctl status avahi-daemon
sudo systemctl start avahi-daemon
sudo systemctl enable avahi-daemon

# Netzwerk-Drucker suchen
avahi-browse -a -t | grep -i printer
```

### 8. API-Test durchführen
```bash
# Teste Discovery-Endpoint direkt
curl http://localhost:8000/api/v1/printers/discover

# Erwartetes Output:
# [
#   {
#     "uri": "usb://HP/ENVY%206400?serial=...",
#     "type": "USB",
#     "make": "HP",
#     "model": "ENVY 6400",
#     "name": "HP ENVY 6400",
#     "supported": true,
#     "configured": false,
#     "status": "Available"
#   }
# ]
```

### 9. Manuelle Drucker-Installation testen
```bash
# USB-Drucker manuell hinzufügen
sudo lpadmin -p Test_Printer \
  -v "usb://HP/ENVY%206400?serial=ABC123" \
  -m everywhere \
  -E

# Drucker-Liste anzeigen
lpstat -p

# Test-Seite drucken
lp -d Test_Printer /usr/share/cups/data/testprint
```

## Häufige Fehler

### "lpinfo: command not found"
```bash
sudo apt install cups
```

### "Unable to connect to CUPS server"
```bash
# CUPS läuft nicht
sudo systemctl start cups

# CUPS Port prüfen
sudo ss -tulpn | grep 631
```

### "No printers found" aber USB angeschlossen
```bash
# 1. USB-Verbindung prüfen
lsusb | grep -i printer

# 2. CUPS Logs prüfen
sudo journalctl -u cups -n 50

# 3. Drucker abstecken/anstecken und erneut testen
```

### Drucker zeigt "stopped" oder "paused"
```bash
# Drucker aktivieren
cupsenable Printer_Name

# Oder über lpadmin
sudo lpadmin -p Printer_Name -E
```

### Wireless-Drucker nicht gefunden
```bash
# 1. Avahi prüfen
sudo systemctl status avahi-daemon

# 2. Firewall prüfen (Port 631 und 5353 für mDNS)
sudo ufw allow 631
sudo ufw allow 5353/udp

# 3. Drucker im gleichen Netzwerk?
ping printer.local

# 4. IPP Discovery testen
ippfind
```

## Debug-Modus aktivieren

### CUPS Debug-Logging
```bash
# In /etc/cups/cupsd.conf
sudo nano /etc/cups/cupsd.conf

# Ändere:
LogLevel debug

# CUPS neustarten
sudo systemctl restart cups

# Logs anschauen
sudo tail -f /var/log/cups/error_log
```

### RaspScan mit Debug-Logs
```bash
# Service mit Debug-Level starten
sudo systemctl stop raspscan
cd /opt/raspscan
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
```

## Support-Informationen sammeln

Bei Problemen folgende Infos bereitstellen:

```bash
# System-Info
uname -a
lsb_release -a

# CUPS-Version
cupsd --version

# Drucker-Hardware
lsusb

# CUPS-Status
systemctl status cups
lpinfo -v
lpstat -p
lpstat -t

# Berechtigungen
groups
ls -la /usr/lib/cups/backend/

# RaspScan-Logs
sudo journalctl -u raspscan -n 100 --no-pager

# API-Test
curl http://localhost:8000/api/v1/printers/discover
curl http://localhost:8000/api/v1/printers
```

## Bekannte kompatible Drucker

### Getestete USB-Drucker:
- ✅ HP Envy 6400 (Multi-function)
- ✅ HP LaserJet (verschiedene Modelle)
- ✅ Canon Pixma (meiste Modelle)
- ✅ Brother HL-Serie
- ✅ Epson EcoTank

### Getestete Wireless-Drucker:
- ✅ HP Envy/OfficeJet (AirPrint)
- ✅ Canon Pixma (IPP)
- ✅ Brother (IPP)

### Nicht unterstützt:
- ❌ Sehr alte Drucker ohne IPP Everywhere
- ❌ Windows-only Treiber
- ❌ Proprietary Protokolle ohne Linux-Support

## Weitere Hilfe

- **CUPS Dokumentation:** https://www.cups.org/doc/index.html
- **RaspScan Issues:** https://github.com/fgrfn/RaspScan/issues
- **CUPS Forum:** https://www.cups.org/forums.php
