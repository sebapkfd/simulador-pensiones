import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from calculos import simulacion
from calculos import analisis

def simular():
    # Obtiene las variables ingresadas en el formulario
    sexo = str(gen_var.get())
    edad = entry_edad.get()
    ahorro_afp = entry_ahorros_afp.get()
    ahorro_apv = entry_ahorros_apv.get()
    afp = str(var_afp.get())
    fondo = str(var_fondo.get())
    sueldo_est = entry_sueldo.get()
    apv_est = entry_vol.get()

    # Comprueba que esten correctamente ingresadas, en caso de error manda una alerta
    if edad.isnumeric() is False or ahorro_afp.isnumeric() is False or ahorro_apv.isnumeric() is False:
        mensaje('Llene los campos con valores válidos')
        return
    elif sueldo_est.isnumeric() is False or apv_est.isnumeric() is False:
        mensaje('Llene los campos con valores válidos')
        return

    # Se retorna una lista con: [monto_total_simulado, pension_simulada]
    # En caso de error, la lista es: [None, mensaje_de_error]
    result = simulacion(int(ahorro_afp), afp, fondo, int(edad), int(sueldo_est), sexo, int(ahorro_apv), int(apv_est))

    # Si se envían valores fuera de rango, se muestra una alerta, se usa la lista de la línea 27
    if result[0] is None:
        mensaje(result[1])
        return
    
    # Muestra de resultados
    resultado = 'Monto total: ' + str(result[0]) + '\n Pensión: ' + str(result[1])
    mensaje(resultado, 'Monto calculado')

def analizar():
    # Obtiene las variables ingresadas en el formulario
    sexo = str(gen_var.get())
    edad = entry_edad.get()
    ahorro_afp = entry_ahorros_afp.get()
    ahorro_apv = entry_ahorros_apv.get()
    afp = str(var_afp.get())
    fondo = str(var_fondo.get())
    sueldo_est = entry_sueldo.get()
    apv_est = entry_vol.get()
    pension_deseada = entry_pension.get()

    # Comprueba que esten correctamente ingresadas, en caso de error manda una alerta
    if edad.isnumeric() is False or ahorro_afp.isnumeric() is False or ahorro_apv.isnumeric() is False:
        mensaje('Llene los campos con valores válidos')
        return
    elif sueldo_est.isnumeric() is False or pension_deseada.isnumeric() is False:
        mensaje('Llene los campos con valores válidos')
        return
    
    # Se retorna una lista con: [Apv_requerido]
    # En caso de error, la lista es: [None, mensaje_de_error]
    result = analisis(int(ahorro_afp), afp, fondo, int(edad), int(sueldo_est), sexo, int(ahorro_apv), int(apv_est), int(pension_deseada))

    # Si se envían valores fuera de rango, se muestra una alerta
    if result[0] is None:
        mensaje(result[1])
        return
    
    # Si no hay error, se define el mensaje que envia el programa
    resultado=''
    if result[0]<=0:
        resultado = 'Con los datos ingresados, se puede alcanzar la pensión sin aportes voluntarios'
    
    elif result[0]>0 and result[0]<=1378288:
        resultado ='Con los datos ingresados, para alcanzar la pensión deseada su aporte voluntario debe ser aproximadamente: $'+str(result[0])
    
    elif result[0]>1378288:
        resultado ='Con los datos ingresados, no puede alcanzar su pensión deseada, ya que su APV debería superar el máximo permitido: $'+str(1378288)
    
    # Muestra de resultados
    mensaje(resultado, 'Monto calculado')

def mensaje(mensaje, titulo='Error'):
    # Mensaje de alerta, se envía cuando se mandan valores fuera de rango
    mb.showinfo(message=mensaje, title=titulo)

# Creacion ventana
my_win = tk.Tk()
my_win.title('Retirement Simulator') 

# Tamaño ventana
width_w = 500 
height_w = 440 

# Tamaño pantalla
widht_s = my_win.winfo_screenwidth() 
height_s = my_win.winfo_screenheight() 

# Centrar posicion de ventana usando tamaño pantalla
x = (widht_s/2) - (width_w/2)
y = (height_s/2) - (height_w/2)

# Define Tamaño y posicion de ventana
# Prohibe cambiar tamaño de la ventana
# Define color background
my_win.geometry('%dx%d+%d+%d' % (width_w, height_w, x, y))
my_win.resizable(0,0)
my_win.config(bg='MediumPurple4') # MediumPurple4 RoyalMediumPurple34

# Creacion de 4 frames para
# Titulo, Datos personales, Info AFP y expectativas
frame_0 = tk.Frame(my_win, bg= 'MediumPurple4')
frame_0.place(height=40, width=500, x=0, y=0)

frame_1 = tk.Frame(my_win, bg= 'gray97')
frame_1.place(height=70, width=480,x=10,y=40)

frame_2 = tk.Frame(my_win, bg= 'gray97')
frame_2.place(height=110, width=480,x=10, y=120)

frame_3 = tk.Frame(my_win, bg= 'gray97')
frame_3.place(height=110, width=480,x=10, y=240)

frame_4 = tk.Frame(my_win, bg= 'gray97')
frame_4.place(height=70, width=480,x=10, y=360)

# Frame 0
# Contiene Titulo
titulo = tk.Label(frame_0, text='Retirement Simulator', fg='gray97', bg='MediumPurple4', font=("Helvetica", 18))
titulo.place(height=20, width=245,x=0, y=10)

# Frame 1 - Datos personales
# Textos de informacion
datos_user = tk.Label(frame_1, text='Datos Personales', fg='MediumPurple4', bg ='gray97',font=("Helvetica", 12))
datos_user.place(height=20, width=130 ,x=20, y=5)

genero = tk.Label(frame_1, text='Sexo', fg='black', bg ='gray97')
genero.place(height=20, width=40, x=60, y=30)

age = tk.Label(frame_1, text='Edad', fg='black', bg ='gray97')
age.place(height=20, width=100, x=250, y=30)

# Entradas de informacion
# Entrada por teclado
entry_edad = tk.Entry(frame_1)
entry_edad.place(height=20, width=80, x=360, y=30)

# gen_var guardará la opcion de sexo seleccionado, por defecto guarda Masculino
# gen_values opciones a seleccionar en op_genero
gen_var = tk.StringVar(value='Masculino')
gen_values = ['Masculino','Femenino']

# Menu con opciones de sexo
op_genero = tk.Spinbox(frame_1, values=gen_values, textvariable=gen_var, justify='center', state='readonly', wrap=True)
op_genero.place(height=20, width=80, x=130, y=30)


# Frame 2 - Datos AFP
# Textos de informacion
datos_afp = tk.Label(frame_2, text='Información AFP', fg='MediumPurple4', bg ='gray97',font=("Helvetica", 12))
datos_afp.place(height=20, width=120 , x=20, y=5)

afp_usuario = tk.Label(frame_2, text='AFP', fg='black', bg ='gray97')
afp_usuario.place(height=20, width=40, x=60, y=30)

fondo_usuario = tk.Label(frame_2, text='Fondo', fg='black', bg ='gray97') # 
fondo_usuario.place(height=20, width=40, x=60, y=70)

ahorros_afp = tk.Label(frame_2, text='Ahorros AFP', fg='black', bg ='gray97')
ahorros_afp.place(height=20, width=100, x=250, y=30) 

ahorros_apv = tk.Label(frame_2, text='Ahorros APV', fg='black', bg ='gray97', justify='left')
ahorros_apv.place(height=20, width=100, x=250, y=70)

# Entradas de informacion
# Entradas por teclado
entry_ahorros_afp = tk.Entry(frame_2)
entry_ahorros_afp.place(height=20, width=80, x=360, y=30)

entry_ahorros_apv = tk.Entry(frame_2)
entry_ahorros_apv.place(height=20, width=80, x=360, y=70)

# var_afp guarda la opcion selecionada de op_afp
# val_afp valores a seleccionar en op_afp
var_afp = tk.StringVar()
val_afp = ['Capital', 'Cuprum', 'Habitat', 'Modelo', 'Planvital', 'Provida']

# Menu con opciones de AFP
opc_afp = tk.Spinbox(frame_2, values=val_afp, textvariable=var_afp, justify='center', state='readonly', wrap=True)
opc_afp.place(height=20, width=80, x=130, y=30)

# var_fondo guarda la opcion selecionada de op_fondo
# val_fondo valores a seleccionar en op_fondo
var_fondo = tk.StringVar()
val_fondo = ['A', 'B', 'C', 'D', 'E']

# Menu con opciones de Fondo
opc_fondo = tk.Spinbox(frame_2, values=val_fondo, textvariable=var_fondo, justify='center', state='readonly', wrap=True)
opc_fondo.place(height=20, width=80, x=130, y=70)

# Frame 3 - Expectativas
# Textos de informacion
datos_estimados = tk.Label(frame_3, text='Expectativas', fg='MediumPurple4', bg ='gray97',font=("Helvetica", 12))
datos_estimados.place(height=20, width=100 ,x=20, y=5)

sueldo_usuario = tk.Label(frame_3, text='Sueldo estimado', fg='black', bg ='gray97')
sueldo_usuario.place(height=20, width=100, x=20, y=30)

apv_futuro = tk.Label(frame_3, text='APV estimado', fg='black', bg ='gray97')
apv_futuro.place(height=20, width=100, x=20, y=70)

# Entradas de información por teclado
# Sueldo bruto estimado
entry_sueldo = tk.Entry(frame_3)
entry_sueldo.place(height=20, width=80, x=130, y=30)

# Aporte voluntario estimado
entry_vol = tk.Entry(frame_3)
entry_vol.place(height=20, width=80, x=130, y=70)

# b_simulacion llama a simular(), es el boton que inicia los calculos
b_simulacion = tk.Button(frame_3, text='Simular pensión', command = simular, bg='MediumPurple4', fg='white') 
b_simulacion.place(height=20, width=130, x=280, y=70)

# Frame 4
datos_user = tk.Label(frame_4, text='Análisis de ahorro', fg='MediumPurple4', bg ='gray97',font=("Helvetica", 12))
datos_user.place(height=20, width=130 ,x=20, y=5)

# Textos de informacion
p_deseada = tk.Label(frame_4, text='Pensión deseada', fg='black', bg ='gray97')
p_deseada.place(height=20, width=100, x=20, y=30)

# Entrada de informacion
entry_pension = tk.Entry(frame_4)
entry_pension.place(height=20, width=80, x=130, y=30)

# b_analisis llama a analizar(), inicia los calculos
b_analisis = tk.Button(frame_4, text='Analizar ahorros', command = analizar, bg='MediumPurple4', fg='white') 
b_analisis.place(height=20, width=130, x=280, y=30)

# Mantiene abierta la ventana
my_win.mainloop()