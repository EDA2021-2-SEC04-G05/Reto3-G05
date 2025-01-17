﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import sys
import prettytable
import config
import folium
from flask import Flask
from DISClib.DataStructures import orderedmapstructure as om
from DISClib.ADT import list as lt
from App import controller
assert config
from prettytable import PrettyTable

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Carga de datos")
    print("1- Contar los avistamientos en una ciudad")
    print("2- Contar los avistamientos por duración")
    print("3- Contar los avistamientos por hora/minutos del día")
    print("4- Contar los avistamientos en un rango de fechas")
    print("5- Contar los avistamientos de una zona geográfica")
    print("6- Visualizar los avistamientos de una zona geográfica")
    
ufosfile = 'UFOS-utf8-small.csv'
cont = None
catalog = None

def printCargarDatos(analyzer):
    x = PrettyTable()
    x.field_names = ["datetime","city","state","country","shape","duration (seconds)","duration (hours/min)","comments","date posted","latitude","longitude"]
    ancho_max = 5
    if lt.size(analyzer['avistamientos']) <= 10:
            for ufos in lt.iterator(analyzer['avistamientos']):
                a = [ufos["datetime"],ufos["city"],ufos["state"],ufos["country"],ufos["shape"],ufos["duration (seconds)"],ufos["duration (hours/min)"],ufos["comments"],ufos["date posted"],ufos["latitude"],ufos["longitude"]]
                d = []
                for i in a:
                    d.append(salto(i,ancho_max))
                x.add_row(d)
            print(x)
    else:
            l = lt.size(analyzer['avistamientos'])
            #pos = [artistas[0],artistas[1],artistas[2],artistas[l-3],artistas[l-2],artistas[l-1]] 
            #pos = [artistas[1],artistas[2],artistas[3],artistas[l-2],artistas[l-1],artistas[l]] 
            pos_inicial = lt.subList(analyzer['avistamientos'],1,5)
            pos_final = lt.subList(analyzer['avistamientos'],l-5,5)
            for ufos in lt.iterator(pos_inicial):
                a = [ufos["datetime"],ufos["city"],ufos["state"],ufos["country"],ufos["shape"],ufos["duration (seconds)"],ufos["duration (hours/min)"],ufos["comments"],ufos["date posted"],ufos["latitude"],ufos["longitude"]]
                d = []
                for i in a:
                    d.append(salto(i,ancho_max))
                x.add_row(d)
            for ufos in lt.iterator(pos_final):
                a = [ufos["datetime"],ufos["city"],ufos["state"],ufos["country"],ufos["shape"],ufos["duration (seconds)"],ufos["duration (hours/min)"],ufos["comments"],ufos["date posted"],ufos["latitude"],ufos["longitude"]]
                d = []
                for i in a:
                    d.append(salto(i,ancho_max))
                x.add_row(d)
            print(x) 

def salto(cad,lon): #texto muy largo 
	if len(cad)>lon:
		pos=lon-1
		for i in cad[lon-1:0:-1]:
			if i==" ":
				sal=cad[0:pos]+"\n"+salto(cad[pos+1:],lon)
				return sal
			pos=pos-1
		sal=cad[0:lon-1]+"\n"+salto(cad[lon-1:],lon)
		return sal
	else:
		return cad

def printufosdate(avist):
    x=PrettyTable()
    ancho=18
    #total=lt.size(analyzer["avistamientos"])
    #x.field_names = ["datetime","city","state","country","shape","duration (seconds)","duration (hours/min)","comments","date posted","latitude","longitude"]
    x.field_names = ["datetime","city","state","country","shape","duration (seconds)"]
    for evento in lt.iterator(avist):
            row= [evento["datetime"],evento["city"],evento["state"],evento["country"],evento["shape"],evento["duration (seconds)"]]
            adjrow=[]
            for elem in row:
                adjrow.append(salto(elem,ancho))
            x.add_row(adjrow) 
    print(x)

def printInitial(analyzer):
    initialDate0 = str(controller.minKey(analyzer['fechas'])) 
    total6 = controller.getAvistamientosByRangeForPrint3(analyzer, initialDate0, initialDate0)
    x = PrettyTable()
    x.field_names = ["date","count"]
    fila = [initialDate0,str(lt.size(total6))]
    x.add_row(fila)
    print(x)

def printInitial2(analyzer):
    maxduracion = str(controller.maxKey(analyzer['duracion'])) 
    total6 = controller.getAvistamientosByRangeForPrint4(analyzer, maxduracion, maxduracion)
    x = PrettyTable()
    x.field_names = ["duration (seconds)","count"]
    fila = [maxduracion,str(lt.size(total6))]
    x.add_row(fila)
    print(x)

def printInitial3(analyzer):
    maxduracion = str(controller.maxKey(analyzer['HH:MM'])) 
    total6 = controller.getAvistamientosByRangeForPrint5(analyzer, maxduracion, maxduracion)
    x = PrettyTable()
    x.field_names = ["time","count"]
    fila = [maxduracion,str(lt.size(total6))]
    x.add_row(fila)
    print(x)

def printmaxcity(analyzer):
    lista = om.keySet(analyzer['ciudades'])
    maxavista = 0
    maxcity = ''
    for city in lt.iterator(lista):
        map = om.get(analyzer['ciudades'],city)['value']
        initialDate = str(om.minKey(map))
        finalDate = str(om.maxKey(map))
        ciudades = controller.getAvistamientosByCity(analyzer,city,initialDate, finalDate)
        if ciudades > maxavista:
            maxavista = ciudades
            maxcity = city 
    print('La ciudad con mas avistamientos reportados es: ')
    x = PrettyTable()
    x.field_names = ["city","count"]
    fila = [maxcity,str(maxavista)]
    x.add_row(fila)
    print(x)

def printmap(centro,lista,listap):
    app = Flask(__name__)
    @app.route('/')

    def index():
        start_coords = (centro)
        folium_map = folium.Map(location=start_coords,
                            tiles="Stamen Terrain",
                            #min_lot=-109.05,
                            #max_lot=-103.00,
                            #min_lat=31.33,
                            #max_lat=37.00,
                            #max_bounds=True,
                            zoom_start = 9,
                            #max_zoom = 5,
                            #min_zoom =4,
                            width = '100%',
                            height = '100%') 
                            #zoom_control=False)
        for i in lt.iterator(lista):
            folium.Marker([float(i['latitude']),float(i['longitude'])],popup='<i>' + i['comments'] + '</i>').add_to(folium_map)
            folium.PolyLine(listap,color='red').add_to(folium_map)
        return folium_map._repr_html_()


    """"
    tooltip = "Click me!"

    folium.Marker(
    [45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
    ).add_to(folium_map)
    folium.Marker(
    [45.3311, -121.7113], popup="<b>Timberline Lodge</b>", tooltip=tooltip
    ).add_to(folium_map)
    """
    if __name__ == '__main__':
        app.run() 


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        cont = controller.init()
        controller.loadData(cont, ufosfile)
        print('Avistamientos cargados: ' + str(controller.ufosSize(cont)))
        printCargarDatos(cont)

    elif int(inputs[0]) == 1:
        print("\nBuscando avistamientos en una ciudad: ")
        ciudad = input("Ingrese el nombre de la ciudad: ")
        #print('Crimenes cargados: ' + str(controller.ufosSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont['ciudades'])))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont['ciudades'])))
        print('Hay ' + str(controller.indexSize(cont['ciudades'])) + ' donde se han presentando avistamientos')
        printmaxcity(cont)
        fechas = om.get(cont['ciudades'],ciudad)
        initialDate = str(controller.minKey(fechas['value'])) 
        finalDate = str(controller.maxKey(fechas['value']))
        #print('Menor Llave: ' + str(controller.minKey(fechas['value'])))
        #print('Mayor Llave: ' + str(controller.maxKey(fechas['value'])))
        ciudades = controller.getAvistamientosByCity(cont,ciudad,initialDate, finalDate)
        print('Hay ' + str(ciudades) + ' avistamientos en la ciudad de ' + ciudad)
        map = fechas['value']
        total6 = controller.getAvistamientosByRangeForPrint2(map, initialDate, finalDate)
        print('Los 3 primeros y 3 ultimos avistamientos son: ')
        printufosdate(total6)

    elif int(inputs[0]) == 2:
        print("\nBuscando avistamientos en el rango de duración: ")
        duracionmin = input("Ingrese la duración minima en segundos: ")
        duracionmax = input("Ingrese la duración maxima en segundos: ")
        duracion = controller.getAvistamientosByDuracion(cont,duracionmin,duracionmax)
        totalavistamientos = controller.getAvistamientosByRangeForPrint4(cont, duracionmin, duracionmax)
        print('Hay ' + str(om.size(cont['duracion'])) + ' diferentes duraciones en los avistamientos')
        print('El avistamiento mas largo es: ')
        printInitial2(cont)
        print('Hay ' + str(lt.size(totalavistamientos)) + ' avistamientos entre ' + duracionmin + ' y ' + duracionmax + ' segundos' )
        print('Los primeros 3 y ultimos 3 avistamientos en la duración dada son: ')
        if lt.size(totalavistamientos) < 7:
            total6 = totalavistamientos
        else:
            total6 = controller.concatlist(lt.subList(totalavistamientos,1,3),lt.subList(totalavistamientos,lt.size(totalavistamientos)-2,3))
        printufosdate(total6)

    elif int(inputs[0]) == 3:
        print("\nBuscando avistamientos en el rango de horas dadas: ")
        duracionmin = input("Ingrese el tiempo inicial de observación en formato HH:MM :  ")
        duracionmax = input("Ingrese el tiempo final de observación en formato HH:MM :  ")
        duracion = controller.getAvistamientosByHHMM(cont,duracionmin,duracionmax)
        totalavistamientos = controller.getAvistamientosByRangeForPrint5(cont, duracionmin + ':00', duracionmax + ':00')
        print('Hay ' + str(om.size(cont['duracion'])) + ' horas y minutos distintos de avistamientos')
        print(lt.size(om.keySet(cont['duracion'])))
        print('El avistamiento mas tardido es: ')
        printInitial3(cont)
        print('Hay ' + str(lt.size(totalavistamientos)) + ' avistamientos entre las ' + duracionmin + ' y las ' + duracionmax)
        print('Los primeros 3 y ultimos 3 avistamientos en el rango dado son: ')
        if lt.size(totalavistamientos) < 7:
            total6 = totalavistamientos
        else:
            total6 = controller.concatlist(lt.subList(totalavistamientos,1,3),lt.subList(totalavistamientos,lt.size(totalavistamientos)-2,3))
        printufosdate(total6)

    elif int(inputs[0]) == 4:
        print("\nBuscando avistamientos en un rango de fechas: ")
        initialDate = input("Fecha Inicial (YYYY-MM-DD): ")
        finalDate = input("Fecha Final (YYYY-MM-DD): ")
        total = controller.getAvistamientosByRange(cont, initialDate, finalDate)
        total6 = controller.getAvistamientosByRangeForPrint(cont, initialDate, finalDate)
        print('Hay ' + str(om.size(cont['fechas'])) + ' avistamientos con fechas distintas. ')
        print('El avistamiento mas antiguo es: ')
        printInitial(cont)
        print("\nTotal de avistamientos en el rango de fechas: " + str(total)) 
        print('Los 3 primeros y 3 ultimos avistamientos son: ')
        printufosdate(total6)

    elif int(inputs[0]) == 5:
        print("\nBuscando avistamientos en una zona geográfica: ")
        latitudemin = input("Ingrese la latitud minima con dos cifras decimales: ")
        latitudemax = input("Ingrese la latitud maxima con dos cifras decimales : ")
        while float(latitudemin) > float(latitudemax):
            print('Error en el rango de latitudes, asegurese de poner el valor min al inicio')
            latitudemin = input("Ingrese la latitud minima con dos cifras decimales: ")
            latitudemax = input("Ingrese la latitud maxima con dos cifras decimales : ")
        longitudemin = input("Ingrese la longitud minima con dos cifras decimales: ")
        longitudemax = input("Ingrese la longitud maxima con dos cifras decimales: ")
        while float(longitudemin) > float(longitudemax):
            print('Error en el rango de longitudes, asegurese de poner el valor min al inicio')
            longitudemin = input("Ingrese la longitud minima con dos cifras decimales: ")
            longitudemax = input("Ingrese la longitud maxima con dos cifras decimales : ")
        rango = controller.getAvistamientosByZnGeo(cont,longitudemin,longitudemax,latitudemin,latitudemax,)
        totalavistamientos = controller.getAvistamientosByRangeForPrint6(cont,longitudemin,longitudemax,latitudemin,latitudemax )
        print('Hay ' + str(lt.size(totalavistamientos)) + ' avistamientos entre las latitudes desde ' + latitudemin + ' hasta ' + latitudemax) 
        print('y las longitudes desde ' + longitudemin + ' hasta ' + longitudemax) 
        print('Los primeros 5 y ultimos 5 avistamientos en la duración dada son: ')
        if lt.size(totalavistamientos) < 11:
            total6 = totalavistamientos
        else:
            total6 = controller.concatlist(lt.subList(totalavistamientos,1,5),lt.subList(totalavistamientos,lt.size(totalavistamientos)-4,5))
        printufosdate(total6)

    elif int(inputs[0]) == 6:
        print("\nBuscando avistamientos en una zona geográfica: ")
        latitudemin = input("Ingrese la latitud minima con dos cifras decimales: ")
        latitudemax = input("Ingrese la latitud maxima con dos cifras decimales : ")
        while float(latitudemin) > float(latitudemax):
            print('Error en el rango de latitudes, asegurese de poner el valor min al inicio')
            latitudemin = input("Ingrese la latitud minima con dos cifras decimales: ")
            latitudemax = input("Ingrese la latitud maxima con dos cifras decimales : ")
        longitudemin = input("Ingrese la longitud minima con dos cifras decimales: ")
        longitudemax = input("Ingrese la longitud maxima con dos cifras decimales: ")
        while float(longitudemin) > float(longitudemax):
            print('Error en el rango de longitudes, asegurese de poner el valor min al inicio')
            longitudemin = input("Ingrese la longitud minima con dos cifras decimales: ")
            longitudemax = input("Ingrese la longitud maxima con dos cifras decimales : ")
        rango = controller.getAvistamientosByZnGeo(cont,longitudemin,longitudemax,latitudemin,latitudemax,)
        totalavistamientos = controller.getAvistamientosByRangeForPrint6(cont,longitudemin,longitudemax,latitudemin,latitudemax )
        print('Hay ' + str(lt.size(totalavistamientos)) + ' avistamientos entre las latitudes desde ' + latitudemin + ' hasta ' + latitudemax) 
        print('y las longitudes desde ' + longitudemin + ' hasta ' + longitudemax) 
        print('Los primeros 5 y ultimos 5 avistamientos en la duración dada son: ')
        if lt.size(totalavistamientos) < 11:
            total6 = totalavistamientos
        else:
            total6 = controller.concatlist(lt.subList(totalavistamientos,1,5),lt.subList(totalavistamientos,lt.size(totalavistamientos)-4,5))
        printufosdate(total6)

        centro = ((float(latitudemin) + float(latitudemax))/2,(float(longitudemin) + float(longitudemax))/2)
        print('Para visualizar el mapa con las observaciones siga el enlace que se genera a continuación: ')
        cuadrante = [(float(latitudemin),float(longitudemin)),(float(latitudemin),float(longitudemax)),(float(latitudemax),float(longitudemax)),(float(latitudemax),float(longitudemin)),(float(latitudemin),float(longitudemin))]
        printmap(centro,totalavistamientos,cuadrante)

    else:
        sys.exit(0)
sys.exit(0)
