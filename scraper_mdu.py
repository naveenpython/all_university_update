import requests
from bs4 import BeautifulSoup
import urllib3
from sqlmodel import Session, select
from database import engine, Notice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_mdu_notices():
    print("🚀 MDU Rohtak Scraping start ho rahi hai (Parent Hack)...")
    url = "https://mdu.ac.in/default.aspx" 
    
    try:
        response = requests.get(url, verify=False, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            count = 0
            
            with Session(engine) as session:
                # Page ke saare links uthao
                for link in soup.find_all('a'):
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    # NAYA HACK: Link ke parent (jaise <li> ya <div>) ka poora text nikal lo
                    parent_text = link.parent.get_text() if link.parent else ""
                    grandparent_text = link.parent.parent.get_text() if link.parent and link.parent.parent else ""
                    
                    # Agar link me title hai, aur uske aas-paas "Dated:" likha hai, tabhi use uthao!
                    if len(title) > 8 and href and ("Dated:" in parent_text or "Dated:" in grandparent_text):
                        
                        # Faltu links ko ignore karo
                        if "javascript:" in href or "mailto:" in href:
                            continue
                            
                        # MDU URLs ko pura banana
                        if href.startswith('/'): 
                            full_url = "https://mdu.ac.in" + href
                        elif not href.startswith('http'): 
                            full_url = "https://mdu.ac.in/" + href
                        else: 
                            full_url = href
                            
                        existing = session.exec(select(Notice).where(Notice.link == full_url)).first()
                        
                        if not existing:
                            session.add(Notice(university_id=2, title=title, link=full_url))
                            print(f"✅ MDU Naya Save: {title[:50]}...")
                        else:
                            print(f"⚠️ Pehle se maujud: {title[:30]}...")
                            
                        count += 1
                        if count >= 20: # Top 20 notices
                            break
                
                session.commit()
                print("🎉 MDU ke notices successfully database me save ho gaye!\n")
        else:
            print(f"❌ MDU Website load nahi hui. Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error aayi: {e}")

if __name__ == "__main__":
    scrape_mdu_notices()