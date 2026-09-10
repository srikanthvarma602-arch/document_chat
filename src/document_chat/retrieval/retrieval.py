from operator import itemgetter
import sys

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from src.document_chat.utils.model_loader import ModelLoader
from src.document_chat.logger import GLOBAL_LOGGER as log
from src.document_chat.exception.custom_exception import CustomerExpection
from src.document_chat.utils.config_loader import load_config
from src.document_chat.prompts.prompts import PROMT_REGISTRY

class ConversionalRAG:
    def __init__(self):
        try:
             #build retrieval
            log.info("retrievar initialization start")
            self.config=load_config()
            self.embed_model=ModelLoader().load_embedding()
            self.llm=self._llm_load()
            self.retrievar=self._load_qdrant_retrieval()
            
            #build prompt
            self.chain=None
            if self.retrievar is not None:
                self.chain=self._build_icel_chain()

            log.info("retrievar initialization end")
        except Exception as e:
            log.error("retrievar initialization failed",error=str(e))
            raise CustomerExpection("retrievar initialization failed",str(e))  

       

    def _load_qdrant_retrieval(self):
        try:
            log.info("_load_qdrant_retrieval Start")
            vectorStore=QdrantVectorStore.from_existing_collection(
                        embedding=self.embed_model,
                        path="qdrant",
                        collection_name="document_chat"
                    )
            topk=self.config["retriever"]["top_k"]
            retrievar=vectorStore.as_retriever(search_args={"k":topk})
            log.info("_load_qdrant_retrieval sucessfully")
            return retrievar
        except Exception as e:
            log.error("qdrant_retrieval initialization failed",error=str(e))
            raise CustomerExpection("qdrant_retrieval initialization failed",str(e))  

        

    def _llm_load(self):
        try:
            llm=ModelLoader.load_llm()
            if not llm:
                raise ValueError("LLM could not be found")
            log.info("llm load successfully")
            return llm
        except Exception as e:
            log.error("error in load llm",error=str(e))
            raise CustomerExpection("Error llm loader conversionRAG",sys)

    def _build_icel_chain(self):
        try:
            # 1. rewrite user question with chatHistory context
            chat_history=None
            context_question_prompt:ChatPromptTemplate=PROMT_REGISTRY["contextualize_question"]
            question_rewrite=(
                {"input": itemgetter("input"),"chat_history":itemgetter("chat_history")}
                | context_question_prompt
                | self.llm
                | StrOutputParser()
            )
            # 2. Answer using retrieved context + question rewriter
            retrievaldoc= question_rewrite | self.retrievar | self._format_docs
            context_qa_prompt:ChatPromptTemplate=PROMT_REGISTRY["context_qa"]
            self.chain=(
                {"context":retrievaldoc,"input":itemgetter("input")}
                | context_qa_prompt
                | self.llm
                | StrOutputParser()
            )
            log.info("LCEL graph build scuessfully")

        except Exception as e:
            log.error("failed to build LCEL chain in ConversionRAG", error=str(e))
            raise CustomerExpection("failed to build LCEL chain in ConversionRAG")

    def _format_docs(self,docs):
        context=" ".join([doc.page_content  for doc in docs])
        return context

    def invoke(self,user_input,chat_history):
         try:
             if self.chain is None:
                 raise ValueError("RAg chain initialized")
             chat_history=chat_history or []
             pay_load={"input":user_input,"chat_history":chat_history}
             answer=self.chain.invoke(pay_load)
             if not answer:
                 log.waring("No answer generated",user_input=user_input)
                 return "No answer generated"
             log.info("chain invoked generated answer successfully", user_input=user_input,answer=str(answer[:100]))
             return answer
         except Exception as e:
             log.error("failed to invoke conversion rag", error=str(e))
             raise CustomerExpection("failed to invoke conversion rag",str(e))
