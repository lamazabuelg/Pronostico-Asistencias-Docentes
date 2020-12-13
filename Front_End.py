from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
import pandas as pd

data_pronosticos = pd.read_csv("https://gist.github.com/FabianTriana/d0f4d2247fc2db6b553816f016333a93/raw/Pronostico_2021.csv")
data_pronosticos["Fecha"] = pd.to_datetime(data_pronosticos["Fecha"])
data_pronosticos = data_pronosticos[data_pronosticos["Fecha"] >= "Jan 1, 2017"]
data_pronosticos.reset_index(inplace = True, drop = True)
fechas_pronosticos = tuple(list(data_pronosticos["Fecha"].astype(str).unique()))

probabilidades_historicas = pd.read_csv("https://gist.github.com/FabianTriana/9581eaeb13110f3206e541f065d994ce/raw/probabilidades_historicas.csv")

dias = {"1": "lunes", "2": "martes", "3": "miércoles", "4": "jueves", "5": "viernes", "6": "sábado"}


ventana = Tk()
ventana.geometry("500x500")
ventana.title("Pronóstico Asistencias")
ico = Image.open(urllib.request.urlopen("https://pbs.twimg.com/profile_images/1130896403805478912/1VmG0ZEr_400x400.png"))
photo = ImageTk.PhotoImage(ico)
ventana.wm_iconphoto(False, photo)

imagen_logo = ImageTk.PhotoImage(ico.resize((140,70)))
imagen = Label(ventana, image = imagen_logo)
imagen.pack()

titulo = Label(ventana, 
	text = "Pronóstico de Asistencias Docentes", 
	fg = "blue", 
	font = (18))
titulo.pack()

enunciado_dia = Label(ventana, 
	text = "Ingrese la fecha en formato yyy/mm/dd")
enunciado_dia.pack()

combo = ttk.Combobox(ventana)
combo["values"] = fechas_pronosticos
combo.pack()


enunciado_asistencias = Label(ventana, 
	text = "El número de asistencias estimadas es: ")
enunciado_asistencias.pack()

numero_asistencias = Label(ventana)
numero_asistencias.pack()

enunciado_software = Label(ventana, text = "Las probabilidades (basadas en información histórica) son:")
enunciado_software.pack()
probabilidades_software = Label(ventana)
probabilidades_software.pack()


def calcular_numero_asistencias():
	la_fecha = combo.get()
	el_pronostico = data_pronosticos[data_pronosticos["Fecha"] == la_fecha]["Respuesta"].values
	el_dia_de_la_semana = str(data_pronosticos[data_pronosticos["Fecha"] == la_fecha]["Dia de la semana"].values[0])
	el_dia_de_la_semana = dias[str(el_dia_de_la_semana)]
	la_semana_del_semestre = data_pronosticos[data_pronosticos["Fecha"] == la_fecha]["Semana del semestre"].values[0]
	if el_pronostico == 0:
		numero_asistencias["text"] = "Se estiman 2 o menos asistencias"
	elif el_pronostico == 1:
		numero_asistencias["text"] = "Se estiman más de dos asistencias"
	else:
		numero_asistencias["text"] = "No sabemos cuántas asistencias se estiman"
	referencia = probabilidades_historicas[(probabilidades_historicas["Día de la semana"] == el_dia_de_la_semana) & (probabilidades_historicas["Semana del semestre"]==la_semana_del_semestre)]
	la_info = ""
	for index, row in referencia.iterrows():
		programa = row["Software"]
		probabilidad = str(round(row["Probabilidad"]*100,2))+"%"
		nueva_info = programa+" "+ probabilidad + "\n"
		la_info = la_info + nueva_info
	probabilidades_software["text"] = la_info

boton = Button(ventana, text = "Calcular", 
	command = calcular_numero_asistencias)
boton.pack()

ventana.mainloop()