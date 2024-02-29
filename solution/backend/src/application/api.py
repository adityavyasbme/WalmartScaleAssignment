from fastapi import APIRouter
from src.application import workflow as wf

router = APIRouter()


def number_of_models():
    raw_data = get_raw_data()
    # processed_data = pre_process(raw_data)
