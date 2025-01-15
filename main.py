from fastapi import FastAPI

app = FastAPI()

@app.get("/ali/a")
def read_root():
    return {"message": "Hello, FastAPI!"}
