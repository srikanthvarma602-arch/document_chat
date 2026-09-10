import os
from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from document_chat.retrieval.retrieval import ConversionalRAG
from document_chat.ingestion.document_ingestion import DocumentIngestion
from src.document_chat.utils.file_ops import FastApiFileAdapter
from dotenv import load_dotenv
from src.document_chat.logger import GLOBAL_LOGGER as log

load_dotenv()

app=FastAPI()

uploadFilePath=os.getenv("Upload_File_Path")

@app.get("/")
def getInfo():
    return "fast api run"

@app.post("/chat/index")
async def chat_index(files:List[UploadFile]=File(...),
               chunk_size=Form(1000),
               chunk_overlap=Form(2000)):
    try:
        log.info("document ingestion started...")
        warpped=[FastApiFileAdapter(file) for file in files]
        docIngestion=DocumentIngestion()
        docIngestion.insertvectordb(warpped,uploadFilePath,int(chunk_size),int(chunk_overlap))
        log.info("Doucment ingestion completed")
        return {"Response":"Document ingestion completed successfully"}
        
    except Exception as e:
        log.error("document ingestion failed",error=str(e))
        raise HTTPException(status_code=500, detail=f"indexing failed:{e}",)

@app.post("/chat/query")
async def chatquery(question=Form(...)):
    try:
        log.info("calling invoke mrthod")
        cr=ConversionalRAG()
        # fetching history from database
        chat_history=""
        answer=cr.invoke(question,"")
        # insert chat history into database
        log.info("invoke method completed sucssfully")
        return {"answer":answer}
    except Exception as e:
        log.error("Failed invoke method",str(e))
        raise HTTPException(status_code=500,detail=f"invoke failed:{e}")
    