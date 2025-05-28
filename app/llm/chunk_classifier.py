import boto3
from app.configs.appconf import env
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import PydanticOutputParser
from app.llm.tools.classifier_tool import ClassifierInputSchema
from app.utils.logs import log
from app.endpoints.errors import APIException

class ChunkClassifier:
    def __init__(self, chunk_list: list[str]):
        self.serialized_chunks = chunk_list
        self.llm = self._create_llm(env.MODEL_SONNET)
        self.parser = PydanticOutputParser(pydantic_object=ClassifierInputSchema)

    def _create_llm(self, MODEL_ID: str):
        return ChatBedrock(
            client=boto3.client("bedrock-runtime", region_name="us-east-1"),
            model_id=MODEL_ID,
            model_kwargs={"temperature": 0.2, "max_tokens": 3000}
        )
    
    def _build_prompt(self) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert in parsing resume text into structured data.

            You are given:
            1. Multiple JSON schemas — each defines fields for a specific category (e.g., jobs, education, personal info).
            2. A list of text chunks from a resume, labeled by Chunk ID (0, 1, 2, ...).

            Your task:
            For each schema, identify the **chunk numbers** (Chunk IDs) that contain **any relevant information** about the schema’s fields.

            ### Output format
            Return ONLY this JSON object with chunk numbers as integers:
            {format_instructions}

            DO NOT return explanations or unrelated text.

            <context>
            {context}
            </context>

            ### Important instructions:
            - Be inclusive: include a chunk if **any part of it** (not just majority) relates to any field in a schema.
            - Some fields may be scattered — consider even short mentions or partial matches.
            - If a chunk overlaps across multiple schemas (e.g., job and project), assign it to all relevant schemas.
            - You are allowed to select the same chunk ID for multiple schemas.
            - Do not infer — only rely on explicitly stated or clearly implied text.
            - If a chunk has no relevance, skip it.

            Your goal is to ensure **no chunk with useful data is missed**, while avoiding false positives.
            """
        ).partial(format_instructions=self.parser.get_format_instructions())
        return prompt

    def classify(self) -> dict:
        try:
            prompt = self._build_prompt()
            formatted_prompt = prompt.format(context=self.serialized_chunks)
            response = self.llm.invoke(formatted_prompt)
            parsed_output = self.parser.parse(response.content)
            print(f"Results: {parsed_output.model_dump()}")
            return parsed_output.model_dump()
        except Exception as e:
            log.error(f"Error while classifying chunks: {str(e)}")
            raise APIException(500)