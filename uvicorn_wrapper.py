import uvicorn
import os

os.environ["DB_CON"] = "sqlite:///database/tst.db"
from main import app
uvicorn.run(app, host="0.0.0.0", port=8000)
