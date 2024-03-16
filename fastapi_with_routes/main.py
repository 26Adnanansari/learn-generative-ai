from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return "Hello, who are you"

@app.get("/name")
def hello():
    return "Hello, what is your name"

@app.get("/store")
def hello():
    return "give me some detail, Name of item, Cetogery , Description , Price"