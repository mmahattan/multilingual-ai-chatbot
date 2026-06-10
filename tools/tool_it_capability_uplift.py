from tools.base_tool import BaseTool
from config.intent_config import INTENT_RESPONSES

class ITCapabilityUpliftTool(BaseTool):
    name        = "it_capability_uplift"
    description = "Use when user asks about upgrading IT pipelines, intelligent agent platforms, or technology infrastructure uplift."

    def run(self, query: str, language: str) -> dict:
        lang_key = "th" if language == "th" else "en"
        return self.format_output(self.name, INTENT_RESPONSES["it_capability_uplift"][lang_key], language)