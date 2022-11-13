import operator

from bson import ObjectId
from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Resultados import Resultado
from operator import itemgetter
import json
class RepositorioResultados(InterfaceRepositorio[Resultado]):
    pass

    """Listado todos los votos obtenidos por todos los candidatos"""
    def getListadoResultadosPorCandidato(self,id_candidato):
        theQuery = {"candidato.$id": ObjectId(id_candidato)}
        return self.query(theQuery)

    """Listado todos los votos registrados en todas las mesas"""
    def getListadoResultadosPorMesa(self,id_mesa):
        theQuery = {"mesa.$id":ObjectId(id_mesa)}
        return self.query(theQuery)

    """Lista los candidatos ganadores"""
    def getVotacionMasAlta(self):
        query1={
            "$group": {
                "_id": "$candidato",
                "Total_votos": {
                    "$sum": 1
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }
        pipeline = [query1]
        lista = self.queryAggregation(pipeline)
        maximo = 0
        candidatos = []
        for candidatoConTodo in lista:
            t = candidatoConTodo["Total_votos"]
            print(t)
            if t > maximo:
               maximo = t
        for candidatoConTodo in lista:
            votos = candidatoConTodo["Total_votos"]
            if votos == maximo:
                resultado = []
                candidato = candidatoConTodo.get("doc")
                elem = candidato.get("candidato")
                nombre = elem.get("nombre")
                apellido = elem.get("apellido")
                nombrecompleto = nombre + " " + apellido
                resultado.append(nombrecompleto)
                resultado.append(votos)
                candidatos.append(resultado)
        return candidatos

    """8.b - Listado el consolidado de los votos registrados en las mesas"""
    def consolidadoMesas(self):
        query= {
            "$group":{
                "_id":"$mesa",
                "Total_Votos ":{
                    "$count":{}
                         },
            "doc": {
                "$first": "$$ROOT"
                }
            }
        }
        pipeline =[query]
        lista = self.queryAggregation(pipeline)
        ordenado = sorted(lista, key=lambda votos: votos['Total_Votos '])
        listado = []
        for mesaConTodo in ordenado:
            resultado = []
            votos = mesaConTodo.get("Total_Votos ")  # obtener los votos
            mesa = mesaConTodo.get("doc")  # desde aqui obtener elnombre del partido
            elemMesa = mesa.get("mesa")
            numeroMesa = elemMesa.get("num_mesa")
            resultado.append(numeroMesa)
            resultado.append(votos)
            listado.append(resultado)
        return listado

    """"8.a.1 - Listado Votos de todos los candidatos con su partido en todas las mesas - ordenados de mayor a menor"""

    def listadoVotosCandidatoPartidosyMesas(self):
        query1 = {
            "$group": {
                "_id": "$candidato",
                "Total_votos": {
                    "$sum": 1
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }
        pipeline = [query1]
        lista = self.queryAggregation(pipeline)
        ordenado = sorted(lista, key=lambda votos: votos['Total_votos'], reverse=True)
        listadoVotos=[]
        for candidatoConTodo in ordenado:
            resultado=[]
            votosCandidato = candidatoConTodo.get("Total_votos")  # obtener los votos
            candidato = candidatoConTodo.get("doc")  # desde aqui obtener elnombre del partido
            elemDelCandidato = candidato.get("candidato")
            nombreCandidato = elemDelCandidato.get("nombre")
            apellidoCandidato = elemDelCandidato.get("apellido")
            nombreCompleto = nombreCandidato + " " + apellidoCandidato
            numeroDelCandidato = elemDelCandidato.get("numero")
            partidoDelCandidato = elemDelCandidato.get("partido")
            nombrePartido = partidoDelCandidato.get("nombre")
            resultado.append(numeroDelCandidato)
            resultado.append(nombreCompleto)
            resultado.append(votosCandidato)
            resultado.append(nombrePartido)
            listadoVotos.append(resultado)
        return listadoVotos

    """"8.a.2 - Listado Votos de todos los candidatos con su partido en una mesa - ordenados de mayor a menor"""

    def listadoVotosCandidatoPartidosxMesa(self,id_mesa):
        query1 = {
            "$match": {"mesa.$id": ObjectId(id_mesa)}
        }
        query2 = {
            "$group": {
                "_id": "$candidato",
                "Total_votos": {
                    "$sum": 1
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }
        pipeline = [query1,query2]
        lista = self.queryAggregation(pipeline)
        ordenado = sorted(lista, key=lambda votos: votos['Total_votos'], reverse=True)
        listadoVotos=[]
        for candidatoConTodo in ordenado:
            resultado = []
            votosCandidato = candidatoConTodo.get("Total_votos")  # obtener los votos
            candidato = candidatoConTodo.get("doc")  # desde aqui obtener elnombre del partido
            elemDelCandidato = candidato.get("candidato")
            nombreCandidato = elemDelCandidato.get("nombre")
            apellidoCandidato = elemDelCandidato.get("apellido")
            nombreCompleto = nombreCandidato + " " + apellidoCandidato
            numeroDelCandidato = elemDelCandidato.get("numero")
            partidoDelCandidato = elemDelCandidato.get("partido")
            nombrePartido = partidoDelCandidato.get("nombre")
            resultado.append(numeroDelCandidato)
            resultado.append(nombreCompleto)
            resultado.append(votosCandidato)
            resultado.append(nombrePartido)
            listadoVotos.append(resultado)
        return listadoVotos



    """"8.c.1 - Listado Votos partidos en todas las mesas - ordenados de mayor a menor"""

    def listadoPartidosenMesas(self):
        listadoGeneral=self.findAll()
        diccPartidos = {}
        listaPartidos = []
        for diccionario in listadoGeneral:
            candidato = diccionario.get('candidato')
            partido = candidato.get('partido')
            idPartido = partido.get('_id')
            nombPartido = partido.get('nombre')
            if idPartido in listaPartidos:
                diccPartidos[nombPartido] = diccPartidos[nombPartido] + 1
            else:
                listaPartidos.append(idPartido)
                diccPartidos[nombPartido] = 1
        Ordenado = sorted(diccPartidos.items(), key=operator.itemgetter(1), reverse=True)
        return Ordenado

    """"8.c.2 - Listado Votos partidos en una mesas - ordenados de mayor a menor"""

    def listadoPartidosxMesa(self,id_mesa):
        listadoGeneral=self.findAll()
        diccPartidos = {}
        listaPartidos = []
        mesa = id_mesa
        for diccionario in listadoGeneral:
            mesaCompleta = diccionario.get('mesa')
            if mesaCompleta.get('_id') == mesa:
                candidato = diccionario.get('candidato')
                partido = candidato.get('partido')
                idPartido = partido.get('_id')
                nombPartido = partido.get('nombre')
                if idPartido in listaPartidos:
                    diccPartidos[nombPartido] = diccPartidos[nombPartido] + 1
                else:
                    listaPartidos.append(idPartido)
                    diccPartidos[nombPartido] = 1
        Ordenado = sorted(diccPartidos.items(), key=operator.itemgetter(1), reverse=True)
        return Ordenado

    """"8.d- Distribucion porcentual por partido politico del nuevo congreso de la republica"""

    def distribucionPorcentualPartidos(self):
        query1 = {
            "$group": {
                "_id": "$candidato",
                "Total_votos": {
                    "$sum": 1
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }
        pipeline = [query1]
        lista = self.queryAggregation(pipeline)
        ordenado = sorted(lista, key=lambda votos: votos['Total_votos'], reverse=True)
        diccPartidos = {}
        listaPartidos = []
        for candidatoConTodo in ordenado[0:15]:
            candidato = candidatoConTodo.get("doc")
            elemDelCandidato = candidato.get("candidato")
            partidoDelCandidato = elemDelCandidato.get("partido")
            idPartido = partidoDelCandidato.get('_id')
            nombrePartido = partidoDelCandidato.get("nombre")
            if idPartido in listaPartidos:
                diccPartidos[nombrePartido] = diccPartidos[nombrePartido] + 1
            else:
                listaPartidos.append(idPartido)
                diccPartidos[nombrePartido] = 1
        for i in diccPartidos:
            diccPartidos[i] = round(diccPartidos[i]/15*100,1)
        Ordenado = sorted(diccPartidos.items(), key=operator.itemgetter(1), reverse=True)
        return Ordenado

