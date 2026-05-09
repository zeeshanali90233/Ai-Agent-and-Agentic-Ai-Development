from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root(obt_marks:int,total_marks:int):
    calculated_per = (obt_marks / total_marks) * 100
    return {"calculated_percentage": calculated_per}


@app.get("/products/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}