import data 

# Función que calcula pensión y monto total de ahorro
def simulacion(ahorro_o , afp, fondo, edad, sueldo, genero, ahorro_v, apv):
    
    #Validacion de datos ingresados
    if ahorro_v < 0 or ahorro_o < 0 or apv < 0 or sueldo < 0:
        lista = [None,"Ingrese valores positivos"]
        return lista

    if genero == 'Masculino':
        if edad > 65 or edad < 18:
            lista = [None,"Ingrese una edad entre 18 y 65 años"]
            return lista 
    if genero == 'Femenino':
        if edad > 60 or edad <18:
            lista = [None,"Ingrese una edad entre 18 y 60 años"]
            return lista

    # Importa los fondos de la afp del usuario
    for i in data.lista_afp:
        if afp == i['name']:
            afp_user = i
    
    # Importa los fondos voluntarios de la afp del usuario
    for i in data.lista_apv:
        if afp == i['name']:
            apv_user = i

    # Cantidad de meses restantes de cotizacion según género
    tiempo_trabajo = 0
    if genero == 'Masculino':
        tiempo_trabajo = (65 - edad)*12
    elif genero == 'Femenino':
        tiempo_trabajo = (60 - edad)*12

    # Cálculo de aportes voluntarios
    # Topes máximos de APV
    if apv > 1378288:
        apv = 1378288
        
    # Cálculo de los ahorros voluntarios
    ahorros_apv = apv*tiempo_trabajo + ahorro_v
    rentabilidad_apv = ahorros_apv*(apv_user[fondo]/100)
    final_apv = ahorros_apv + rentabilidad_apv

    # Cálculo de aportes obligatorios 
    # Topes máximos y mínimos imponibles de sueldos
    if sueldo > 2183208:
        sueldo = 2183208
        
    if sueldo < 301000:
        sueldo = 301000

    # Cotizaciones = 10% del sueldo * cantidad de meses de trabajo restantes
    cotizaciones = (sueldo*0.1)*tiempo_trabajo

    # Calculo de ahorros
    if fondo != 'A':
        # Ahorros de usuarios sin cambio de fondos
        ahorros_afp = cotizaciones + ahorro_o
        final_afp = ahorros_afp + ahorros_afp*afp_user[fondo]/100
    else:
        # Ahorro de usuarios con cambio de Fondo A hacia B
        if genero == 'Masculino': 
            tiempo_trabajo = (55-edad)*12
        elif genero == 'Femenino':
            tiempo_trabajo = (50-edad)*12

        # Cálculo de ahorro antes de cambiar fondo
        cotizaciones_A = (sueldo*0.1)*tiempo_trabajo
        ahorros_fondo_A = cotizaciones_A + ahorro_o
        final_fondo_A = ahorros_fondo_A + ahorros_fondo_A*(afp_user[fondo]/100)

        # Cálculo de ahorro despues de cambiar fondo
        tiempo_trabajo = 120
        cotizaciones_B = (sueldo*0.1)*tiempo_trabajo
        ahorros_fondo_B = cotizaciones_B + final_fondo_A 
        final_afp = ahorros_fondo_B + ahorros_fondo_B*(afp_user['B']/100)

    # Monto final ahorrado
    total_ahorro = int( final_afp + final_apv)
    
    # Cálculo de pensión
    if genero == 'Masculino' :
        tiempo_pension = 15*12 # asumiendo que la esperanza de vida en chile para un hombre es de 80 años y se jubila a los 65
    if genero == 'Femenino' :
        tiempo_pension = 25*12 # asumiendo que la esperanza de vida en chile para una mujer es de 85 años  y se jubila a los 60
    pension = int(total_ahorro/tiempo_pension)

    # total_ahorro, pension son los resultados a mostrar en la simulación
    # final_afp, rentabilidad_apv son requeridos por la función analisis()
    lista = [total_ahorro, pension, final_afp, rentabilidad_apv]
    return lista



#Obtiene monto de Apv necesario para alcanzar la pensión deseada
def analisis(ahorro_o, afp, fondo, edad, sueldo, genero, ahorro_v, apv, pension_deseada):

    #Validacion de datos ingresados
    if pension_deseada <= 0 :
        lista = [None,"Ingrese valores positivos"]
        return lista

    #Se obtiene una lista con: [total_ahorro, pension, ahorros_cotizaciones, rentabilidad_aportes_voluntarios]
    # ahorros_cotizaciones y rentabilidad_aportes_voluntarios son necesarios para el cálculo
    simular = simulacion(ahorro_o , afp, fondo, edad, sueldo, genero, ahorro_v, apv)

    #Cantidad de meses de pensión y cotizaciones
    if genero == 'Masculino':
        tiempo_pension = 180 # Asumiendo que la esperanza de vida en chile para un hombre es de 80 años y se jubila a los 65
        tiempo_trabajo = (65 - edad)*12

    if genero == 'Femenino':
        tiempo_pension = 300 # Asumiendo que la esperanza de vida en chile para una mujer es de 85 años y se jubila a los 60
        tiempo_trabajo = (60 - edad)*12
    
    #Obtención del Apv requerido
    monto_total_deseado = pension_deseada*tiempo_pension
    ahorros_afp = simular[2]
    rentabilidad_apv = simular[3]
    apv = int((monto_total_deseado - ahorros_afp - rentabilidad_apv - ahorro_v) / tiempo_trabajo)

    return [apv]