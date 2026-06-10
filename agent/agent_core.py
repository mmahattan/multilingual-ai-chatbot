from agent.agent_memory  import AgentMemory
from agent.agent_planner import AgentPlanner
from config.watsonx_config import get_watsonx_model
from tools.tool_new_operating_model  import NewOperatingModelTool
from tools.tool_new_ways_of_working  import NewWaysOfWorkingTool
from tools.tool_it_capability_uplift import ITCapabilityUpliftTool
from tools.tool_talent_workforce     import TalentWorkforceTool
from tools.tool_change_management    import ChangeManagementTool

class KTBClientZeroAgent:
    def __init__(self):
        self.llm   = get_watsonx_model()
        self.tools = [
            NewOperatingModelTool(),
            NewWaysOfWorkingTool(),
            ITCapabilityUpliftTool(),
            TalentWorkforceTool(),
            ChangeManagementTool()
        ]
        self.planner = AgentPlanner(self.llm, self.tools)
        self.memory  = AgentMemory(max_turns=10)

    def run(self, text, language="en"):
        context   = self.memory.get_context_summary()
        tool_name = self.planner.plan(text, context)
        result    = self.planner.act(tool_name, text, language)
        self.memory.add(text, language, text, tool_name, result["response"])
        return {
            "detected_language": language,
            "english_query"    : text,
            "selected_tool"    : tool_name,
            "response"         : result["response"]
        }