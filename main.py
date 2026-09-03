from fastapi import FastAPI
import random

app = FastAPI()


def convertir_a_romano(numero: int) -> str:
    valores = (
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )
    resultado = ""
    for valor, simbolo in valores:
        cantidad, numero = divmod(numero, valor)
        resultado += simbolo * cantidad
    return resultado


@app.get("/obtenerCedula")
def obtener_cedula():
    cedula = random.randint(1_000_000_000, 9_999_999_999)
    return {"cedula": cedula}


@app.get("/obtenerNumeroRomano")
def obtener_numero_romano():
    numero = random.randint(50, 100)
    return {"numero": numero, "romano": convertir_a_romano(numero)}
