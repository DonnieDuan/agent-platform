from agents.base import BaseAgent
from langchain_openai import ChatOpenAI
from config.settings import settings
from typing import Dict, Any


class CodeGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("代码生成 Agent")
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL_NAME,
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_API_BASE,
            max_tokens=settings.LLM_MAX_TOKENS,
            temperature=settings.LLM_TEMPERATURE
        )

    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        prompt = f"""你是一个专业的代码生成助手。请根据以下需求生成高质量的代码：

需求：{task}

要求：
1. 代码必须完整、可运行
2. 包含必要的注释
3. 遵循最佳实践
4. 如果需要，提供测试用例

请直接返回代码，不要包含其他解释。"""

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