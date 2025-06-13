import base64
import json

from nemoguardrails import RailsConfig
from nemoguardrails.rails.llm.llmrails import LLMRails

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config = RailsConfig.from_path("./src/examples/multimodal/config")
rails = LLMRails(config)

with open("./src/examples/multimodal/images/gun.jpg", "rb") as image_file:
  base64_image = base64.b64encode(image_file.read()).decode()

messages = [{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "what is the surface color that the object is placed on?",
    },
    {
      "type": "image_url",
      "image_url": {
          "url": f"data:image/jpeg;base64,{base64_image}"
      },
    },
  ],
}]

response = rails.generate(messages=messages)
print(json.dumps(response, indent=2))