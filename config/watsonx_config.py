import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

def get_watsonx_model():
    creds = Credentials(
        url     = os.getenv("WATSONX_URL"),
        api_key = os.getenv("WATSONX_API_KEY")
    )
    client = APIClient(creds)
    return ModelInference(
        model_id   = "meta-llama/llama-3-3-70b-instruct",
        api_client = client,
        project_id = os.getenv("WATSONX_PROJECT_ID"),
        params     = {"max_new_tokens": 50, "temperature": 0.0}
    )

def verify_connection():
    try:
        model = get_watsonx_model()
        test  = model.generate_text(prompt="Say: OK")
        return {"status": "Connected", "response": test.strip()}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}