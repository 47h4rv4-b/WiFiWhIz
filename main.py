from fastapi import FastAPI
from ensemble_espdata import get_accuracy_data
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/accuracy")
def accuracy():
    return get_accuracy_data();
    # return {"Accuracy":"1321431"}