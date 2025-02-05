from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.contact import router as routerContact

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("venv/main:app", host="0.0.0.0", port=8000, reload=True)

app.include_router(routerContact)