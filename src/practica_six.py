import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import matplotlib.pyplot as plt

window = tk.Tk()
window.title("Archivos Excel")
window.geometry("400x300")

label_mesagge = tk.Label(window, text="")
label_mesagge.pack(pady=2)

# Variable global
df_global = None

def load_route():
    route_file = filedialog.askdirectory(title="Selecciona la carpeta con tus archivos Excel")
    if route_file:
        print(route_file)
        mensaje_exito = "Archivos cargados exitosamente."
        label_mesagge.config(text=mensaje_exito, fg="green")
        return route_file
    return None

def load_content_file():
    route_excel_files = load_route()
    if route_excel_files:
        files_excel = [os.path.join(route_excel_files, file) for file in os.listdir(route_excel_files) if file.endswith('.xlsx')]
        merge_data(files_excel)
    else:
        print("No se seleccionó ninguna carpeta.")

def merge_data(routes):
    try:
        for sheet in routes:
            df = pd.read_excel(sheet, sheet_name='datos', skiprows=0)
            df.columns = df.columns.str.replace('"', '').str.strip()
            print(f"Columnas disponibles en {sheet}: {df.columns}")
            columnas_deseadas = ['gestion', 'mes', 'Precipitacion', 'Temperatura Media', 'Humedad Relativa Media', 'Velocidad de Viento Media']

            if all(col in df.columns for col in columnas_deseadas):
                df_selected = df[columnas_deseadas]
                df_filtrado = filtrar_datos(df_selected)
                graficar_datos(df_filtrado)
            else:
                print(f"Las columnas esperadas no se encontraron en {sheet}")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def filtrar_datos(df):
    condiciones_ideales = {
        'Temperatura Media': (10, 20),
        'Humedad Relativa Media': (30, 60),
        'Precipitacion': (5, 15),
        'Velocidad de Viento Media': (1, 5)
    }

    df_filtrado = pd.DataFrame()
    for sensor, (min_val, max_val) in condiciones_ideales.items():
        if sensor in df.columns:
            filtro = (df[sensor] >= min_val) & (df[sensor] <= max_val)
            df_filtrado = pd.concat([df_filtrado, df[filtro]])

    if 'gestion' in df_filtrado.columns and 'mes' in df_filtrado.columns:
        df_filtrado['mes'] = df_filtrado['mes'].apply(lambda x: f"{int(x):02d}")
        df_filtrado = df_filtrado.sort_values(by=['gestion', 'mes'])
    return df_filtrado

# Función que genera 5 gráficos diferentes
def graficar_datos(df):
    if df.empty:
        print("No hay datos para graficar después de aplicar los filtros.")
        return

    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
    df_grouped = df.groupby('mes').mean()
    df_grouped = df_grouped.loc[(df_grouped.index >= 1) & (df_grouped.index <= 12)]

    # Gráfico 1: Temperatura Media por Mes
    plt.figure()
    plt.plot(df_grouped.index, df_grouped['Temperatura Media'], marker='o', color='blue')
    plt.xlabel('Mes')
    plt.ylabel('Temperatura Media (°C)')
    plt.title('Temperatura Media por Mes')
    plt.grid(True)
    plt.show()

    # Gráfico 2: Humedad Relativa por Mes
    plt.figure()
    plt.plot(df_grouped.index, df_grouped['Humedad Relativa Media'], marker='o', color='green')
    plt.xlabel('Mes')
    plt.ylabel('Humedad Relativa Media (%)')
    plt.title('Humedad Relativa Media por Mes')
    plt.grid(True)
    plt.show()

    # Gráfico 3: Precipitación por Mes
    plt.figure()
    plt.bar(df_grouped.index, df_grouped['Precipitacion'], color='cyan')
    plt.xlabel('Mes')
    plt.ylabel('Precipitación (mm)')
    plt.title('Precipitación por Mes')
    plt.grid(True)
    plt.show()

    # Gráfico 4: Velocidad del Viento por Mes
    plt.figure()
    plt.plot(df_grouped.index, df_grouped['Velocidad de Viento Media'], marker='o', color='red')
    plt.xlabel('Mes')
    plt.ylabel('Velocidad de Viento Media (m/s)')
    plt.title('Velocidad del Viento Media por Mes')
    plt.grid(True)
    plt.show()

    # Gráfico 5: Comparativa de todas las variables
    plt.figure()
    plt.plot(df_grouped.index, df_grouped['Temperatura Media'], label='Temperatura Media', marker='o', color='blue')
    plt.plot(df_grouped.index, df_grouped['Humedad Relativa Media'], label='Humedad Relativa Media', marker='o', color='green')
    plt.plot(df_grouped.index, df_grouped['Precipitacion'], label='Precipitación', marker='o', color='cyan')
    plt.plot(df_grouped.index, df_grouped['Velocidad de Viento Media'], label='Velocidad de Viento', marker='o', color='red')
    plt.xlabel('Mes')
    plt.ylabel('Promedio')
    plt.title('Comparativa de Variables por Mes')
    plt.legend()
    plt.grid(True)
    plt.show()

buttonData = tk.Button(window, text="Procesar datos Excel", command=load_content_file)
buttonData.pack(pady=30)

window.mainloop()
