import boto3
import json
import os
import tempfile
from app.utils.logs import Logger
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, Docx2txtLoader
from langchain_core.output_parsers import PydanticOutputParser
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from app.llm.tools.resume_pydantic_model import ToolSpecWrapper
from app.llm.postprocessing.resume_parser_pp import ToolSpecWrapperPostProcessing
from app.configs.appconf import Environmentals

env = Environmentals()
log = Logger()

class ResumeParser:
    def __init__(self, resume_path: str):
        self.resume_path = resume_path
        self.parser = PydanticOutputParser(pydantic_object=ToolSpecWrapper)
        self.embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.prompt = self.create_prompt()
        self.retriever = self.create_retriever()
        self.llm = ChatBedrock(
            client=boto3.client("bedrock-runtime", region_name="us-east-1"),
            model_id=env.MODEL_HAIKU,
            model_kwargs={"temperature": 0.2, "max_tokens": 3000}
        )
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)

    def create_prompt(self):
        prompt = ChatPromptTemplate.from_template("""
                                    Please extract resume details from the provided context and return ONLY a JSON object.
                                    Do not include any other text, explanations, or formatting outside the JSON object.
                                    
                                    <context>
                                    {context}
                                    </context>
                                    
                                    {format_instructions}
                                    
                                    Return ONLY the JSON object and nothing else.
                                """).partial(format_instructions=self.parser.get_format_instructions())
        return prompt
    
    def create_retriever(self):
        file_extension = self.resume_path.lower().rsplit('.', 1)[-1]  # Extract file extension

        loader_mapping = {
            "pdf": PyPDFLoader,
            "doc": UnstructuredWordDocumentLoader,
            "docx": Docx2txtLoader,
        }

        loader_class = loader_mapping.get(file_extension)

        if loader_class:
            loader = loader_class(self.resume_path)
            resume_texts = loader.load()
        else:
            log.logger.error(f"Unsupported file extension: {self.resume_path}")
            return None

        chunks = self.splitter.split_documents(resume_texts)
        chunk_texts = [chunk.page_content for chunk in chunks]
        db = Chroma.from_texts(chunk_texts, self.embedding_function, persist_directory=tempfile.TemporaryDirectory().name)
        store_size = len(chunk_texts)
        return db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": round(0.85 * store_size),
                "lambda_mult": 0.5
            }
        )

    def run(self):
        retrieval_chain = create_retrieval_chain(self.retriever, self.document_chain)
        result = retrieval_chain.invoke({
            "input": "Extract all possible resume details comprehensively",
            "context": "Provide maximum detail from the resume"
        })
        tool_spec_wrapper = ToolSpecWrapperPostProcessing.model_validate(json.loads(result["answer"]))
        input_schema = tool_spec_wrapper.toolSpec.inputSchema.model_dump()
        return input_schema