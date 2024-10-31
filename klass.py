from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 0):
    return {'sum': skip + limit}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {'item_id': item_id}