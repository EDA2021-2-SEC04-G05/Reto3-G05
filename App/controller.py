"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

def loadData(analyzer, ufosfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufosfile = cf.data_dir + ufosfile
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    for ufos in input_file:
        model.addAvistamiento(analyzer, ufos)
    return analyzer


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def ufosSize(analyzer):
    """
    Numero de avistamientos leidos
    """
    return model.ufosSize(analyzer)

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)

def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

def getAvistamientosByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAvistamientosByRange(analyzer, initialDate.date(),
                                  finalDate.date())

def getAvistamientosByCity(analyzer, cityName,initialDate, finalDate):
    """
    Retorna el total de avistamientos en una ciudad
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAvistamientosByCity(analyzer,cityName,initialDate.date(),
                                  finalDate.date())

def getAvistamientosByHHMM(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate,'%H:%M')
    finalDate = datetime.datetime.strptime(finalDate,'%H:%M' )
    return model.getAvistamientosByHHMM(analyzer, initialDate.time(),
                                  finalDate.time())

def getAvistamientosByDuracion(analyzer,duracionmin,duracionmax):
    """
    Retorna el total de avistamientos en una ciudad
    """
    return model.getAvistamientosByDuracion(analyzer,duracionmin,
                                  duracionmax)

def getAvistamientosByRangeForPrint(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAvistamientosByRangeForPrint(analyzer, initialDate.date(),
                                  finalDate.date())

def getAvistamientosByRangeForPrint2(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAvistamientosByRangeForPrint2(analyzer, initialDate.date(),
                                  finalDate.date())

def getAvistamientosByRangeForPrint3(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAvistamientosByRangeForPrint3(analyzer, initialDate.date(),
                                  finalDate.date())

def getAvistamientosByRangeForPrint4(analyzer, minduracion, maxduracion):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    return model.getAvistamientosByRangeForPrint4(analyzer, minduracion,
                                  maxduracion)

def getAvistamientosByRangeForPrint5(analyzer, minduracion, maxduracion):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    minduracion = datetime.datetime.strptime('1999-08-06 ' + minduracion, '%Y-%m-%d %H:%M:%S') 
    maxduracion = datetime.datetime.strptime('1999-08-06 ' + maxduracion, '%Y-%m-%d %H:%M:%S')
    return model.getAvistamientosByRangeForPrint5(analyzer, minduracion.time(),
                                  maxduracion.time())

def concatlist(lst1,lst2):
    return model.concatlist(lst1,lst2)