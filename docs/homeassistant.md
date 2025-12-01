# Home Assistant Integration

Scan2Target bietet eine vollständige Integration mit Home Assistant, um Scans über Automationen, Buttons und Skripte zu triggern.

## Quick Start

### 1. REST Command für schnellen Scan (mit Favoriten)

```yaml
# configuration.yaml
rest_command:
  scan_document:
    url: "http://YOUR_SERVER_IP/api/v1/homeassistant/scan"
    method: POST
    content_type: "application/json"
    payload: '{"scanner_id": "favorite", "target_id": "favorite", "profile": "document"}'
```

### 2. Button auf dem Dashboard

```yaml
# configuration.yaml
button:
  - platform: template
    name: "Dokument scannen"
    icon: mdi:scanner
    tap_action:
      action: call-service
      service: rest_command.scan_document
```

### 3. Automation zum Triggern des Scans

```yaml
# automations.yaml
- alias: "Scan bei Button-Druck"
  trigger:
    - platform: state
      entity_id: input_button.scan_trigger
      to: "on"
  action:
    - service: rest_command.scan_document
    - service: notify.mobile_app
      data:
        message: "Scan gestartet"
```

## Erweiterte Konfiguration

### Mehrere Scan-Profile

```yaml
# configuration.yaml
rest_command:
  # Dokument (Standard, Graustufen)
  scan_document:
    url: "http://YOUR_SERVER_IP/api/v1/homeassistant/scan"
    method: POST
    content_type: "application/json"
    payload: '{"scanner_id": "favorite", "target_id": "favorite", "profile": "document"}'
  
  # Mehrseitiger Scan (ADF)
  scan_multipage:
    url: "http://YOUR_SERVER_IP/api/v1/homeassistant/scan"
    method: POST
    content_type: "application/json"
    payload: '{"scanner_id": "favorite", "target_id": "favorite", "profile": "adf", "source": "ADF"}'
  
  # Farbe (höhere Qualität)
  scan_color:
    url: "http://YOUR_SERVER_IP/api/v1/homeassistant/scan"
    method: POST
    content_type: "application/json"
    payload: '{"scanner_id": "favorite", "target_id": "favorite", "profile": "color"}'
  
  # Foto (höchste Qualität)
  scan_photo:
    url: "http://YOUR_SERVER_IP/api/v1/homeassistant/scan"
    method: POST
    content_type: "application/json"
    payload: '{"scanner_id": "favorite", "target_id": "favorite", "profile": "photo"}'
```

### Scanner- und Target-Auswahl

```yaml
# configuration.yaml
input_select:
  scan_scanner:
    name: Scanner
    options:
      - "Favorit verwenden"
    initial: "Favorit verwenden"
  
  scan_target:
    name: Ziel
    options:
      - "Favorit verwenden"
    initial: "Favorit verwenden"
  
  scan_profile:
    name: Scan-Profil
    options:
      - "document"
      - "adf"
      - "color"
      - "photo"
    initial: "document"

rest_command:
  scan_custom:
    url: "http://YOUR_SERVER_IP/api/v1/homeassistant/scan"
    method: POST
    content_type: "application/json"
    payload: >
      {
        "scanner_id": "{{ 'favorite' if states('input_select.scan_scanner') == 'Favorit verwenden' else states('input_select.scan_scanner') }}",
        "target_id": "{{ 'favorite' if states('input_select.scan_target') == 'Favorit verwenden' else states('input_select.scan_target') }}",
        "profile": "{{ states('input_select.scan_profile') }}"
      }
```

### Status-Sensor

```yaml
# configuration.yaml
sensor:
  - platform: rest
    name: "Scan2Target Status"
    resource: "http://YOUR_SERVER_IP/api/v1/homeassistant/status"
    method: GET
    value_template: "{{ 'Online' if value_json.online else 'Offline' }}"
    json_attributes:
      - scanner_count
      - target_count
      - active_scans
      - favorite_scanner
      - favorite_target
      - last_scan
    scan_interval: 30

  - platform: template
    sensors:
      scan2target_scanner_count:
        friendly_name: "Anzahl Scanner"
        value_template: "{{ state_attr('sensor.scan2target_status', 'scanner_count') }}"
        unit_of_measurement: "Scanner"
      
      scan2target_active_scans:
        friendly_name: "Aktive Scans"
        value_template: "{{ state_attr('sensor.scan2target_status', 'active_scans') }}"
        unit_of_measurement: "Scans"
```

### Dashboard-Karte

```yaml
# Lovelace UI
type: vertical-stack
cards:
  - type: entities
    title: Scan2Target
    entities:
      - entity: sensor.scan2target_status
        name: Status
      - entity: sensor.scan2target_scanner_count
        name: Scanner verfügbar
      - entity: sensor.scan2target_active_scans
        name: Aktive Scans
      - type: attribute
        entity: sensor.scan2target_status
        attribute: favorite_scanner
        name: Favoriten-Scanner
      - type: attribute
        entity: sensor.scan2target_status
        attribute: favorite_target
        name: Favoriten-Ziel
  
  - type: entities
    title: Scan-Optionen
    entities:
      - input_select.scan_profile
  
  - type: horizontal-stack
    cards:
      - type: button
        name: Dokument
        icon: mdi:file-document-outline
        tap_action:
          action: call-service
          service: rest_command.scan_document
      
      - type: button
        name: Mehrseiten
        icon: mdi:file-document-multiple-outline
        tap_action:
          action: call-service
          service: rest_command.scan_multipage
      
      - type: button
        name: Farbe
        icon: mdi:palette
        tap_action:
          action: call-service
          service: rest_command.scan_color
      
      - type: button
        name: Foto
        icon: mdi:camera
        tap_action:
          action: call-service
          service: rest_command.scan_photo
```

## Automations-Beispiele

### 1. Täglicher automatischer Scan

```yaml
- alias: "Täglicher Dokument-Scan"
  trigger:
    - platform: time
      at: "09:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday
      state: "on"
  action:
    - service: rest_command.scan_document
    - service: notify.mobile_app
      data:
        title: "Scan gestartet"
        message: "Täglicher Dokument-Scan wurde ausgelöst"
```

### 2. Scan bei NFC-Tag

```yaml
- alias: "Scan bei NFC-Tag"
  trigger:
    - platform: tag
      tag_id: YOUR_NFC_TAG_ID
  action:
    - service: rest_command.scan_document
    - service: notify.mobile_app
      data:
        message: "Scan durch NFC-Tag gestartet"
```

### 3. Scan bei Sprachbefehl

```yaml
- alias: "Scan bei Sprachbefehl"
  trigger:
    - platform: conversation
      command:
        - "Scanne ein Dokument"
        - "Starte einen Scan"
  action:
    - service: rest_command.scan_document
    - service: tts.google_translate_say
      data:
        entity_id: media_player.wohnzimmer
        message: "Scan wird gestartet"
```

### 4. Scan mit Benachrichtigung bei Fertigstellung

```yaml
# Zunächst einen Helper für die Job-ID erstellen
input_text:
  last_scan_job_id:
    name: "Letzte Scan Job-ID"
    initial: ""

# REST Command mit Response
rest_command:
  scan_with_notification:
    url: "http://YOUR_SERVER_IP/api/v1/homeassistant/scan"
    method: POST
    content_type: "application/json"
    payload: '{"scanner_id": "favorite", "target_id": "favorite", "profile": "document"}'

# Automation
- alias: "Scan mit Benachrichtigung"
  trigger:
    - platform: state
      entity_id: input_button.scan_with_notification
  action:
    - service: rest_command.scan_with_notification
    - delay:
        seconds: 5
    - service: notify.mobile_app
      data:
        message: "Scan läuft, bitte warten..."
    - delay:
        seconds: 30  # Geschätzte Scan-Dauer
    - service: notify.mobile_app
      data:
        message: "Scan abgeschlossen!"
        data:
          url: "http://YOUR_SERVER_IP"
```

### 5. Bedingter Scan basierend auf Anwesenheit

```yaml
- alias: "Scan wenn jemand zu Hause ist"
  trigger:
    - platform: state
      entity_id: input_button.scan_trigger
  condition:
    - condition: state
      entity_id: zone.home
      state: "home"
  action:
    - service: rest_command.scan_document
  else:
    - service: notify.mobile_app
      data:
        message: "Scan nicht möglich - niemand zu Hause"
```

## API-Endpunkte

### POST /api/v1/homeassistant/scan
Startet einen Scan.

**Parameter:**
- `scanner_id` (optional): Scanner-ID oder "favorite" (Standard)
- `target_id` (optional): Target-ID oder "favorite" (Standard)
- `profile` (optional): Scan-Profil (document, adf, color, photo)
- `filename` (optional): Benutzerdefinierter Dateiname
- `source` (optional): Scan-Quelle (Flatbed, ADF)

**Response:**
```json
{
  "success": true,
  "job_id": "abc123",
  "message": "Scan started successfully",
  "scanner_name": "HP Scanner",
  "target_name": "NAS Scans",
  "estimated_duration": 15
}
```

### GET /api/v1/homeassistant/status
Liefert System-Status.

**Response:**
```json
{
  "online": true,
  "scanner_count": 2,
  "target_count": 3,
  "active_scans": 0,
  "last_scan": "2025-12-01T10:30:00",
  "favorite_scanner": "HP Scanner",
  "favorite_target": "NAS Scans"
}
```

### GET /api/v1/homeassistant/scanners
Liste aller verfügbaren Scanner.

### GET /api/v1/homeassistant/targets
Liste aller verfügbaren Ziele.

### GET /api/v1/homeassistant/profiles
Liste aller verfügbaren Scan-Profile.

## Vorbereitung in Scan2Target

1. **Favoriten-Scanner festlegen:**
   - Web UI öffnen → Scan-Bereich
   - Scanner auswählen → ⭐ Stern klicken

2. **Favoriten-Ziel festlegen:**
   - Web UI öffnen → Targets-Bereich
   - Ziel auswählen → ⭐ Stern klicken

3. **Optional: Authentifizierung deaktivieren (nur lokales Netzwerk!):**
   ```bash
   sudo nano /etc/systemd/system/scan2target.service
   # Hinzufügen:
   Environment="SCAN2TARGET_REQUIRE_AUTH=false"
   
   sudo systemctl daemon-reload
   sudo systemctl restart scan2target
   ```

## Troubleshooting

### Fehler: "No favorite scanner configured"
- In der Scan2Target Web UI einen Scanner als Favorit markieren
- Oder spezifische `scanner_id` im REST Command verwenden

### Fehler: "No favorite target configured"
- In der Scan2Target Web UI ein Ziel als Favorit markieren
- Oder spezifische `target_id` im REST Command verwenden

### REST Command antwortet nicht
- Server-IP überprüfen: `http://YOUR_SERVER_IP/health`
- Firewall-Regeln überprüfen
- Scan2Target-Logs prüfen: `sudo journalctl -u scan2target -f`

### Scan startet nicht
- Scanner in Scan2Target Web UI entdecken
- Ziel-Konnektivität testen (Test & Save Button)
- Active Jobs in Web UI überprüfen

## Sicherheitshinweise

⚠️ **Wichtig für Produktionsumgebungen:**

1. **Netzwerk-Isolation:** Scan2Target nur im lokalen Netzwerk betreiben
2. **Reverse Proxy:** Bei Internet-Zugriff HTTPS-Reverse-Proxy verwenden
3. **Authentifizierung:** JWT-Auth aktivieren für externe Zugriffe
4. **API-Token:** Für externe Aufrufe API-Token verwenden statt Favoriten

## Weitere Ressourcen

- [Scan2Target API Dokumentation](http://YOUR_SERVER_IP/docs)
- [Home Assistant REST Integration](https://www.home-assistant.io/integrations/rest/)
- [Home Assistant RESTful Command](https://www.home-assistant.io/integrations/rest_command/)
