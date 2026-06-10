import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent.agent_core import KTBClientZeroAgent

agent = KTBClientZeroAgent()

def test_agent_loads():
    assert agent is not None
    assert len(agent.tools) == 5
    print("PASS: Agent loaded with 5 tools")

def test_english_routing():
    cases = [
        ("How is KTB moving away from siloed IT?",                   "new_operating_model"),
        ("Tell me about human-agent collaboration",                   "new_ways_of_working"),
        ("How are IT pipelines being upgraded?",                      "it_capability_uplift"),
        ("How is KTB reskilling its developers?",                    "talent_workforce"),
        ("How is KTB building an AI-native transformation culture?",  "change_management"),
    ]
    for query, expected in cases:
        result = agent.run(text=query, language="en")
        assert result["selected_tool"] == expected, "FAIL: " + query + " -> got " + result["selected_tool"]
        print("PASS: " + expected)

def test_memory():
    agent.memory.clear()
    agent.run(text="Tell me about operating model", language="en")
    assert len(agent.memory.history) == 1
    agent.memory.clear()
    assert len(agent.memory.history) == 0
    print("PASS: Memory works")