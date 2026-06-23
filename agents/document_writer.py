from agents.base import BaseAgent
from langchain_openai import ChatOpenAI
from config.settings import settings
from typing import Dict, Any


class DocumentWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("文档编写 Agent")
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL_NAME,
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_API_BASE,
            max_tokens=settings.LLM_MAX_TOKENS,
            temperature=0.5
        )

    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        content = context.get("content", "") if context else ""
        
        prompt = f"""你是一个专业的技术文档编写专家。请根据以下内容编写高质量的技术文档：

主题：{task}

相关内容：
{content}

文档要求：
1. 结构清晰，层次分明
2. 语言专业、简洁
3. 包含必要的代码示例
4. 遵循技术文档最佳实践

请直接返回文档内容。"""

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