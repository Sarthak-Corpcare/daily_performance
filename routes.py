import uuid
import tempfile
from fastapi import  APIRouter,UploadFile, File
from fastapi.responses import FileResponse
from config import SHEETS_TO_IGNORE, LOGO_FILENAME
from datetime import datetime

from service import excel_processing

router= APIRouter(tags=["Excel Processing"])

today_str = datetime.now().strftime("%d-%B-%Y")
@router.post("/process-excel")
async def process_excel(file:UploadFile=File(...)):
    temp_input=tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    temp_input.write(await file.read())
    temp_input.close()

    output_path= f"/tmp/{uuid.uuid4()}.xlsx"
    excel_processing(raw_file=temp_input.name, output_file=output_path, SHEETS_TO_IGNORE=SHEETS_TO_IGNORE,LOGO_FILENAME=LOGO_FILENAME)
    return FileResponse(path =output_path ,filename =f"Daily Performance Report {today_str}.xlsx",media_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@router.get("/")
def root():
    return {"status": "ok", "message": "Excel API is running"}
