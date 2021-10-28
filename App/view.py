"""
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
    x.field_names = ["datetime","city","country","shape","duration (seconds)"]
    for evento in lt.iterator(avist):
            row= [evento["datetime"],evento["city"],evento["country"],evento["shape"],evento["duration (seconds)"]]
            adjrow=[]
            for elem in row:
                adjrow.append(salto(elem,ancho))
            x.add_row(adjrow) 
    print(x)



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
        fechas = om.get(cont['ciudades'],ciudad)
        initialDate = str(controller.minKey(fechas['value']))
        finalDate = str(controller.maxKey(fechas['value']))
        #print('Menor Llave: ' + str(controller.minKey(fechas['value'])))
        #print('Mayor Llave: ' + str(controller.maxKey(fechas['value'])))
        map = fechas['value']
        total6 = controller.getAvistamientosByRangeForPrint2(map, initialDate, finalDate)
        printufosdate(total6)


    elif int(inputs[0]) == 4:
        print("\nBuscando avistamientos en un rango de fechas: ")
        initialDate = input("Fecha Inicial (YYYY-MM-DD): ")
        finalDate = input("Fecha Final (YYYY-MM-DD): ")
        total = controller.getAvistamientosByRange(cont, initialDate, finalDate)
        total6 = controller.getAvistamientosByRangeForPrint(cont, initialDate, finalDate)
        print("\nTotal de avistamientos en el rango de fechas: " + str(total))
        printufosdate(total6)

    else:
        sys.exit(0)
sys.exit(0)
