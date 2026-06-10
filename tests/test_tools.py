import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.tool_new_operating_model  import NewOperatingModelTool
from tools.tool_new_ways_of_working  import NewWaysOfWorkingTool
from tools.tool_it_capability_uplift import ITCapabilityUpliftTool
from tools.tool_talent_workforce     import TalentWorkforceTool
from tools.tool_change_management    import ChangeManagementTool

def test_all_tools_english():
    tests = [
        (NewOperatingModelTool(),  "new_operating_model"),
        (NewWaysOfWorkingTool(),   "new_ways_of_working"),
        (ITCapabilityUpliftTool(), "it_capability_uplift"),
        (TalentWorkforceTool(),    "talent_workforce"),
        (ChangeManagementTool(),   "change_management"),
    ]
    for tool, expected_intent in tests:
        result = tool.run("test query", "en")
        assert result["intent"]   == expected_intent
        assert result["language"] == "en"
        assert len(result["response"]) > 10
        print("PASS: " + expected_intent)

def test_all_tools_thai():
    tests = [
        (NewOperatingModelTool(),  "new_operating_model"),
        (NewWaysOfWorkingTool(),   "new_ways_of_working"),
        (ITCapabilityUpliftTool(), "it_capability_uplift"),
        (TalentWorkforceTool(),    "talent_workforce"),
        (ChangeManagementTool(),   "change_management"),
    ]
    for tool, expected_intent in tests:
        result = tool.run("test query", "th")
        assert result["language"] == "th"
        print("PASS Thai: " + expected_intent)