from collections import deque
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MemoryEntry:
    timestamp    : str
    user_input   : str
    detected_lang: str
    english_query: str
    selected_tool: str
    response     : str

class AgentMemory:
    def __init__(self, max_turns=10):
        self.history = deque(maxlen=max_turns)

    def add(self, user_input, lang, english_query, tool, response):
        self.history.append(MemoryEntry(
            timestamp     = datetime.now().isoformat(),
            user_input    = user_input,
            detected_lang = lang,
            english_query = english_query,
            selected_tool = tool,
            response      = response
        ))

    def get_context_summary(self):
        if not self.history:
            return "No previous conversation."
        return "\n".join([
            f"User asked about '{e.selected_tool}' in {e.detected_lang.upper()}"
            for e in list(self.history)[-3:]
        ])

    def clear(self):
        self.history.clear()