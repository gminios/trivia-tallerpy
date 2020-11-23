#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta, Usuario, Respuesta, Role

db.drop_all()
db.create_all()

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")
c_cultura = Categoria(descripcion="Cultura")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?", categoria=c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?", categoria=c_geogra)
q_mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1982?", categoria=c_deporte)
q_cine1 = Pregunta(text="'No es tan difícil hacer dinero cuando es solo hacer dinero lo que se pretende'. ¿A qué película corresponde esta frase?",categoria=c_cultura)

#respuestas
r_Laos1= Respuesta(text="Hanoi", pregunta=q_Laos, correcta=False)
r_Laos2= Respuesta(text="Vientián", pregunta=q_Laos, correcta=True)
r_Laos3= Respuesta(text="Shangai", pregunta=q_Laos, correcta=False)

r_Armenia1 = Respuesta(text="5 millones", pregunta=q_Armenia, correcta=False)
r_Armenia2 = Respuesta(text="3 millones", pregunta=q_Armenia, correcta=True)
r_Armenia3 = Respuesta(text="7 millones", pregunta=q_Armenia, correcta=False)

r_Mundial1 = Respuesta(text="México", pregunta=q_mundial, correcta=False)
r_Mundial2 = Respuesta(text="Inglaterra", pregunta=q_mundial, correcta=False)
r_Mundial3 = Respuesta(text="España", pregunta=q_mundial, correcta=True)

r_cine1 = Respuesta(text="Ciudadano Kane", pregunta=q_cine1, correcta=True)
r_cine2 = Respuesta(text="El color del dinero", pregunta=q_cine1, correcta=False)
r_cine3 = Respuesta(text="El lobo de Wall Street", pregunta=q_cine1, correcta=False)

#Creo un usuario administrador y otro común
q_u1 = Usuario(name="Admin", email="jminos@antel.com.uy")
# el pass lo seteamos con el método set_password para que se guarde con hash
q_u1.set_password("admin");

q_u2 = Usuario(name="Gonzalo", email="gminos@gmail.com")
q_u2.set_password("admin");

db.session.add(c_geogra)
db.session.add(c_deporte)
db.session.add(c_cultura)

db.session.add(q_Laos)
db.session.add(q_Armenia)
db.session.add(q_mundial)

db.session.add(r_Laos1)
db.session.add(r_Laos2)
db.session.add(r_Laos3)
db.session.add(r_Armenia1)
db.session.add(r_Armenia2)
db.session.add(r_Armenia3)
db.session.add(r_Mundial1)
db.session.add(r_Mundial2)
db.session.add(r_Mundial3)
db.session.add(r_cine1)
db.session.add(r_cine2)
db.session.add(r_cine3)

db.session.add_all([q_u1, q_u2])
db.session.add_all(
         [Role(rolename='admin', user=q_u1),
          Role(rolename='user', user=q_u2)])

db.session.commit()

# creamos otros usuarios (…) y los recorremos
categorias = Categoria.query.all()
for c in categorias:
    print(c.id, c.descripcion)
    # para cada categoria, obtenemos sus preguntas y las recorremos
    for p in c.preguntas:
        print(p.id, p.text)


cat = Categoria.query.get(1)
print(cat)
