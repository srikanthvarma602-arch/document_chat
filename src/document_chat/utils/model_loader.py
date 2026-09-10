
from src.document_chat.utils.config_loader import load_config
from src.document_chat.logger import GLOBAL_LOGGER as log
from src.document_chat.exception.custom_exception import CustomerExpection
import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

class ModelLoader:
    def __init__(self):
        log.info("logging env")
        load_dotenv() # for loading env variables
        log.info("logging configs")
        self.config=load_config()
        
    def load_embedding(self):
        try:    
            embeddingmodel_name=self.config["embedding_model"]["model_name"]
            log.info("Loaded Embedding model",model=embeddingmodel_name)
            return HuggingFaceEmbeddings(model_name=embeddingmodel_name)
        
        except Exception as e:
            log.error("Error:Loadding Embedding model ",error=str(e))
            raise CustomerExpection("failed to embedded model",sys)

    def load_llm(self):
        try:       
            llm_block=self.config["llm"]
            provider_key=os.getenv("LLM_Provider","groq")

            if provider_key not in llm_block:
                log.error("LLM provider not found in config",provider=provider_key)
                return ValueError(f"LLM provider {provider_key} not found in config")

            llm_config=llm_block[provider_key]
            provider=llm_config.get("provider")
            model_name=llm_config.get("model_name")
            temperature=llm_config.get("temperature")
            max_output_tokens=llm_config.get("max_output_tokens")

            log.info("loading llm",provider=provider_key,model=model_name)

            if provider=="google":
                return ChatGoogleGenerativeAI(model=model_name,google_api_key=os.getenv("GOOGLE_API_Key"),temperature=temperature,max_output_tokens=max_output_tokens)
            elif provider=="groq":
                return ChatGroq(model=model_name,api_key=os.getenv("GROQ_API_Key"),max_tokens=max_output_tokens,temperature=temperature)
            else:
                return ChatOpenAI(model=model_name,api_key=os.getenv("OPENAI_API_Key"),max_tokens=max_output_tokens,temperature=temperature)

        except Exception as e:
            log.error("error loading LLm",error=str(e))
            return ValueError("error loading LLM")



 #local Testing         
if __name__=="__main__":
    loder=ModelLoader()

#test embedded
    embedding=loder.load_embedding()
    result=embedding.embed_query("hi bro")
    print(result)

#test llm
    llm=loder.load_llm()
    llmresult=llm.invoke("What is the capital city of india")
    print(llmresult)
    