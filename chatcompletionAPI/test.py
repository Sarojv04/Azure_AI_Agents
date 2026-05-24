import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("MODEL_DEPLOYMENT_NAME_EX"))