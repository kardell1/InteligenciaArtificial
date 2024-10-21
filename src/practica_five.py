import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

window = tk.Tk()
window.title("Archivos Excel")
window.geometry("400x300")  # tamaño de la ventana

label_mesagge = tk.Label(window, text="")
label_mesagge.pack(pady=2)

# Variable global para almacenar el DataFrame combinado
df_global = None

# Función para cargar carpeta con archivos Excel
def load_route():
    route_file = filedialog.askdirectory(title="Selecciona la carpeta con archivos Excel")
    if route_file:
        mensaje_exito = "Carpeta cargada con éxito."
        label_mesagge.config(text=mensaje_exito, fg="green")
        return route_file
    return None

# Función para cargar el contenido de los archivos Excel
def load_content_file():
    route_excel_files = load_route()
    if route_excel_files:
        files_excel = [os.path.join(route_excel_files, file) for file in os.listdir(route_excel_files) if file.endswith('.xlsx')]
        merge_data(files_excel)
    else:
        print("No se seleccionó ninguna carpeta.")

# Función para combinar datos de varios archivos Excel en un DataFrame
def merge_data(routes):
    global df_global
    try:
        data_frames = []
        for sheet in routes:
            df = pd.read_excel(sheet, sheet_name='datos', skiprows=0)
            df.columns = df.columns.str.replace('"', '').str.strip()
            columnas_deseadas = ['gestion', 'mes', 'Precipitacion', 'Temperatura Media', 'Humedad Relativa Media', 'Velocidad de Viento Media']
            
            if all(col in df.columns for col in columnas_deseadas):
                df_selected = df[columnas_deseadas]
                data_frames.append(df_selected)
            else:
                print(f"Columnas esperadas no encontradas en {sheet}")

        if data_frames:
            df_global = pd.concat(data_frames, ignore_index=True)
            df_global.dropna(inplace=True)  # Eliminar filas con valores nulos
            procesar_modelos(df_global)
        else:
            print("No se encontraron datos para procesar.")

    except Exception as e:
        print(f"Error al leer los archivos: {e}")

# Función para procesar los datos y entrenar modelos predictivos
def procesar_modelos(df):
    # Separar las características (X) y la variable objetivo (y)
    X = df[['Precipitacion', 'Temperatura Media', 'Humedad Relativa Media', 'Velocidad de Viento Media']]
    y = df['Temperatura Media']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definir los modelos
    modelos = [
        LinearRegression(),
        DecisionTreeRegressor(),
        RandomForestRegressor()
    ]
    
    nombres_modelos = ['Linear Regression', 'Decision Tree', 'Random Forest']

    mejor = [0.0, 0.0, 0.0]
    cont = 0

    for modelo in modelos:
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mse_redondeado = round(mse, 2)
        print(f"Modelo: {nombres_modelos[cont]}, MSE: {mse_redondeado:.1f}")

        if cont == 0 or mse_redondeado < mejor[1]:
            mejor = [cont, mse_redondeado]

        cont += 1 

    print(f"El mejor modelo es: {nombres_modelos[int(mejor[0])]} con un MSE de {mejor[1]:.1f}")

buttonData = tk.Button(window, text="Procesar datos Excel", command=load_content_file)
buttonData.pack(pady=30)

window.mainloop()

