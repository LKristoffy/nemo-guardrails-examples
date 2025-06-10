import logging
from nemoguardrails import LLMRails, RailsConfig
from dotenv import load_dotenv
import os
import spacy
# Load environment variables from .env file
load_dotenv()

# Check if the required environment variable is set
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("OPENAI_API_KEY is not set in the environment variables.")

# Check if Spacy model 'en_core_web_lg' is available
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    raise OSError("Spacy model 'en_core_web_lg' is not installed. Please run 'python -m spacy download en_core_web_lg' to install it.")

    

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("nemoguardrails").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

try:
    # Initialize the RailsConfig with the path to your Rails file
    config = RailsConfig.from_path("./src/examples/input-checking/config/config.yml")
    logger.info("RailsConfig initialized successfully.")
    
    guardrails = LLMRails(config)
except Exception as e:
    logger.error(f"Failed to initialize LLMRails: {e}")
    raise


def main():
    guardrails = LLMRails(config)
    logger.info("LLMRails instance created successfully.")


    msg = [{"role": "user", "content": "Hi, I’m Alice (alice@example.com)"}]
    logger.info(f"Message to be processed: {msg}")

    guardrails_ouput = guardrails.generate(messages=msg, options={"rails": ["input"]})
    logger.info(f"Guardrails output: {guardrails_ouput}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred in main: {e}")
        raise
    else:
        logger.info("Execution completed successfully.")

