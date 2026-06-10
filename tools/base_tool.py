from abc import ABC, abstractmethod

class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, query: str, language: str) -> dict:
        pass

    def format_output(self, intent, response, language):
        return {
            "intent"  : intent,
            "response": response,
            "language": language,
            "tool"    : self.name
        }