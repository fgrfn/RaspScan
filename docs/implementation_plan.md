# Scan2Target Implementation Plan

**📚 Learning Project:** Created with AI/Copilot assistance as a learning exercise.

## Implementation Status

**Current Version: v1.0+** - All major milestones completed

## Completed Milestones

### ✅ Core Features (v1.0)
- FastAPI backend with JWT authentication
- SQLite database for persistence
- SANE and eSCL/AirScan scanner support
- Multiple scan profiles (150-600 DPI, color/grayscale, PDF/JPEG)
- 9 target types: SMB, SFTP, Email, Paperless-ngx, Webhooks, Google Drive, Dropbox, OneDrive, Nextcloud
- Fernet encryption for credentials (AES-128-CBC + HMAC)
- Automatic retry logic with exponential backoff
- WebSocket real-time updates
- Job history with status tracking
- Systemd service integration
- Automated installer script

### ✅ Web UI Features
- Modern Svelte + Vite frontend
- Multi-language support (English, German)
- Responsive PWA design
- Statistics dashboard with comprehensive analytics:
  - Total scans, success rate, daily averages
  - Most used scanner/target
  - Hourly scan distribution chart with timezone conversion
  - Scanner and target usage breakdowns
  - 30-day timeline view
- Live scan previews and thumbnails
- Favorites system for scanners/targets
- Manual scanner addition via IP
- Connection testing for targets
- Clear history functionality (all or individual jobs)
- Delete target statistics
- Formatted scanner names (model + IP)
- Real-time timezone conversion (UTC to local)
- Job cancellation for running/queued scans
- Home Assistant REST API integration:
  - Scan trigger endpoint with favorites support
  - Status sensor for monitoring
  - Complete documentation with examples
  - REST commands, scripts, automations
  - Dashboard card templates

### ✅ Advanced Features
- Multi-page scanning (ADF support)
- Scan preview (low-res quick scan)
- Automatic PDF compression
- Upload retry for failed deliveries
- Automatic cleanup (cron job)
- Maintenance API endpoints
- Real-time progress indicators
- Separate scan/upload status tracking

## Technology Justification
- **FastAPI (Python 3):** async-friendly, strong typing via Pydantic, lightweight for Pi hardware.
- **Svelte Frontend:** minimal bundle size, fast load on low-power devices, easy component model.
- **SQLite + YAML:** SQLite for atomic writes and queries; YAML for bootstrap and human-editable defaults. Encryption for secrets.
- **CUPS Integration:** Native on Raspberry Pi OS, provides IPP/AirPrint exposure.
- **Avahi/mDNS:** Needed for AirPrint/AirScan discovery.

## Phased Development Steps
1. **Bootstrap repo**: scaffold backend folders, create Svelte starter, add pre-commit configs, Dockerfile/compose skeleton.
2. **Config + Auth foundation**: setup SQLite models, migration tool (Alembic), auth endpoints, secure password hashing, secret key loader.
3. **Printing module**: CUPS client wrapper, printer listing, print submission, test page, queues API.
4. **Scanning module**: device discovery abstraction (SANE/eSCL), scan execution worker, file conversion, filename templates.
5. **Targets module**: local + SMB + webhook first; add email, Paperless, SFTP with connectivity checks.
6. **Jobs/history**: persistent job tracking, WebSocket notifications, retry logic service.
7. **Frontend**: dashboard widgets, scan/print flows, target management forms, history views, auth UI.
8. **Security & deployment**: IP allowlist middleware, TLS proxy guidance, systemd units, Docker Compose, Avahi/CUPS integration docs.
9. **Hardening & tests**: unit/integration tests with mock devices, linting, observability hooks, backup/restore scripts.
