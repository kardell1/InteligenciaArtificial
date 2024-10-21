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

# Variable global para almacenar el DataFrame
df_global = pd.DataFrame()

# Función para cargar una carpeta con archivos Excel
def load_route():
    route_file = filedialog.askdirectory(title="Seleccione su carpeta de archivos Excel")
    if route_file:
        label_mesagge.config(text="Carpeta cargada con éxito", fg="green")
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
    global df_global
    try:
        df_list = []
        for sheet in routes:
            df = pd.read_excel(sheet, sheet_name='datos', skiprows=0)
            df.columns = df.columns.str.replace('"' , '').str.strip()
            columnas_deseadas = ['gestion', 'mes', 'Precipitacion' , 'Temperatura Media' , 'Humedad Relativa Media' , 'Velocidad de Viento Media']  
            if all(col in df.columns for col in columnas_deseadas):
                df_selected = df[columnas_deseadas]
                df_list.append(df_selected)
            else:
                print(f"Columnas faltantes en {sheet}")
        df_global = pd.concat(df_list, ignore_index=True)
        label_mesagge.config(text="Archivos combinados con éxito", fg="green")
        generar_graficos(df_global)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def generar_graficos(df):
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
    
    # 1. Gráfico de barras - Temperatura Media por Mes
    df_grouped_temp = df.groupby('mes').mean()
    plt.figure(figsize=(8, 5))
    plt.bar(df_grouped_temp.index, df_grouped_temp['Temperatura Media'], color='orange')
    plt.xlabel('Mes')
    plt.ylabel('Temperatura Media (°C)')
    plt.title('Temperatura Media por Mes')
    plt.xticks(range(1, 13))
    plt.show()

    # 2. Histograma - Distribución de Humedad Relativa Media
    plt.figure(figsize=(8, 5))
    plt.hist(df['Humedad Relativa Media'], bins=10, color='green', edgecolor='black')
    plt.xlabel('Humedad Relativa Media (%)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de la Humedad Relativa Media')
    plt.grid(True)
    plt.show()

    # 3. Gráfico de líneas - Velocidad de Viento Media por Mes
    plt.figure(figsize=(8, 5))
    plt.plot(df_grouped_temp.index, df_grouped_temp['Velocidad de Viento Media'], marker='o', linestyle='-', color='blue')
    plt.xlabel('Mes')
    plt.ylabel('Velocidad de Viento Media (m/s)')
    plt.title('Velocidad de Viento Media por Mes')
    plt.xticks(range(1, 13))
    plt.grid(True)
    plt.show()

    # 4. Gráfico de dispersión - Precipitación vs Temperatura Media
    plt.figure(figsize=(8, 5))
    plt.scatter(df['Precipitacion'], df['Temperatura Media'], color='red')
    plt.xlabel('Precipitación (mm)')
    plt.ylabel('Temperatura Media (°C)')
    plt.title('Precipitación vs Temperatura Media')
    plt.grid(True)
    plt.show()

    # 5. Gráfico de caja (boxplot) - Distribución de Temperatura Media por Mes
    plt.figure(figsize=(8, 5))
    df.boxplot(column='Temperatura Media', by='mes', grid=False)
    plt.xlabel('Mes')
    plt.ylabel('Temperatura Media (°C)')
    plt.title('Distribución de Temperatura Media por Mes')
    plt.suptitle('')  # Eliminar el título automático del boxplot
    plt.show()

buttonData = tk.Button(window, text="Procesar datos Excel", command=load_content_file)
buttonData.pack(pady=30)

window.mainloop()
