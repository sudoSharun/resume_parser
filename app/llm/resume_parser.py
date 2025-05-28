import boto3
import json
import asyncio
import tempfile
from app.utils.logs import Logger
from langchain_core.output_parsers import PydanticOutputParser
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.text_splitter import SemanticChunker
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from app.llm.postprocessing.pp import ResumeDetails
from langchain.chains.combine_documents import create_stuff_documents_chain
from app.llm.tools.resume_parser_tool import EducationInputSchema, ProjectInputSchema, JobInputSchema, ProfessionalInputSchema, PersonalInputSchema
from app.configs.appconf import env
from app.services.text_loader import ExtractText
from app.endpoints.errors import APIException
from app.llm.chunk_classifier import ChunkClassifier
from langchain_core.documents import Document

log = Logger()

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

class ResumeParser:
    def __init__(self, resume_path: str):
        self.resume_path = resume_path
        self.haikullm = self._create_llm(env.MODEL_HAIKU)
        self.sonnetllm = self._create_llm(env.MODEL_SONNET)
        # self.deepseekllm = self._create_llm(env.MODEL_DEEPSEEK)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        self.serialized_chunks = self._create_serialized_chunks()

    def _create_llm(self, MODEL_ID: str):
        return ChatBedrock(
            client=boto3.client("bedrock-runtime", region_name="us-east-1"),
            model_id=MODEL_ID,
            model_kwargs={"temperature": 0.2, "max_tokens": 3000}
        )

    def _clean_chunks(self, chunk_list: list[str]) -> list[str]:
        """
        Cleans the input chunk list by removing newlines, tabs, extra spaces, and stripping whitespace.
        """
        cleaned_chunks = []
        for chunk in chunk_list:
            if chunk.strip():
                cleaned_chunk = chunk.replace("\n", " ").replace("\t", "")
                cleaned_chunk = ' '.join(cleaned_chunk.split())
                cleaned_chunks.append(cleaned_chunk)
        return cleaned_chunks
    
    def _create_serialized_chunks(self):
        try:
            resume_text = ExtractText(self.resume_path).text_content
            chunks = self.splitter.split_text(resume_text)
            chunks = self._clean_chunks(chunks)
            serialized_chunks = {i: chunk for i, chunk in enumerate(chunks)}
            return serialized_chunks
        except Exception as e:
            log.error(f"Error while creating serialized chunks: {str(e)}")
            raise APIException(500)
        
    def _create_prompt(self, parser: PydanticOutputParser):
        prompt = ChatPromptTemplate.from_template("""
                                    Please extract resume details from the provided context and return ONLY a JSON object.
                                    Do not include any other text, explanations, or formatting outside the JSON object.

                                    <context>
                                    {context}
                                    </context>

                                    {format_instructions}

                                    Return ONLY the JSON object and nothing else.
                                """).partial(format_instructions=parser.get_format_instructions())
        return prompt

    def _postprocess_results(self, results):
        combined_results = {}
        for result in results:
            combined_results.update(result)
        try:
            combined_results = ResumeDetails(**combined_results).model_dump()
            return combined_results
        except Exception as e:
            log.error(f"Error while postprocessing results: {str(e)}")
            raise APIException(500)
    
    async def parse_details(self, tool_spec: PydanticOutputParser, chunk_indexes, llm):
        raw_response = None
        try:
            documents = [
                Document(page_content=self.serialized_chunks[idx]) for idx in chunk_indexes
            ]
            prompt = self._create_prompt(tool_spec)
            stuff_chain = create_stuff_documents_chain(llm, prompt, document_variable_name="context")
            result = await stuff_chain.ainvoke({"context": documents})
            raw_response = result
            result = json.loads(result)
            return result
        except Exception as e:
            log.error(f"Error while parsing details: {str(e)}")
            log.error(f"Raw response: {raw_response}")
            raise APIException(500)

    async def run(self):
        professional_parser = PydanticOutputParser(pydantic_object=ProfessionalInputSchema)
        personal_parser = PydanticOutputParser(pydantic_object=PersonalInputSchema)
        education_parser = PydanticOutputParser(pydantic_object=EducationInputSchema)
        project_parser = PydanticOutputParser(pydantic_object=ProjectInputSchema)
        job_parser = PydanticOutputParser(pydantic_object=JobInputSchema)
        
        classified_chunks = ChunkClassifier(self.serialized_chunks).classify()

        results = await asyncio.gather(
            self.parse_details(project_parser, classified_chunks["ProjectDetails"], self.sonnetllm),
            self.parse_details(job_parser, classified_chunks["JobDetails"], self.sonnetllm),
            self.parse_details(personal_parser, classified_chunks["PersonalInfo"], self.haikullm),
            self.parse_details(education_parser, classified_chunks["EducationDetails"], self.haikullm),
            self.parse_details(professional_parser, classified_chunks["ProfessionalInfo"], self.sonnetllm),
        )
        
        combined_results = self._postprocess_results(results)
        return combined_results