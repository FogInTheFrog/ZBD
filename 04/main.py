from fastapi import FastAPI
from database import get_db
import crud

app = FastAPI()

if __name__ == '__main__':
    print(crud.get_shortest_path(get_db(), 12126782, 12132897))
