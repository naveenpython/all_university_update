from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from sqlmodel import Session, select
from database import engine, Notice
import time
import urllib3

urllib3.disable_warnings()

def scrape_du_notices():
    print("🚀 DU 'Whitelist Keyword' Scraping start ho raha hai...")
    
    options = webdriver.ChromeOptions()
    # 🔥 NAYI MAGIC LINE: Browser ko background me chupane ke liye
    options.add_argument("--headless=new") 
    
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        url = "https://www.du.ac.in/"
        driver.get(url)
        driver.maximize_window()
        
        print("⏳ Page load ho raha hai, Spotlight box render hone ka wait kar rahe hain...")
        time.sleep(6)
        
        # Thoda scroll karenge Spotlight box tak
        for i in range(4):
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(1)
            
        print("🔍 Sirf ASLI Notices dhoondh rahe hain (Keywords ke zariye)...")
        links = driver.find_elements(By.XPATH, "//a[@href]")
        
        count = 0
        kuch_mila = False
        
        # 🔴 NAYA JADU: Sirf in words wale titles ko hi notice mana jayega!
        valid_keywords = ['notice', 'notification', 'convocation', 'press release', 'advt', 'result', 'date', 'extension', 'exam', 'admissions', 'deadline', 'circular', 'guidelines', 'syllabus']
        
        with Session(engine) as session:
            for link in links:
                try:
                    title = link.get_attribute("textContent")
                    href = link.get_attribute("href")
                    
                    if title and href:
                        clean_title = " ".join(title.strip().split())
                        clean_title_lower = clean_title.lower()
                        
                        # Check karo ki kya title me humara koi "Valid Keyword" hai?
                        if any(keyword in clean_title_lower for keyword in valid_keywords):
                            
                            # Subdomains aur Menu ko aur strictly roko
                            if "page=" in href or href == "https://www.du.ac.in/" or "index.php?page=" in href:
                                continue
                                
                            # Faltu navigation buttons roko
                            ignore_words = ['home', 'about', 'contact', 'login', 'read more', 'click here', 'skip to', 'view all']
                            if not any(word in clean_title_lower for word in ignore_words):
                                
                                # Duplicate Check
                                existing = session.exec(select(Notice).where(Notice.link == href)).first()
                                
                                if not existing:
                                    session.add(Notice(university_id=3, title=clean_title, link=href))
                                    print(f"✅ ASLI DU Naya Save: {clean_title[:70]}...")
                                    kuch_mila = True
                                    
                                count += 1
                                if count >= 20: # Top 20 asli notices
                                    break
                except Exception as e:
                    continue 
            
            session.commit()
            if kuch_mila:
                print("🎉 DU ke Spotlight notices finally database me save ho gaye!\n")
            else:
                print("⚠️ Script chali par keyword match nahi hua (Ya toh pehle se save hain).")
                
    except Exception as e:
        print(f"❌ DU Scraping Error: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_du_notices()