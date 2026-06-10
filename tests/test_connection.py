import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.watsonx_config import verify_connection

def test_watsonx_connects():
    result = verify_connection()
    print(result)
    assert result["status"] == "Connected"