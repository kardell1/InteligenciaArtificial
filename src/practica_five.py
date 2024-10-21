import tkinter as tk 
from tkinter import filedialog 
import pandas as pd 
import os #libreria para manipular rutas
import matplotlib.pyplot as plt
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
            columnas_deseadas = ['gestion', 'mes', 'Precipitacion' , 'Temperatura Media' , 'Humedad Relativa Media' , 'Velocidad de Viento Media' ]  

            #toma una columna de df.columns 
            #y ve si esta presente en las columnas que queremos
            if all(col in df.columns for col in columnas_deseadas):
                #df_selected es una nueva hoja con los datos de las columnas que queremos
                df_selected = df[columnas_deseadas]
                
                df_filtrado = filtrar_datos(df_selected)
                #print(f"Datos seleccionados de {sheet}:")
                graficar_datos(df_filtrado)
                #print(df_selected)  # Muestra el DataFrame seleccionado
                print("esto es el filtrado de datos : ")
                print(df_filtrado)
            else:
                print(f"Las columnas esperadas no se encontraron en {sheet}")
    except Exception as e:
        print(f"Error al leer el archivo {e}")


def filtrar_datos(df):
    # Definir las condiciones ideales para cada sensor
    condiciones_ideales = {
        'Temperatura Media': (10, 20),  # Rango ideal de temperatura
        'Humedad Relativa Media': (30, 60),  # Rango ideal de humedad
        'Precipitación': (5, 15),  # Rango ideal de precipitación
        'Velocidad de Viento Media': (1, 5)  # Rango ideal de velocidad de viento
    }

    # Filtrar datos que cumplan las condiciones ideales
    df_filtrado = pd.DataFrame()  # DataFrame vacío para almacenar los datos que cumplen las condiciones
    for sensor, (min_val, max_val) in condiciones_ideales.items():
        if sensor in df.columns:
            # Seleccionar solo los datos que cumplen las condiciones para este sensor
            filtro = (df[sensor] >= min_val) & (df[sensor] <= max_val)
            df_filtrado = pd.concat([df_filtrado, df[filtro]])

    if 'gestion' in df_filtrado.columns and 'mes' in df_filtrado.columns:
        #convierte un digito en dos digitos
        df_filtrado['mes'] = df_filtrado['mes'].apply(lambda x: f"{int(x):02d}")
        #ordenar en base a esas columnas
        df_filtrado = df_filtrado.sort_values(by=['gestion', 'mes'])
    return df_filtrado
def graficar_datos(df):
    # Asegurarse de que hay datos después de aplicar los filtros
    if df.empty:
        print("No hay datos para graficar después de aplicar los filtros.")
        return
    
    # Convertir la columna 'mes' a tipo numérico, por si está en formato string
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')

    # Agrupar los datos por mes y calcular el promedio de la columna 'Temperatura Media'
    df_grouped = df.groupby('mes').mean()

    # Asegurarse de que los meses están entre 1 y 12
    df_grouped = df_grouped.loc[(df_grouped.index >= 1) & (df_grouped.index <= 12)]

    # Graficar la temperatura media por mes
    plt.plot(df_grouped.index, df_grouped['Temperatura Media'], marker='o', linestyle='-', color='blue')

    # Etiquetas de los ejes
    plt.xlabel('Mes')
    plt.ylabel('Temperatura Media (°C)')
    plt.title('Temperatura Media a lo largo de los Meses')
    
    # Mostrar la gráfica
    plt.xticks(range(1, 13))  # Asegurar que el eje X tenga los meses de 1 a 12
    plt.grid(True)
    plt.show()

buttonData = tk.Button(window , text="Procesar datos Excel" , command=load_content_file)
buttonData.pack(pady=30)


#funcion de convinar varios campos de todos los archivos excel




window.mainloop()
