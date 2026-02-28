from fastapi import FastAPI,Depends,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from sqlmodel import Session
from sqlmodel import select
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables,get_session,University,Notice
from apscheduler.schedulers.background import BackgroundScheduler
# Humari scraping file gurugram uviversity
from scraper import scrape_and_save_notices
#it is mdu university
from scraper_mdu import scrape_mdu_notices  
#DU
from scraper_du import scrape_du_notices 


# Scheduler ka object banaya
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Tables ready hain!")
    
    print("Background Automation (Scheduler) start ho raha hai...")
    
    # 1. Gurugram University ko har 2 minute mein check karo
    scheduler.add_job(scrape_and_save_notices, 'interval', minutes=600)
    
    # 2. MDU ko har 3 minute mein check karo (Alag time hone se server fast rahega)
    scheduler.add_job(scrape_mdu_notices, 'interval', minutes=600) 
    # 3.MDU ko har 3 minute mein check karo
    scheduler.add_job(scrape_du_notices, 'interval', minutes=600)
    
    scheduler.start()
    yield
    print("Scheduler band ho raha hai...")
    scheduler.shutdown()

#initialize fast api app

app=FastAPI(title="All University Updates API !",lifespan=lifespan)
# Yeh line browser ko permission degi API read karne ki
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Abhi ke liye sabko allow kar rahe hain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Yeh line aapke 'static' folder (CSS/JS) ko backend se jod degi
app.mount("/static", StaticFiles(directory="static"), name="static")

# Yeh line HTML templates ke folder ko set karegi
templates = Jinja2Templates(directory="templates")

# NAYA ROUTE: Jab koi seedha website kholega (jaise google.com), toh kya dikhega?
@app.get("/")
def serve_homepage(request:Request):
    # Yeh aapki index.html file ko browser par bhej dega
    return templates.TemplateResponse("index.html", {"request": request})
#----create root api--
@app.get('/')
def read_root():
    return{"message":"Welcome to the All University Updates API !"}

#-- add the new university updates
@app.post("/universites")
def add_university(university:University,session:Session=Depends(get_session)):
    session.add(university)
    session.commit()
    session.refresh(university)
    return{"message":"Add the University successfully","data":university}
#see the all university route
@app.get("/universities/")
def get_universities(session:Session=Depends(get_session)):
    #fetch the all universities data
    universities=session.exec(select(University)).all()
    return{"data":universities}
# 4. Saare Notices fetch karne ka naya Route
@app.get("/notices/")
def get_notices(session: Session = Depends(get_session)):
    # Database se notices nikalna (Naye wale sabse upar dikhane ke liye order_by ka use kiya hai)
    from sqlmodel import desc # Agar upar import nahi kiya toh yahan bhi kar sakte ho
    
    statement = select(Notice).order_by(desc(Notice.date_published)).limit(50)
    notices = session.exec(statement).all()
    
    return {
        "message": "Notices successfully fetch ho gaye",
        "total_notices": len(notices),
        "data": notices
    }
