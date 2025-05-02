import uvicorn
import os


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT",10000))  # Get PORT from environment variable, default to 8000
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)  