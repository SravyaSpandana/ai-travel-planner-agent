from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
if api_key:
    print("Succesfully got API KEY")
else:
    print("Failed to read api key from env variabels")