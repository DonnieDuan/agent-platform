from agents.base import BaseAgent
from langchain_openai import ChatOpenAI
from config.settings import settings
from typing import Dict, Any


class CodeReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__("代码审查 Agent")
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL_NAME,
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_API_BASE,
            max_tokens=settings.LLM_MAX_TOKENS,
            temperature=0.3
        )

    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        code = context.get("code", "") if context else ""
        
        prompt = f"""你是一个专业的代码审查专家。请对以下代码进行全面审查：

代码：
{code}

审查要求：
1. 检查代码质量和规范
2. 识别潜在的 bug 和安全隐患
3. 提供优化建议
4. 评估代码复杂度和可维护性

请以结构化的方式返回审查结果。"""

        try:
            response = self.llm.invoke(prompt)
            return {
                "agent": self.name,
                "task": task,
                "result": response.content,
                "status": "completed"
            }
        except Exception as e:
            return {
                "agent": self.name,
                "task": task,
                "result": str(e),
                "status": "failed"
            }