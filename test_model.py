from google.genai import Client
from core.config import GEMINI_API_KEY

client = Client(api_key=GEMINI_API_KEY)

# List available models
models = client.models.list()
for model in models:
    print(f"Model: {model.name}")
    print(f"  Display name: {model.display_name if hasattr(model, 'display_name') else 'N/A'}")
    print(f"  Description: {model.description if hasattr(model, 'description') else 'N/A'}")
    
    # Print all available attributes
    print(f"  Attributes: {dir(model)}")
    print()