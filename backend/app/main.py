from fastapi import FastAPI

app = FastAPI(title="AIOps NOC Platform")


@app.get("/")
def root():
    return {"status": "ok"}