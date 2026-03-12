Attack Surface Management Platform (ASM)
A lightweight Attack Surface Management (ASM) platform built with Flask, PostgreSQL, Docker, and Nmap that enables organizations to discover, monitor, and assess their exposed digital assets.
The platform automatically discovers subdomains, scans exposed ports, classifies services, calculates risk scores, and generates executive security reports.

Features
Passive Subdomain Discovery
Automatically discover subdomains using Subfinder.
Active Port Scanning
Perform active scanning using Nmap to identify exposed services.
Asset Classification
Automatically classify assets based on:
    • Open ports
    • Banner information
    • Known service signatures
Risk Scoring
Calculate a risk score (0–100) for each asset based on exposed services.
Example:
Port	Risk
3306	High
5432	High
22	Medium
80	Low
443	Low
Continuous Monitoring
A scheduler automatically rescans assets to detect:
    • New open ports
    • Closed ports
    • Exposure changes
Executive PDF Reporting
Generate executive-level reports containing:
    • Total assets
    • Risk distribution
    • Exposure changes

Architecture
                +------------------+
                |   Frontend UI    |
                |  (AdminLTE)      |
                +--------+---------+
                         |
                         |
                    REST API
                         |
+------------------------+------------------------+
|                        Backend                  |
|                    Flask API                    |
|                                                 |
|  Subdomain Discovery   Port Scanning            |
|  (Subfinder)           (Nmap)                   |
|                                                 |
|  Risk Scoring          Asset Classification     |
|                                                 |
+------------------------+------------------------+
                         |
                         |
                    PostgreSQL

Tech Stack
Backend
    • Python
    • Flask
    • PostgreSQL
    • APScheduler
    • Nmap
    • Subfinder
Frontend
    • AdminLTE
    • Bootstrap
    • Vanilla JavaScript
Infrastructure
    • Docker
    • Docker Compose

Project Structure
asm-platform
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── engines
│   │   ├── models
│   │   └── services
│   │
│   ├── routes
│   │   ├── asset_routes.py
│   │   └── dashboard_routes.py
│   │
│   ├── main.py
│   └── Dockerfile
│
├── frontend
│   ├── assets
│   ├── js
│   ├── dashboard.html
│   ├── assets.html
│   ├── asset_details.html
│   └── Dockerfile
│
├── db
│   └── init.sql
│
├── docker-compose.yml
└── README.md

Installation
Requirements
    • Docker
    • Docker Compose
Run the platform
docker-compose up --build
Services will start:
Frontend  → http://localhost:3000
Backend   → http://localhost:5000
Postgres  → internal container

http://localhost:3000/dashboard.html
http://localhost:3000/assets.html

API Endpoints
Authentication
POST /api/register
POST /api/login
GET  /api/profile
Assets
POST   /api/assets
GET    /api/assets
DELETE /api/assets/{id}
Scanning
POST /api/assets/{id}/scan
GET  /api/assets/{id}/results
Discovery
POST /api/discover/{asset_id}
Reports
GET /api/report/executive

Security Features
    • JWT Authentication
    • Rate Limiting
    • Input validation
    • Dockerized services
    • Separation of frontend/backend
    • Role based access control

Example Workflow
1- Register user
2- Add asset
example.com
3- Discover subdomains
api.example.com
dev.example.com
mail.example.com
4- Run scan
Open ports detected
5- Platform calculates risk score
6- Generate executive report

Future Improvements
    • CVE vulnerability detection
    • TLS certificate monitoring
    • ASN / cloud asset discovery
    • Attack surface visualization
    • Email alerting
    • Risk trend analytics

License
This project is for educational and research purposes.

Author
ADMIRAL
