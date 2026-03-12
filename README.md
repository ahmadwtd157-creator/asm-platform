
<img width="1882" height="849" alt="Screenshot_20260312_220820" src="https://github.com/user-attachments/assets/81701c76-36c8-48b1-9a04-9e314ebf834d" />
<img width="1910" height="609" alt="Screenshot_20260312_051331" src="https://github.com/user-attachments/assets/51d99def-9e59-46f3-8350-206f8122c5b8" />
<img width="1905" height="426" alt="Screenshot_20260312_052609" src="https://github.com/user-attachments/assets/3b70f511-e6fb-4464-94b6-8c6ce86e7a0e" />
<img width="1035" height="656" alt="Screenshot_20260312_161257" src="https://github.com/user-attachments/assets/446b76ff-45dd-4324-83ec-30d1a31f35d9" />
<img width="1327" height="810" alt="Screenshot_20260312_155940" src="https://github.com/user-attachments/assets/087984bf-207c-4607-b018-9b735940089b" />
<img width="1035" height="656" alt="Screenshot_20260312_161257" src="https://github.com/user-attachments/assets/f817b767-b2b4-40b1-9490-bd7abaf0fa77" />
<img width="784" height="804" alt="Screenshot_20260312_220124" src="https://github.com/user-attachments/assets/8fcbd1e2-3db7-47a9-8395-43eda1fd3358" />


Attack Surface Management Platform (ASM)
A lightweight Attack Surface Management (ASM) platform built with Flask, PostgreSQL, Docker, Subfinder, and Nmap that enables organizations to discover, monitor, and assess their exposed digital assets.
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



Installation
Requirements
    • Docker
    • Docker Compose
Run the platform
git clone https://github.com/ahmadwtd157-creator/asm-platform
cd asm-platform
docker-compose up --build
Services will start:
Frontend  → http://localhost:3000
Backend   → http://localhost:5000
Postgres  → internal container

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
1️⃣ Register user
2️⃣ Add asset
example.com
3️⃣ Discover subdomains
api.example.com
dev.example.com
mail.example.com
4️⃣ Run scan
Open ports detected
5️⃣ Platform calculates risk score
6️⃣ Generate executive report


License
This project is for educational and research purposes.

Author
ADMIRAL  
