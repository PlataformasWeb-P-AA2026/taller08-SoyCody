import pandas as pd

from sqlalchemy.orm import sessionmaker

from config import engine
from generaTablas import Continente, Pais, Jugador

Session = sessionmaker(bind=engine)
session = Session()

diccionario_continentes = {
    "Alemania":      "Europa",
    "Argentina":     "América del Sur",
    "Australia":     "Oceanía",
    "Brasil":        "América del Sur",
    "Ecuador":       "América del Sur",
    "España":        "Europa",
    "Estados Unidos":"América del Norte",
    "Francia":       "Europa",
    "Inglaterra":    "Europa",
    "Japón":         "Asia",
    "Marruecos":     "África",
    "México":        "América del Norte",
    "Nigeria":       "África",
    "Portugal":      "Europa",
    "Senegal":       "África",
}

datos = pd.read_csv("../jugadores_futbol.csv")

for i, fila in datos.iterrows():

    nombre_pais = fila["pais_nacimiento"]

    nombre_continente = diccionario_continentes.get(
        nombre_pais,
        "Desconocido"
    )

    continente = session.query(Continente).filter_by(
        nombre=nombre_continente
    ).first()

    if continente is None:

        continente = Continente(
            nombre=nombre_continente
        )

        session.add(continente)
        session.commit()

    pais = session.query(Pais).filter_by(
        nombre=nombre_pais
    ).first()

    if pais is None:

        pais = Pais(
            nombre=nombre_pais,
            continente=continente
        )

        session.add(pais)
        session.commit()

    jugador = Jugador(
        nombre=fila["nombre_jugador"],
        posicion=fila["posicion"],
        edad=int(fila["edad"]),
        numero_partidos_seleccion=int(
            fila["numero_partidos_seleccion"]
        ),
        goles_seleccion=int(
            fila["goles_seleccion"]
        ),
        pais_donde_juega=fila["pais_donde_juega"],

        # RELACIÓN ORM
        pais=pais
    )

    session.add(jugador)

session.commit()

print("DATOS MIGRADOS CORRECTAMENTE")