from tools.base_tool import BaseTool
from config.intent_config import INTENT_RESPONSES

class NewWaysOfWorkingTool(BaseTool):
    name        = "new_ways_of_working"
    description = "Use when user asks about human-agent collaboration, shifting from linear delivery, or new team working models."

    def run(self, query: str, language: str) -> dict:
        lang_key = "th" if language == "th" else "en"
        return self.format_output(self.name, INTENT_RESPONSES["new_ways_of_working"][lang_key], language)