from fastapi import FastAPI
import pickle
import uvicorn

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    dewpoint: str
    temperature: str
    pressure: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/response/")
async def response(
    capacidad_pasajeros: int,
    total_conductor: int,
    total_acompanante: int,
    total_pasajero: int,
    total_peaton: int,
    sector: int,
    gravedad: int,
    carac_viaRecCur: int,
    carc_planaLom: int,
    sentido_via: int,
    cant_carriles: int,
):
    #print (capacidad_pasajeros)
    with open("./prediccion_heridos.pkl", "rb") as file:
    
        model = pickle.load(file)
    
    parametros = [[capacidad_pasajeros, total_conductor, total_acompanante, total_pasajero, total_peaton, sector, gravedad, carac_viaRecCur, carc_planaLom, sentido_via, cant_carriles]]

    result = model.predict(parametros)
    
    return {"result": f"{result}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
