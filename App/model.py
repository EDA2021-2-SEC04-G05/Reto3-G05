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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'avistamientos': None,
                'ciudades': None,
                'duracion':None,
                'fechas':None,
                'HH:MM':None,
                'zngeo':None
                }

    analyzer['avistamientos'] = lt.newList('SINGLE_LINKED')
    analyzer['fechas'] = om.newMap(omaptype='BTS',
                                      comparefunction=compareFechas)
    analyzer['ciudades'] = om.newMap(omaptype='BTS',
                                      comparefunction=compareCiudades)
    analyzer['duracion'] = om.newMap(omaptype='BTS',
                                      comparefunction=compareDuracion) 
    analyzer['HH:MM'] = om.newMap(omaptype='BTS',
                                      comparefunction=compareHHMM)   
    analyzer['zngeo'] = om.newMap(omaptype='BTS',
                                      comparefunction=comparezngeo)   
    return analyzer

# Funciones para agregar informacion al catalogo

def addAvistamiento(analyzer, ufos):
    """
    """
    lt.addLast(analyzer['avistamientos'], ufos)
    updateCity(analyzer['ciudades'], ufos)
    updateDateIndex(analyzer['fechas'], ufos)
    updateDuracion(analyzer['duracion'], ufos)
    updateHHMM(analyzer['HH:MM'], ufos)
    updatezngeo(analyzer['zngeo'],ufos)
    return analyzer

def updateCity(map, ufos):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    city = ufos['city']
    #crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, city)
    if entry is None:
        datentry = newMapEntry(ufos,compareFechas)
        om.put(map, city, datentry)
    else:
        datentry = me.getValue(entry)
    addCiudad(datentry, ufos)
    return map

def updateDateIndex(map, ufos):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    time = ufos['datetime']
    date = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') 
    entry = om.get(map, date.date())
    if entry is None:
        datentry = newDataEntry(ufos)
        om.put(map, date.date(), datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast((datentry)['lstavistamientos'],ufos)
    return map

def updateHHMM(map, ufos):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    time = ufos['datetime']
    date = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') 
    entry = om.get(map, date.time())
    if entry is None:
        datentry = newMapEntry(ufos,compareFechas)
        om.put(map, date.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addHHMM(datentry,ufos)
    return map

def updateDuracion(map, ufos):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    duracion = ufos['duration (seconds)']
    #crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, duracion)
    if entry is None:
        datentry = newMapEntry(ufos,compareCiudades)
        om.put(map, duracion, datentry)
    else:
        datentry = me.getValue(entry)
    addDuracion(datentry, ufos)
    return map

def updatezngeo(map, ufos):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    duracion = ufos['longitude']
    #crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, duracion)
    if entry is None:
        datentry = newMapEntry(ufos,comparezngeo)
        om.put(map, duracion, datentry)
    else:
        datentry = me.getValue(entry)
    addzngeo(datentry, ufos)
    return map

def addCiudad(map, ufos):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    time = ufos['datetime']
    date = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') 
    entry = om.get(map, date.date())
    if entry is None:
        datentry = newDataEntry(ufos)
        om.put(map, date.date(), datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast((datentry)['lstavistamientos'],ufos)
    return map

def addzngeo(map, ufos):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    geo = ufos['latitude']
    entry = om.get(map, geo)
    if entry is None:
        datentry = newDictEntry(ufos,'latitude','lstavistamientos','latitude',comparezngeo)
        om.put(map, geo, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast((datentry)['lstavistamientos'],ufos)
    return map

def addHHMM(map, ufos):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    time = ufos['datetime']
    date = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') 
    entry = om.get(map, date.date())
    if entry is None:
        datentry = newDataEntry(ufos)
        om.put(map, date.date(), datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast((datentry)['lstavistamientos'],ufos)
    return map
    
def addDuracion(map, ufos):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    ciudad = ufos['city']
    entry = om.get(map, ciudad)
    if entry is None:
        datentry = newDictEntry(ufos,'ciudad','lstavistamientos','city',compareCiudades)
        om.put(map, ciudad, datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast((datentry)['lstavistamientos'],ufos)
    return map
    
def newDataEntry(ufos):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'date': None, 'lstavistamientos': None}
    entry['date'] = ufos['datetime']
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED', compareFechas)
    return entry

def newDictEntry(ufos,cadkey,cadvalue,namecol,comparar):
    """
    Crea un dict, con dos llaves: cadkey y cadvalue. El valor de cadkey es el atributo namecol del renglon leido
    El valor cadvalue es una lista de los renglones asociados a cadkey.
    """
    entry = {cadkey: None, cadvalue: None}
    entry[cadkey] = ufos[namecol]
    entry[cadvalue] = lt.newList('SINGLE_LINKED', comparar)
    return entry

def newMapEntry(ufos,clasificacion):
    entry = om.newMap(omaptype='BST', comparefunction=clasificacion)
    return entry 

# Funciones para creacion de datos

# Funciones de consulta

def ufosSize(analyzer):
    """
    Número de avistamientos y fechas 
    """
    #return lt.size(analyzer['avistamientos'])
    return [lt.size(analyzer['avistamientos']),om.size(analyzer['fechas']),om.size(analyzer['ciudades']),om.size(analyzer['duracion']),om.size(analyzer['HH:MM']),om.size(analyzer['zngeo'])]


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer)


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer)


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer) 


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer)

def getAvistamientosByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['fechas'], initialDate, finalDate)
    totavistamientos = 0
    for lstdate in lt.iterator(lst):
        totavistamientos += lt.size(lstdate['lstavistamientos'])
    return totavistamientos

def getAvistamientosByCity(analyzer, cityName,initialDate, finalDate):
    """
    Retorna el numero de avistamientos en una ciudad.
    """
    fechas = om.get(analyzer['ciudades'],cityName)
    lst = om.values(fechas['value'], initialDate, finalDate)
    totavistamientos = 0
    for lstdate in lt.iterator(lst):
        totavistamientos += lt.size(lstdate['lstavistamientos'])
    return totavistamientos

def getAvistamientosByDuracion(analyzer, duracionmin,duracionmax):
    """
    Retorna el numero de avistamientos en una ciudad.
    """
    lst = om.values(analyzer['duracion'], duracionmin,duracionmax)
    totavistamientos = 0
    for lstduracion in lt.iterator(lst):
        min = om.minKey(lstduracion)
        max = om.maxKey(lstduracion)
        lst2 = om.values(lstduracion,min,max)
        for lstciudad in lt.iterator(lst2):
            totavistamientos += lt.size(lstciudad['lstavistamientos'])
    return totavistamientos

def getAvistamientosByZnGeo(analyzer,longitudemin,longitudenmax,latitudemin,latitudemax):
    """
    Retorna el numero de avistamientos en una ciudad.
    """
    lst = om.values(analyzer['zngeo'],longitudemin,longitudenmax) 
    totavistamientos = 0
    for lstduracion in lt.iterator(lst):
        min = latitudemin
        max = latitudemax
        lst2 = om.values(lstduracion,min,max)
        for lstciudad in lt.iterator(lst2):
            totavistamientos += lt.size(lstciudad['lstavistamientos'])
    return totavistamientos

def getAvistamientosByHHMM(analyzer, HHMMinicial,HHMMfinal):
    """
    Retorna el numero de avistamientos en una ciudad.
    """
    lst = om.values(analyzer['HH:MM'], HHMMinicial,HHMMfinal)
    totavistamientos = 0
    for lstduracion in lt.iterator(lst):
        min = om.minKey(lstduracion)
        max = om.maxKey(lstduracion)
        lst2 = om.values(lstduracion,min,max)
        for lstciudad in lt.iterator(lst2):
            totavistamientos += lt.size(lstciudad['lstavistamientos'])
    return totavistamientos

def getAvistamientosByRangeForPrint(analyzer, initialDate, finalDate):
    """
    Retorna los tres primeros y los tres ultimos avistamientos
    """
    Avist=lt.newList('SINGLE_LINKED', compareFechas)
    lst = om.values(analyzer['fechas'], initialDate, finalDate)
    totalvist = 0
    for lstdate in lt.iterator(lst):
        totalvist += lt.size(lstdate['lstavistamientos'])
        for row in lt.iterator(lstdate["lstavistamientos"]):
            lt.addLast(Avist,row)
    if totalvist<7:
        return Avist
    else:
        return concatlist(lt.subList(Avist,1,3),lt.subList(Avist,totalvist-2,3))

def getAvistamientosByRangeForPrint2(analyzer, initialDate, finalDate):
    """
    Retorna los tres primeros y los tres ultimos avistamientos
    """
    
    Avist=lt.newList('SINGLE_LINKED', compareFechas)
    lst = om.values(analyzer, initialDate, finalDate)
    totalvist = 0
    for lstdate in lt.iterator(lst):
        totalvist += lt.size(lstdate['lstavistamientos'])
        for row in lt.iterator(lstdate["lstavistamientos"]):
            lt.addLast(Avist,row)
    if totalvist<7:
        return Avist
    else:
        return concatlist(lt.subList(Avist,1,3),lt.subList(Avist,totalvist-2,3))

def getAvistamientosByRangeForPrint3(analyzer, initialDate, finalDate):
    """
    Retorna los tres primeros y los tres ultimos avistamientos
    """
    Avist=lt.newList('SINGLE_LINKED', compareFechas)
    lst = om.values(analyzer['fechas'], initialDate, finalDate)
    totalvist = 0
    for lstdate in lt.iterator(lst):
        totalvist += lt.size(lstdate['lstavistamientos'])
        for row in lt.iterator(lstdate["lstavistamientos"]):
            lt.addLast(Avist,row)
    return Avist

def getAvistamientosByRangeForPrint4(analyzer, minduracion, maxduracion):
    """
    Retorna los tres primeros y los tres ultimos avistamientos
    """
    Avist=lt.newList('SINGLE_LINKED')# compareCiudades)
    lst = om.values(analyzer['duracion'], float(minduracion),float(maxduracion))
    totalvist = 0
    for lstdate in lt.iterator(lst):
        min = om.minKey(lstdate)
        max = om.maxKey(lstdate)
        lst2 = om.values(lstdate,min,max)
        for lstciudad in lt.iterator(lst2):
            totalvist += lt.size(lstciudad['lstavistamientos'])
            for row in lt.iterator(lstciudad["lstavistamientos"]):
                lt.addLast(Avist,row)
    return Avist

def getAvistamientosByRangeForPrint5(analyzer, minduracion, maxduracion):
    """
    Retorna los tres primeros y los tres ultimos avistamientos
    """
    Avist=lt.newList('SINGLE_LINKED')# compareCiudades)
    lst = om.values(analyzer['HH:MM'], minduracion,maxduracion)
    totalvist = 0
    for lstdate in lt.iterator(lst):
        min = om.minKey(lstdate)
        max = om.maxKey(lstdate)
        lst2 = om.values(lstdate,min,max)
        for lstciudad in lt.iterator(lst2):
            totalvist += lt.size(lstciudad['lstavistamientos'])
            for row in lt.iterator(lstciudad["lstavistamientos"]):
                lt.addLast(Avist,row)
    return Avist

def getAvistamientosByRangeForPrint6(analyzer,longitudemin,longitudenmax,latitudemin,latitudemax):
    """
    Retorna los tres primeros y los tres ultimos avistamientos
    """
    Avist=lt.newList('SINGLE_LINKED')# compareCiudades)
    lst = om.values(analyzer['zngeo'],longitudemin,longitudenmax)
    totalvist = 0
    for lstdate in lt.iterator(lst):
        min = latitudemin
        max = latitudemax
        lst2 = om.values(lstdate,min,max)
        for lstciudad in lt.iterator(lst2):
            totalvist += lt.size(lstciudad['lstavistamientos'])
            for row in lt.iterator(lstciudad["lstavistamientos"]):
                lt.addLast(Avist,row)
    return Avist

    """
    Retorna los tres primeros y los tres ultimos avistamientos
    """
    Avist=lt.newList('SINGLE_LINKED')# compareCiudades)
    lst = om.values(analyzer['HH:MM'], minduracion,maxduracion)
    totalvist = 0
    for lstdate in lt.iterator(lst):
        min = om.minKey(lstdate)
        max = om.maxKey(lstdate)
        lst2 = om.values(lstdate,min,max)
        for lstciudad in lt.iterator(lst2):
            totalvist += lt.size(lstciudad['lstavistamientos'])
            for row in lt.iterator(lstciudad["lstavistamientos"]):
                lt.addLast(Avist,row)
    return Avist



def concatlist(lst1,lst2):
    """
    Recibe dos listas, agrega los elementos de la segunda lista al final de la primera y retorna dicha lista 
    """
    for elem in lt.iterator(lst2):
        lt.addLast(lst1,elem)
    return lst1

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def compareCiudades(ciudad1, ciudad2):
    """
    Compara dos ciudades
    """
    if (ciudad1 == ciudad2):
        return 0
    elif ciudad1 > ciudad2:
        return 1
    else:
        return -1

def compareFechas(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareDuracion(duracion1, duracion2):
    """
    Compara dos fechas
    """
    if (float(duracion1) == float(duracion2)):
        return 0
    elif (float(duracion1) > float(duracion2)):
        return 1
    else:
        return -1

def compareHHMM(date1, date2):
    """
    Compara dos HH:MM
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def comparezngeo(geo1, geo2):
    """
    Compara dos fechas
    """
    if (float(geo1) == float(geo2)):
        return 0
    elif (float(geo1) > float(geo2)):
        return 1
    else:
        return -1
