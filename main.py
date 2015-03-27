#! /usr/bin/env python3
## coding: utf-8
#####################################################################
#          _____         _   _               _   _                  #
#         | __  |___ ___| |_| |_ ___ ___ ___| |_|_|___ ___          #
#         | __ -| .'|  _| '_|  _|  _| .'|  _| '_| |   | . |         #
#         |_____|__,|___|_,_|_| |_| |__,|___|_,_|_|_|_|_  |         #
#                                                     |___|         #
#                                                                   #
#          __        _           _     _   _                        #
#         |  |   ___| |_ _ _ ___|_|___| |_| |_                      #
#         |  |__| .'| . | | |  _| |   |  _|   |                     #
#         |_____|__,|___|_  |_| |_|_|_|_| |_|_|                     #
#                       |___|                                       #
#                                                                   #
#          _____     _                                              #
#         |   __|___| |_ _ ___ ___                                  #
#         |__   | . | | | | -_|  _|                                 #
#         |_____|___|_|\_/|___|_|                                   #
#                                                                   #
#####################################################################
#                                                                   #
#       Author:                                                     #
#               Diego Rasero    diegolo.r8 (at) gmail (dot) com     #
#                                                                   #
#####################################################################
#                                                                   #
#       License:                                                    #
#               Copyright 2015 under license GPL v2.0               #
#                                                                   #
#####################################################################

from tkinter import *

import labmap
from nodo import Node

import time
from argparse import ArgumentParser

def main():
	argp = ArgumentParser(
	prog='Backtracking labyrinth solver',
	usage="python main.py -h",												

	description='Tool for solving, visualize and generate mazes.',
	epilog='Copyright 2015 Diego Rasero (diegolo.r8 (at) gmail (dot) com) under license GPL v2.0',)

	
	## Aspecto

		# Dimensiones ventana
	argp.add_argument('--height', dest='h', type=int, help="window height in pixels", default=600)
	argp.add_argument('--width', dest='w', type=int, help="window width in pixels", default=600)
		# Full Screen
	argp.add_argument('-f', '--fullscreen', action='store_true', dest='full', help="Enable fullscreen mode")

	
	
	## Comportamiento

		# Solo visualizar un mapa
	argp.add_argument('-v', '--view', dest='v', action='store_true', help="only view map, do not solve it") 

		# Flag exportar ps
	argp.add_argument('-ps', dest='ps', action='store_true', help="Export the maze to postscript.")

		# Modo salvapantallas (pantalla completa + modo bucle infinito)
	argp.add_argument('--screensaver', dest='screensaver',action='store_true', help="Screensaver mode")

		# Modo bucle infinito
	argp.add_argument('--loop', dest='loop', action='store_true', help="Infinite loop mode.") 

		# Flag Realentizar animación
		# tiempo de retraso
	argp.add_argument('-t', dest='t', type=float, help="timelapse", default=0)
		# Cargar mapa y nombre del mapa (si esta vacio no carga)
	argp.add_argument('-i', '--input', dest='input', type=str, help="Name of the input map", default="")
		# Guardar mapa
	argp.add_argument('-o', '--output', dest='out', type=str, help="Name of the output map and solution for the maze", default="tmp")

		# Verbose
	argp.add_argument('-V', '--verbose', action='store_true', dest='verbose', help="Prints extra information about the process")



	## Generador de mapas
		# Dimensiones del laberinto
	argp.add_argument('-rh', dest='rh', type=int, help="high number of rectangles", default=30)
	argp.add_argument('-rw', dest='rw', type=int, help="wide number of rectangles", default=30)
	argp.add_argument('--exits', dest='exits', type=int, help="number of exits of the generated maze", default=1)
	argp.add_argument('--ratio', dest='ratio', type=float, help="ratio of walls", default=1.0/3)

		# Colores
			# Paredes
			# Pasillos
			# Inicio
			# Finales
			# Solución

			# Ruta
			# Incremento de color
			# Flag Cambio de color		

	argp.add_argument('--wallcolor', dest='wc', type=str, help="Wall color", default="#1c1c1c")
	argp.add_argument('--corridorcolor', dest='cc', type=str, help="Corridor color", default="#ffffff")
	argp.add_argument('--solutioncolor', dest='sc', type=str, help="Corridor color", default="#a2f73a")
	argp.add_argument('--startcolor', dest='stc', type=str, help="Corridor color", default="#ff44ff")
	argp.add_argument('--exitcolor', dest='ec', type=str, help="Corridor color", default="#44ff44")

	argp.add_argument('--pathcolor', dest='pc', type=str, help="Path color", default="#656666")
	argp.add_argument('-pi', dest='pi', type=int, help="path increment color", default=65536)
	argp.add_argument('-pch', dest='pch', action='store_false', help="do not change path color", default=True)
	args = argp.parse_args()
	

	# Variables de configuración Se mantienen como punteros a args, debido a que puede que introduzca la configuración mediante un archivo de texto.



	# aspecto
	color_pared=args.wc
	color_pasillo=args.cc
	color_sol=args.sc
	color_start=args.stc
	color_exit=args.ec

	color_ruta=args.pc
	# color de ruta
	increment=args.pi
	color_change=args.pch

	# comportamiento
	steps=bool(args.t)
	step_time=args.t

	load=bool(args.input)
	lab_name=args.input

	export=args.ps

	loop=args.loop
	view=args.v
	verbose=args.verbose

	# generar mapa
	lab_w=args.rw
	lab_h=args.rh
	lab_exits=args.exits
	lab_ratio=args.ratio
	lab_outname=args.out


	# tamaño del canvas
	c_w = args.w
	c_h = args.h


	#### TK 


	# Crea ventana.
	master = Tk()
	master.title("Backtracking labyrinth solver")
	img = PhotoImage(file='icon.gif')
	master.tk.call('wm', 'iconphoto', master._w, img)
	master.resizable(0,0)



	# Fullscreen y modo screensaver
	if args.screensaver or args.full:
		master.attributes("-fullscreen", True)
		c_w=master.winfo_screenwidth()
		c_h=height=master.winfo_screenheight()
		if args.screensaver: loop=True

	# Inicializa el canvas
	w = Canvas(master, width=c_w, height=c_h,bg=color_pasillo)
	w.pack()
	
	####
	count=""
	if loop: count=1

	while 1:
		solve( 	
				master, w, verbose,

				load, lab_name, view, export,

				c_w, c_h,	lab_w, lab_h, lab_exits, lab_ratio, lab_outname+str(count),

				color_pasillo, color_pared, color_sol,color_exit,color_start,
				color_ruta, color_change,increment,

				step_time,steps

			)
		if not loop: break
		count+=1

	# Cargar laberinto y resolver.
	mainloop() # mantiene la ventana abierta hasta que el usuario la cierre.


##########################

def solve( 	
				master, w, verbose,

				load, lab_name, view, export,

				c_w, c_h,	lab_w, lab_h, lab_exits, lab_ratio, lab_outname,

				color_pasillo, color_pared, color_sol,color_exit,color_start,
				color_ruta, color_change,increment,

				step_time,steps
):
	"""
		Dibuja el proceso de resolución del laberinto.
	"""
	# Carga laberinto
	if load:
		laberinto=labmap.load(lab_name)
	else:
		laberinto=labmap.laberinto(lab_w,lab_h,lab_exits,lab_ratio)
		labmap.save(lab_outname+".map",laberinto)

	solved=False
	# tamaño del mapa en unidades discretas
	m_w=len(laberinto[0])
	m_h=len(laberinto)
	# Calculo de la unidad proporcional al tamaño del canvas
	u_w = c_w / m_w # Tamaño del lienzo entre tamaño del mapa
	u_h = c_h / m_h

	def draw_rect(pos,color):
		w.create_rectangle(pos[0]*u_w , pos[1]*u_h, (pos[0]+1)*u_w, (pos[1]+1)*u_h, fill=color,width=0)

	def draw_lab(lab):
		"""
			Dibuja el laberinto
		"""
		for y in range(m_h):
			for x in range(m_w):
				if (lab[y][x] == '#'):
					draw_rect((x,y),color_pared)
				#elif (lab[y][x] == '.'):      # pintar los huecos consume recursos
				#	draw_rect((x,y),color_pasillo)
				elif (lab[y][x] == 'e'):				
					draw_rect((x,y),color_exit)
				elif (lab[y][x] == 's'):				
					draw_rect((x,y),color_start)
					start=(x,y)
		return start



	# Limpia el canvas
	w.delete(ALL)

	# Dibuja el laberinto en el canvas y retorna el punto de inicio.
	start=draw_lab(laberinto)
	master.update()
	
	if not view: # no modo visualizar

		# Marca para calcular el tiempo en resolver
		t1=time.time()

		arbol=Node(None,start)

		aux=arbol
		aux.calcula_caminos(laberinto)
		if verbose: print("[Verbose] Start point: "+str(aux))

		if not aux.sig:
			solved=True
			sol=[]
			print("\tThe maze don't have solution, "+str(time.time()-t1)+" seconds")	
		try:
			while not solved:
				if aux.ramas():
					aux=aux.bajar()
					aux.calcula_caminos(laberinto)
					if verbose: print("[Verbose] Down to: "+str(aux))

					if steps: time.sleep(step_time) # pausa para permitir observar el comportamiento del algoritmo

					if aux.soy_salida(laberinto):
					
						solved=True
						sol=aux.get_sol()
						print("\tSolved in "+str(time.time()-t1)+" seconds")
					else:
					
						if color_change: # suma incremento en decimal al color
							color_ruta="#"+("00000"+ str( hex( (eval("0x"+color_ruta[1:]) +increment )%16777215  )  )[2:])[-6:] 
							if verbose: print("[Verbose] Path color changed to: "+color_ruta)
						draw_rect(aux.coord ,color_ruta) # dibuja el nodo
						if verbose: print("[Verbose] Drawing point")
						master.update() 
				else:
					aux=aux.subir()
					if verbose: print("[Verbose] Backtraking to: "+str(aux))
					if aux==None:
						solved=True
						sol=[]
						print("\tThe maze don't have solution, "+str(time.time()-t1)+" seconds")			
	
			for c in sol[1:-1]: # dibujar solución
				draw_rect(c,color_sol) # redibuja solución.
				master.update() 


			if export:
				if verbose: print("[Verbose] Exporting to postcript")
				w.postscript(file=lab_outname+".ps", colormode='color') # Guarda solución como postscript
				print("\tExported to "+lab_outname+".ps")

		except:
			pass

if __name__== "__main__":
    main()
