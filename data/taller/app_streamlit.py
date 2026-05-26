import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from config import engine
from migrar_datos import Continente, Pais, Jugador

Session = sessionmaker(bind=engine)
session = Session()

st.title("Jugadores de Fútbol")

st.header("Tabla de Jugadores")

jugadores = session.query(Jugador).all()

lista_jugadores = []

for j in jugadores:

    diccionario = {
        "nombre_jugador": j.nombre,
        "pais_nacimiento": j.pais.nombre,
        "pais_donde_juega": j.pais_donde_juega,
        "posicion": j.posicion,
        "edad": j.edad,
        "numero_partidos_seleccion": j.numero_partidos_seleccion,
        "goles_seleccion": j.goles_seleccion,
        "continente": j.pais.continente.nombre
    }

    lista_jugadores.append(diccionario)

st.dataframe(lista_jugadores)

st.header("Jugadores y goles por continente")

consulta_continentes = session.query(
    Continente.nombre,
    func.count(Jugador.id),
    func.sum(Jugador.goles_seleccion)
).join(Continente.paises).join(Pais.jugadores).group_by(
    Continente.nombre
).all()

lista_continentes = []

for c in consulta_continentes:

    diccionario = {
        "continente": c[0],
        "numero_jugadores": c[1],
        "numero_goles": c[2]
    }

    lista_continentes.append(diccionario)

st.dataframe(lista_continentes)

st.header("Jugadores y goles por país")

consulta_paises = session.query(
    Pais.nombre,
    func.count(Jugador.id),
    func.sum(Jugador.goles_seleccion)
).join(Pais.jugadores).group_by(
    Pais.nombre
).all()

lista_paises = []

for p in consulta_paises:

    diccionario = {
        "pais": p[0],
        "numero_jugadores": p[1],
        "numero_goles": p[2]
    }

    lista_paises.append(diccionario)

st.dataframe(lista_paises)