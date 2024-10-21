import tkinter as tk 
from tkinter import filedialog 
import pandas as pd 

window = tk.Tk()
window.title("Archivos Excel")
window.geometry("400x300")#tamano de la ventana

label_mesagge = tk.Label(window , text="")
label_mesagge.pack(pady=2)
#variable global
df_global = None
def load_file():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", ".xlsx")])
    if ruta_archivo:
        try:
            #es el nombre de la hoja que tiene ese archivo que estamos cargando 
            df = pd.read_excel(ruta_archivo,"PREMIO_ITEM_OFICINA_CLIENTE")
            mensaje_exito ="El archivo ha sido cargado correctamente."
            label_mesagge.config(text=mensaje_exito, fg="green")
            #desde aqui especificar que hacer con la informacion
            #necesita ser llamado por global para saber que es global y no local
            
            global df_global
            df_global = df
            #mostramos por consola , los datos del excel 
            print(df_global)
        except Exception as e:
            # Si ocurre un error, lo mostramos
            mensaje_error = f"Error al cargar el archivo: {e}"
            label_mesagge.config(text=mensaje_error, fg="red")


buttonLoad = tk.Button(window , text="Load Excel" , command=load_file)
#el commando recibe el nombre , pero no lleva ()
buttonLoad.pack(pady=10)


window.mainloop()