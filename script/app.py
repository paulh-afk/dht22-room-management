import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from utils import csvfile_to_datas, add_data, get_dht_info
from time import sleep
# from PIL import Image, ImageTk

import socket
import netifaces as ni

INTERVAL_SECONDES = 8
TOLERANCE_ERREUR = 10

datas = csvfile_to_datas()

root = tk.Tk()
root.title('Données sonde')

root.attributes("-fullscreen", True)

label_tempeture = tk.Label(root, text='Température')
label_tempeture.config(font=('Roboto', 35))
label_tempeture.grid(row=0, column=0, pady=50, padx=50)

label_humidity = tk.Label(root, text='Humidité')
label_humidity.config(font=('Roboto', 35))
label_humidity.grid(row=0, column=1, pady=50, padx=50)

temperature_lab = tk.Label(root)
temperature_lab.config(font=('Roboto', 35))
temperature_lab.grid(row=1, column=0, pady=50, padx=50)

humidity_lab = tk.Label(root)
humidity_lab.config(font=('Roboto', 35))
humidity_lab.grid(row=1, column=1, pady=50, padx=50)

def is_network_connected():
    try:
        gws = ni.gateways()
        gateway = gws['default'][ni.AF_INET][0]
        
        socket.gethostbyaddr(gateway)
    except:
        messagebox.showwarning('Non connecté à un réseau', 'Vérifier que le Raspberry est bien connecté au réseau!')

def close():
    root.destroy()
    
def update_csv():
    count = 0
    while True:
        dht_info = get_dht_info()
        
        if count == TOLERANCE_ERREUR:
            messagebox.showwarning('Erreur de lecture des données',
                                   'Vérifier que le capteur est bien branché ' + \
                                   'ou que vous possédez bien les droits!')
            count = 0  

        # Gestion RuntimeError
        if dht_info is None:
            sleep(1.5)
            count += 1
            continue

        add_data(dht_info['temperature'], dht_info['humidity'], 15)
        break 

def update_graph(): 
    x = [data['horodatage'].strftime('%M:%S') for data in datas]

    y1 = [float(data['temperature']) for data in datas]
    y2 = [float(data['humidite']) for data in datas]    

    global graph1
    global graph2

    graph2.clear()
    graph1.clear()
    
    # TODO affichage ordonnées 0 à 1
    graph2 = graph1.twinx()

    graph1.set_ylabel('Température en °C', color='tab:red')
    graph1.tick_params(axis='y', labelcolor='tab:red')
    graph1.plot(x, y1, color='tab:red')
    
    graph2.set_ylabel('Humdité relative en %', color='tab:blue')
    graph2.tick_params(axis='y', labelcolor='tab:blue')
    graph2.plot(x, y2, color='tab:blue')

    fig.tight_layout()
    
    canvas.draw()

def open_new_window():
    new_window = tk.Toplevel(root)

    new_window.title('')
    new_window.geometry('400x600')

    tk.Label(new_window, text='Hello, world!')

def update():
    global datas 
    datas = csvfile_to_datas()
    
    # temperature_lab.config(fg='black')
    # humidity_lab.config(fg='black')
    
    # sleep(0.5)
    
    if len(datas) != 0:
        temperature = datas[-1].get('temperature')
        humidity = datas[-1].get('humidite')
        
        is_network_connected()
        update_csv()
        update_graph()
    else:
        temperature = '-'
        humidity = '-'

    if type(temperature) is float and temperature > 30:
        temperature_lab.config(fg='red')
    
    if type(humidity) is float and humidity > 70:
        humidity_lab.config(fg='red')

    temperature_lab['text'] = str(temperature) + " °C"
    humidity_lab['text'] = str(humidity) + " %"

    root.after(INTERVAL_SECONDES * 1000, update)


fig = Figure(figsize=(9, 3), dpi=150)

graph1 = fig.add_subplot(111)
graph1.set_ylabel('Température en °C', color='tab:red')

graph2 = graph1.twinx()
graph2.set_ylabel('Humdité relative en %', color='tab:blue')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=3, columnspan=2, pady=50, padx=50)

# btn = tk.Button(root, text='Ouvrir les paramètres', command=open_new_window)
# btn.grid(row=2, columnspan=2)

root.bind('<KeyRelease-F11>', lambda _: close())

update()
root.mainloop()
