from fastapi import APIRouter, HTTPException
from agents.code_generator import CodeGeneratorAgent
from agents.code_reviewer import CodeReviewerAgent
from agents.document_writer import DocumentWriterAgent
from schemas import AgentTaskRequest, AgentResponse

router = APIRouter(prefix="/agent", tags=["Agent"])

code_generator = CodeGeneratorAgent()
code_reviewer = CodeReviewerAgent()
document_writer = DocumentWriterAgent()


@router.post("/code/generate", response_model=AgentResponse, summary="代码生成")
def generate_code(request: AgentTaskRequest):
    try:
        result = code_generator.execute(request.task, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/code/review", response_model=AgentResponse, summary="代码审查")
def review_code(request: AgentTaskRequest):
    try:
        result = code_reviewer.execute(request.task, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/document/write", response_model=AgentResponse, summary="文档编写")
def write_document(request: AgentTaskRequest):
    try:
        result = document_writer.execute(request.task, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
