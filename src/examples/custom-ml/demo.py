import logging
import os 
from nemoguardrails import LLMRails, RailsConfig
from scripts.train import train_model
try:
    from config.actions import validate_tabular
except ImportError:
    from .config.actions import validate_tabular



# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("nemoguardrails").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

try:
    # Initialize the RailsConfig with the path to your Rails file
    try:
        config = RailsConfig.from_path("./src/examples/custom-ml/config")
    except ValueError:
        config = RailsConfig.from_path("./config")
    logger.info("RailsConfig initialized successfully.")
    
    guardrails = LLMRails(config)
except Exception as e:
    logger.error(f"Failed to initialize LLMRails: {e}")
    raise

def check_data_exists():
    """
    Check if the test data file exists.
    If not, train the model to generate the data.
    """
    data_path = "./src/examples/custom-ml/data/test_data.csv"
    if not os.path.exists(data_path):
        logger.info("Test data file not found. Training model to generate data...")
        train_model()
        logger.info("Model trained and test data generated.")
    else:
        logger.info("Test data file already exists.")

def main():
    guardrails = LLMRails(config)
    logger.info("LLMRails instance created successfully.")
    # Example usage of the guardrails instance
    output_text = "This is a sample output text that needs validation."
    logger.info(f"Output text to validate: {output_text}")

    msg = [{"role": "user", "content": ""}]
    logger.info(f"Message to be processed: {msg}")

    # To run with generate method, need to specify a message as this is for a chat model
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
