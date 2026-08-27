from src.document_chat.utils.file_ops import load_documents,save_upload_files
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.document_chat.logger import GLOBAL_LOGGER as log
from src.document_chat.utils.model_loader import ModelLoader
from langchain_qdrant import QdrantVectorStore
from src.document_chat.exception.custom_exception import CustomerExpection
class DocumentIngestion:
    def __init__(self):        
        self.model_loader=ModelLoader()

    def _splitchunks(self,docs,chunksize=1000,chunkoverlap=200):
        try:
            splitter=RecursiveCharacterTextSplitter(chunksize=chunksize,chunk_overlap=chunkoverlap)
            chunks=splitter.split_documents(docs)
            log.info("documents splitted completed")
            return chunks
        except Exception as e:
            log.error("Failed chunks")
            raise CustomerExpection("Error failed chunks",str(e))    

    def _strorevectordb(self,chunks)->QdrantVectorStore:
        try:
            embedd_model=self.model_loader.load_embedding()
            vectorstrore=QdrantVectorStore.add_documents(
            document=chunks,
                    embedding=embedd_model,
                    path="qdrant",
                    collection_name="document_chat"
                )
            log.info("vectorstrore succssfully")
            return vectorstrore
        except Exception as e:
            log.error("Failed Qdrant vector stroe")
            raise CustomerExpection("Error failed Qdrant vector",str(e))    
      
    def insertvectordb(self,uploadfiles,path,chunksize,chunkoverlap):
        try:
            #load documents
            paths=save_upload_files(uploadfiles,path)
            docs=load_documents(paths)
            # split chunks
            chunks=self._splitchunks(docs,chunksize,chunkoverlap)       
            # convert embedding  and store vector db
            self._strorevectordb(chunks)
            # return vectorstroe.as_retriever(search_args={"k":5})
            # return retriver
        except Exception as e:
            log.error("Failed retriever")
            raise CustomerExpection("Error creating retriever",str(e))     
       

        pass



    