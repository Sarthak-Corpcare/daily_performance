from fastapi import FastAPI
from routes import router as excel_router
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI(title="Excel Processor", version="1.0")
app.include_router(excel_router)

today_str = datetime.now().strftime("%d-%B-%Y")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)




