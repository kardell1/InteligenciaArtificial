import tkinter as tk 
from tkinter import filedialog 
import pandas as pd 
import os 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Configuración de la ventana
window = tk.Tk()
window.title("Archivos Excel")
window.geometry("400x300")  # Tamaño de la ventana

label_message = tk.Label(window, text="")
label_message.pack(pady=2)

# Variable global
df_global = None

# Función para cargar la carpeta con archivos Excel
def load_route():
    route_file = filedialog.askdirectory(title="Take your files excel")
    if route_file:
        mensaje_exito = "This file is loaded."
        label_message.config(text=mensaje_exito, fg="green")
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
    df_list = []
    try:
        for sheet in routes:
            df = pd.read_excel(sheet, sheet_name='datos', skiprows=0)
            df.columns = df.columns.str.replace('"', '').str.strip() 
            print(f"Columnas disponibles en {sheet}: {df.columns}")  
            # Columnas deseadas
            columnas_deseadas = ['gestion', 'mes', 'estacion', 'Precipitacion', 'Temperatura Media', 'Humedad Relativa Media', 'Velocidad de Viento Media']

            if all(col in df.columns for col in columnas_deseadas):
                df_selected = df[columnas_deseadas]

                df_selected = df_selected.fillna(1)  # Reemplazar NaN con 1
                df_selected = df_selected.replace(0, 1)  # Reemplazar 0 con 1
                
                df_list.append(df_selected)
                print("Esto es el filtrado de datos:")
                print(df_selected)
            else:
                print(f"Las columnas esperadas no se encontraron en {sheet}")

    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def perform_linear_regression(df):
    # Preparar los datos para la regresión
    X = df[['Precipitacion']]  # Cambiar a la variable independiente deseada
    y = df['Temperatura Media']  # Cambiar a la variable dependiente deseada

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo de regresión lineal
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Realizar predicciones
    df['Predicciones'] = model.predict(X)

    # Graficar resultados
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Precipitacion'], df['Temperatura Media'], color='blue', label='Temperatura Real')
    plt.plot(df['Precipitacion'], df['Predicciones'], color='red', label='Predicciones')
    plt.xlabel('Precipitacion')
    plt.ylabel('Temperatura Media')
    plt.legend()
    plt.title('Temperatura Real vs Predicciones')
    plt.show()

# Botón para procesar datos Excel
buttonData = tk.Button(window, text="Procesar datos Excel", command=load_content_file)
buttonData.pack(pady=30)

window.mainloop()
