import tkinter as tk 
from tkinter import filedialog 
import pandas as pd 
import os #libreria para manipular rutas
window = tk.Tk()
window.title("Archivos Excel")
window.geometry("400x300")#tamano de la ventana

label_mesagge = tk.Label(window , text="")
label_mesagge.pack(pady=2)

#variable global
df_global = None
#funcion cargar carpeta con archivos excel
def load_route():
    route_file = filedialog.askdirectory(title="Take your files excel")
    if route_file:
        print (route_file)
        mensaje_exito ="this file is loaded."
        label_mesagge.config(text=mensaje_exito, fg="green")
        return route_file
    return None

def load_content_file():
    route_excel_files = load_route()
    #os.path.join  = convina partes de la ruta de un archivo
    #dentro recibe multiples partes que se convinan para formar una ruta
    #en este caso recibe la ruta de la carpeta 
    #y el archivo es para cada archico dentro del directorio que tenemos
    #debe tomar el archivo que termine en .xlsx
    #y este retorna un array que contiene la ubicacion de cada archivo.xlsx
    if route_excel_files:
        files_excel = [os.path.join(route_excel_files, file) for file in os.listdir(route_excel_files) if file.endswith('.xlsx')]
        #print(f"Archivos en la carpeta: {os.listdir(route_excel_files)}")
        #print(f"Las rutas son: {archivos_excel}")
        merge_data(files_excel)
    else :
        print("No se seleccionó ninguna carpeta.")

def merge_data(routes):
    df_list = []
    try:
        #read_excel recibe los parametros :
        #1.-le pasamos la ruta
        #2.-atributo indica el nombre de la hoja que va leer
        #3.-Rango de columnas a analizar
        #4.-Rango de lineas que debera de saltar
        for sheet in routes:
            df = pd.read_excel(sheet, sheet_name='datos', skiprows=0)
            df.columns = df.columns.str.replace('"' , '').str.strip() 
            print(f"Columnas disponibles en {sheet}: {df.columns}")  
            # Columnas de las que necesitamos los datos
            columnas_deseadas = ['gestion', 'mes', 'estacion', 'Precipitacion' , 'Temperatura Media' , 'Humedad Relativa Media' , 'Velocidad de Viento Media' ]  

            #toma una columna de df.columns 
            #y ve si esta presente en las columnas que queremos
            if all(col in df.columns for col in columnas_deseadas):
                #df_selected es una nueva hoja con los datos de las columnas que queremos
                df_selected = df[columnas_deseadas]
                df_list.append(df_selected)
                print("esto es el filtrado de datos : ")
                print(df_selected)
            else:
                print(f"Las columnas esperadas no se encontraron en {sheet}")

        #tomar la lista que contiene el array de los datos del excel
        if df_list:
            #concatenar todo en un solo archivo final
            df_final = pd.concat(df_list, ignore_index=True)
            #nombre que se elija para guardar el archivo
            save_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")], title="Save Combined Excel File")
            if save_path:
                #toma la ruta de guardado , y guarda el archivo
                df_final.to_excel(save_path, index=False)
                print(f"Archivo combinado guardado en {save_path}")
            else:
                print("No se seleccionó una ruta para guardar el archivo.")
        else:
            print("No se encontraron datos para combinar.")
    except Exception as e:
        print(f"Error al leer el archivo {e}")

buttonData = tk.Button(window , text="Procesar datos Excel" , command=load_content_file)
buttonData.pack(pady=30)

window.mainloop()
