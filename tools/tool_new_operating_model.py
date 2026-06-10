from tools.base_tool import BaseTool
from config.intent_config import INTENT_RESPONSES

class NewOperatingModelTool(BaseTool):
    name        = "new_operating_model"
    description = "Use when user asks about AI-orchestrated enterprises, moving away from siloed IT, or operating model transformation."

    def run(self, query: str, language: str) -> dict:
        lang_key = "th" if language == "th" else "en"
        return self.format_output(self.name, INTENT_RESPONSES["new_operating_model"][lang_key], language)