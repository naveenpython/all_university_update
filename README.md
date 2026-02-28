Live at:https://alluniversity.org

Yeh ek automated platform hai jo alag-alag universities (Gurugram University, MDU Rohtak, DU) ki official websites se latest notices aur updates ko scrape karke ek centralized dashboard par dikhata hai. Ise real-world production environment mein AWS par host kiya gaya hai.

🛠️ Tech Stack & Infrastructure
Backend: Python 3.12 + FastAPI

Database: MySQL (Relational database)

Scraping: Selenium & BeautifulSoup4

Automation: APScheduler

Server: AWS EC2 (Ubuntu)

Web Server: Nginx (Reverse Proxy)

DNS & SSL: Cloudflare (Flexible Mode)

🚀 Key Features
Multi-University Support: Notices from multiple universities in one place.

Real-time Scraping: Background workers keep the database fresh.

Production Ready: Managed via nohup for 24/7 uptime.

📂 Project Structure
Plaintext
all_university_update/
├── main.py              # FastAPI routes aur logic
├── database.py          # Database connection settings
├── models.py            # Database tables schema
├── scrapers/            # University-wise scraping modules
├── static/              # Dashboard CSS/Images
└── templates/           # Jinja2 HTML templates
🔧 Installation & Deployment (AWS)
Environment Setup: ```bash
source myenv/bin/activate
pip install -r requirements.txt

Database: university_update_db banaya gaya aur schema sync kiya gaya.

Nginx: Domain alluniversity.org ko port 5006 par proxy kiya gaya.

Uptime: Server ko nohup ke sath background mein chalu rakha gaya hai.

👨‍💻 Developed By
Naveen Kumar

Education: Master of Computer Applications (MCA), Gurugram University (2025)

Role: Python Backend Developer

Skills: Python, FastAPI, SQL, Web Scraping, AWS Cloud, Nginx

Email: naveen.python143@gmail.com
