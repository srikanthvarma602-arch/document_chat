from pathlib import Path
from typing import Iterable,List
from src.document_chat.logger import GLOBAL_LOGGER as log
from src.document_chat.exception.custom_exception import CustomerExpection
import re,uuid,sys
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader

SUPPORT_EXTENTION={".pdf",".txt",".docx"}

def save_upload_files(uploadfiles:Iterable,targetpath:Path):
    try:
        targetpath.mkdir(exist_ok=True)
        saved:List[Path]=[]
        for uf in uploadfiles:
            name=getattr(uf,"name","file.pdf")
            exit=Path(name).suffix.lower()
            if exit not in SUPPORT_EXTENTION:
                log.warning("unsupported file",filename=name)
                continue
            safe_name=re.sub(r'[<>:"/\\|?*]', '_', re.sub(r'\s+', '_', Path(name).stem)).strip(' ._')
            filename=f"{safe_name}_{uuid.uuid4().hex[:6]}{exit}"
            out=targetpath/filename

            with open(out,"wb") as f:
                if hasattr(uf,"read"):
                    f.write(uf.read())
                else:
                    f.write(uf.getbuffer())
            saved.append(out)
            return saved 
    except Exception as e:
        log.error("failed to load file",error=str(e),dir=str(targetpath))
        raise CustomerExpection("failed to load file",sys)

def load_documents(paths=Iterable[Path]):
    """Load docs using appropriate loader based on extension """ #doc String
    docs:List[any]=[]
    try:
        for p in paths:
            ext=p.suffix.lower()
            if ext==".pdf":
                loader=PyPDFLoader(str(p))
            elif ext==".txt":
                loader=TextLoader(str(p))
            elif ext==".docx":
                loader=Docx2txtLoader(str(p))
            else:
                log.warring("unsupported extension file",path=str(p))
            docs.extend(loader.load)
        log.info("document successfully loaded",count=len(docs))
        return docs
        pass
    except Exception as e:
        log.error("failed loading the documents",str(e))
        raise CustomerExpection("Error loading documents",str(e))
        

   



if __name__=="__main__":
    save_upload_files()