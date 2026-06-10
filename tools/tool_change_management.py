from tools.base_tool import BaseTool
from config.intent_config import INTENT_RESPONSES

class ChangeManagementTool(BaseTool):
    name        = "change_management"
    description = "Use when user asks about AI-native culture, change management, transformation adoption, or AI mindset."

    def run(self, query: str, language: str) -> dict:
        lang_key = "th" if language == "th" else "en"
        return self.format_output(self.name, INTENT_RESPONSES["change_management"][lang_key], language)