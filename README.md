# 🎓 AllUniversity.org - Academic Alert System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![AWS EC2](https://img.shields.io/badge/Deployed_on-AWS_EC2-FF9900.svg)
![Nginx](https://img.shields.io/badge/Proxy-Nginx-009639.svg)

## 📌 Project Overview
**AllUniversity.org** is a centralized, automated academic alert platform designed to scrape and serve daily notices from various university portals (including Gurugram University and MDU) into a single, accessible dashboard. It eliminates the need for students to manually check multiple slow-loading university websites.

## 🚀 Key Features
- **Automated Data Pipelines:** Built with Python and Selenium to routinely extract real-time notices, exam dates, and updates.
- **High-Performance APIs:** Utilizes FastAPI to serve extracted data swiftly to the front-end.
- **Relational Database:** Efficient data storage and retrieval using MySQL.
- **Production-Grade Deployment:** Hosted on an AWS EC2 instance.
- **Server Optimization:** Configured Nginx as a reverse proxy and implemented 1GB Swap memory allocation to ensure zero downtime and resolve 502 Bad Gateway server crashes during heavy scraping loads.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Web Scraping (Selenium)
- **Database:** MySQL
- **Infrastructure & DevOps:** AWS EC2, Nginx, Linux Server Administration

## ⚙️ Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/naveenpython/all-university-scraper.git](https://github.com/naveenpython/all-university-scraper.git)
   cd all-university-scraper

   Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

Bash
pip install -r requirements.txt
Run the FastAPI server:

Bash
uvicorn main:app --reload
🌐 Live Demo
Check out the live project here: https://alluniversity.org

👨‍💻 About the Developer
Developed by Naveen Kumar MCA Graduate (2025) | Python Backend Developer

LinkedIn Profile | Email: naveen.python143@gmail.com

***

### 💡 How to use this?
Open your AllUniversity project/repository on GitHub.

Click on "Add a README" or "Create new file" and name the file README.md.

Copy the code provided above, paste it in the file, and save (commit) it.
(Note: Make sure to replace the git clone link in the code with the actual link to your repository).
