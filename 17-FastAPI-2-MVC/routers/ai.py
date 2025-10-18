from fastapi import APIRouter
from controllers.query import get_query_answer

router = APIRouter(prefix="/ai", tags=["Users"])

@router.get("/query/")
def query_ai(q: str):
    return get_query_answer(q)