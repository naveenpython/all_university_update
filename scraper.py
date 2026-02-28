import requests
from bs4 import BeautifulSoup
import urllib3
from sqlmodel import Session, select
from database import engine, Notice  # Humari database file se connection aur table import kar rahe hain

# SSL warning hide karne ke liye
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_and_save_notices():
    print("Scraping aur Database me save karna shuru ho raha hai...\n")
    url = "https://gurugramuniversity.ac.in/allNotifications/allNotice/index.php" 
    
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for kachra in soup(['header', 'footer', 'nav', 'aside', 'marquee']):
            kachra.decompose()
            
        all_links = soup.find_all('a')
        count = 0
        
        # Database session open karna
        with Session(engine) as session:
            for link in all_links:
                href = link.get('href')
                text = link.text.strip()
                
                if href and len(text) > 5 and not href.startswith(('#', 'javascript:')):
                    
                    if href.startswith('/'):
                        full_url = "https://gurugramuniversity.ac.in" + href
                    elif not href.startswith('http'):
                        full_url = "https://gurugramuniversity.ac.in/allNotifications/allNotice/" + href
                    else:
                        full_url = href
                    
                    # 1. Check karna ki kya yeh notice (link) pehle se MySQL me hai?
                    existing_notice = session.exec(select(Notice).where(Notice.link == full_url)).first()
                    
                    if not existing_notice:
                        # 2. Agar nahi hai, toh naya Notice object banao
                        naya_notice = Notice(
                            university_id=1,  # 1 kyu? Kyunki Gurugram Uni ki ID 1 hai (Swagger UI me dekha tha)
                            title=text,
                            link=full_url
                        )
                        session.add(naya_notice) # Database me add karne ke liye ready karo
                        print(f"✅ Naya Save Hua: {text[:40]}...")
                    else:
                        print(f"⚠️ Pehle se maujud: {text[:40]}...")
                        
                    count += 1
                    
                    if count == 15:
                        break
            
            # 3. Saara naya data ek sath MySQL me push (commit) kar do
            session.commit()
            print("\n🎉 Saare naye notices successfully MySQL me save ho gaye!")
                    
    else:
        print(f"Website load nahi hui. Status Code: {response.status_code}")

if __name__ == "__main__":
    scrape_and_save_notices()