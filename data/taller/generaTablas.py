from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config import engine


Base = declarative_base()


class Continente(Base):
    __tablename__ = 'continentes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    paises = relationship("Pais", back_populates="continente")

    def __str__(self):
        return f"{self.nombre}"


class Pais(Base):
    __tablename__ = 'paises'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    continente_id = Column(Integer, ForeignKey('continentes.id'))

    continente = relationship("Continente", back_populates="paises")

    jugadores = relationship("Jugador", back_populates="pais")

    def __str__(self):
        return f"{self.nombre}"

class Jugador(Base):
    __tablename__ = 'jugadores'

    id = Column(Integer, primary_key=True)

    nombre = Column(String(200))
    posicion = Column(String(100))
    edad = Column(Integer)

    numero_partidos_seleccion = Column(Integer)
    goles_seleccion = Column(Integer)

    pais_donde_juega = Column(String(100))

    pais_id = Column(Integer, ForeignKey('paises.id'))

    pais = relationship("Pais", back_populates="jugadores")

    def __str__(self):
        return f"{self.nombre} - {self.pais.nombre}"


# Crear tablas
Base.metadata.create_all(engine)