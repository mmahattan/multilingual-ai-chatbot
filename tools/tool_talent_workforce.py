from tools.base_tool import BaseTool
from config.intent_config import INTENT_RESPONSES

class TalentWorkforceTool(BaseTool):
    name        = "talent_workforce"
    description = "Use when user asks about reskilling developers, workforce transformation, or turning builders into AI orchestrators."

    def run(self, query: str, language: str) -> dict:
        lang_key = "th" if language == "th" else "en"
        return self.format_output(self.name, INTENT_RESPONSES["talent_workforce"][lang_key], language)