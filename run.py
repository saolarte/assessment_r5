from dotenv import load_dotenv
from api.app import app
import uvicorn

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)