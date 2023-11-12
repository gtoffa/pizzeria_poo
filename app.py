
from datetime import time, timedelta, datetime
import os
import getpass
import random
import math


class Pizza():

    def __init__(self, nombre, ingredientes, precio_base):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.precio_base = precio_base

    def __str__(self) -> str:
        return f"{self.nombre} - Ingredientes({', '.join(self.ingredientes)})"


class Tipo():
    '''
     clase para tipo cocción (a la piedra, a la parrilla, molde) y tiempo para realizar calculos de duracion
    '''

    def __init__(self, tipo, tiempo_coccion, precio_elaboracion):
        self.tipo = tipo
        self.tiempo_coccion = tiempo_coccion
        self.precio_elaboracion = precio_elaboracion

    def __str__(self) -> str:
        return f"{self.tipo}  {self.duracion_minutos()} "

    def duracion_minutos(self) -> str:
        return f"Duracion: {self.tiempo_coccion .total_seconds() / 60} minutos"

    def duracion_minutos_cant(self, cantidad) -> str:
        return f"{(self.tiempo_coccion*cantidad).total_seconds() / 60} min."


class Variedad():
    '''
        clase se utiliza para guardar todas las variedades de pizza, modo de cocción y porciones
    '''

    def __init__(self, pizza: Pizza, tipo, precio, porciones):
        self.pizza: Pizza = pizza
        self.precio = precio
        self.tipo: Tipo = tipo
        self.porciones = porciones

    def __str__(self) -> str:
        return f"{self.pizza.nombre} {self.tipo.tipo} - X{self.porciones}P. -> ${self.precio}"


class Usuario():

    def __init__(self, nombre, user, contrasenia, rol):
        self.nombre = nombre
        self.user = user
        self.contrasenia = contrasenia
        self.rol = rol

    def __str__(self) -> str:
        return f"{self.nombre} ({self.rol})"


class DetallePedidos:
    def __init__(self, variedad, cantidad):
        self.variedad = variedad
        self.cantidad = cantidad

    def __str__(self) -> str:
        return f"{self.variedad} {' '*10} | {self.cantidad} | ${self.precio_total()}"

    def precio_total(self):
        return self.cantidad*self.variedad.precio


class Pedidos:
    def __init__(self, numero, fecha, cliente, detallePedidos, estado, usuario):
        self._numero = numero
        self._fecha = fecha
        self._cliente = cliente
        self._detallePedidos = detallePedidos
        self._estado = estado
        self._usuario = usuario
        self._total = None
        self._fecha_entrega = None
        self._demora = None

    def __str__(self)->str:
        return f"Pedido {self._numero}"
    
    def tiempo_estimado(self) -> timedelta:
        tiempo: timedelta
        for dp in self.detallePedidos:
            tiempo += dp.variedad.tipo.tiempo_coccion * dp.cant

        return tiempo

    def print_pedido(self):
        print(f"Pedido N°: {self._numero}")
        print(f"Cliente  : {self._cliente}")
        print(f"Estado   : {self._estado}")
        print("Detalles")
        print("="*136)
        formato = "{:<97}   {:<10}   {:<10}   {:<10}  "

        print(formato.format(* ("Pizza", "Cant", "Duracion", "SubT")))
        print(formato.format(* ("-----", "----", "--------", "----")))

        for dp in self.get_detallePedidos():
            print(formato.format(
                *(dp.variedad.__str__(),  dp.cantidad, dp.variedad.tipo.duracion_minutos_cant(dp.cantidad), f"${dp.precio_total():.2f}")))

        if len(self.get_detallePedidos()) < 10:
            print("\n"*(10-len(self.get_detallePedidos())))

        print("="*136)
        self.establecer_totales()

        formato_fecha = "%d-%m %H:%M"
        print(formato.format(
            * ("", "", "Total",  f"${self._total:.2f}")))
        print(formato.format(
            * ("", "", "Demora",  f"{self._demora}")))
        print(formato.format(
            * ("", "", "Entrega",  f"{self._fecha_entrega.strftime(formato_fecha)}")))

    def establecer_totales(self):
        self._total = 0
        self._fecha_entrega = None
        self._demora = timedelta(minutes=0)
        for dp in self._detallePedidos:
            self._total += dp.precio_total()
            self._demora += dp.variedad.tipo.tiempo_coccion*dp.cantidad

        self._fecha_entrega = datetime.now() + self._demora

    # Getter y Setters

    def get_numero(self):
        return self._numero

    def set_numero(self, nuevo_numero):
        self._numero = nuevo_numero

    def get_fecha(self):
        return self._fecha

    def set_fecha(self, nueva_fecha):
        self._fecha = nueva_fecha

    def get_cliente(self):
        return self._cliente

    def set_cliente(self, nuevo_cliente):
        self._cliente = nuevo_cliente

    def get_detallePedidos(self) -> []:
        return self._detallePedidos

    def set_detallePedidos(self, nuevo_detallePedidos):
        self._detallePedidos = nuevo_detallePedidos

    def get_estado(self):
        return self._estado

    def set_estado(self, nuevo_estado):
        self._estado = nuevo_estado

    def get_usuario(self):
        return self._usuario

    def set_usuario(self, nuevo_usuario):
        self._usuario = nuevo_usuario

    def get_total(self):
        return self._total

    def set_usuario(self, total):
        self._total = total

    def get_fecha_entrega(self) -> str:
        formato_fecha = "%d-%m %H:%M"
        return f"{self._fecha_entrega.strftime(formato_fecha)}"


# Función para limpiar la pantalla de la consola
def limpiar_pantalla():
    """
    Esta función se encarga de limpiar la pantalla de la consola,
    detectando el sistema operativo y ejecutando el comando
    apropiado para limpiar la pantalla.
    """
    if os.name == "posix":  # En sistemas tipo Unix (macOS y Linux)
        os.system("clear")
    elif os.name == "nt":  # En Windows
        os.system("cls")


# Funcion generica para imprimir el encabezado
def print_encabezado(text=None):
    limpiar_pantalla()
    print('''
                // ""--.._
                ||  (_)  _ "-._
                ||    _ (_)    '-.   Bytes & Slices Pizzería
                ||   (_)   __..-'
                 \__..--""
        ''')
    print("▒"*136)

    print("Fecha  : ", datetime.now().strftime("%d-%m-%Y"))
    if user_actual != None:
        print(f"Usuario: {user_actual}\n")

    if text != None:
        print("")
        print(text)
        print("—"*136)


# Inicializar usuarios
usuarios = [
    Usuario(user="empleado", nombre="Elsa Pallo",
            contrasenia="1234", rol="empleado"),
    Usuario(user="cocina", nombre="Armando Calabreza",
            contrasenia="1234", rol="chef"),
    Usuario(user="admin", nombre="Aquiles Bailo", contrasenia="1234", rol="admin")]

# agregamos tipos de pizza los precios estan establecido por 1 porcion
pizzas = [
    Pizza("Pizza Margarita", ["Tomate", "Queso", "Albahaca"], 210),
    Pizza("Pizza Pepperoni", ["Tomate", "Queso", "Pepperoni"], 250),
    Pizza("Pizza Hawaiana", ["Tomate", "Queso", "Jamón", "Piña"], 270),
    Pizza("Pizza Vegetariana", [
        "Tomate", "Queso", "Pimiento", "Champiñones", "Aceitunas"], 280)]


# agregamos tipos de coccion los precios estan establecido por 1 porcion
tipos_cocciones = [Tipo("a la piedra", timedelta(minutes=7), 20),
                   Tipo("a la parrilla", timedelta(minutes=5), 10),
                   Tipo("al molde", timedelta(minutes=15), 30)]

variedades = []

# Creamos todas las variedades disponibles según pizza tipo de cocción
for pizza in pizzas:
    for tipo in tipos_cocciones:
        for porcion in range(8, 13, 2):
            # para el precio se suma el precio de elaboracion por el precio base de la pizza
            # y se multiplica por la cantidad de porciones
            precio_pizza = (tipo.precio_elaboracion +
                            pizza.precio_base) * porcion
            variedades.append(Variedad(pizza, tipo, precio_pizza, porcion))


list_pedidos = []

# Pedidos random de ejemplo
for i in range(10):
    p = Pedidos(numero=i, cliente="Prueba", estado="Entregado", detallePedidos=[],
                fecha=datetime.now(), usuario=usuarios[1])
    cant_variedad = len(variedades)-1
    dp = [
        DetallePedidos(cantidad=random.randint(1, 3),
                       variedad=variedades[random.randint(0, cant_variedad)]),
        DetallePedidos(cantidad=random.randint(1, 3),
                       variedad=variedades[random.randint(0, cant_variedad)]),
    ]
    p.set_detallePedidos(dp)
    p.establecer_totales()
    list_pedidos.append(p)


user_actual = None

# funcion inicial del programa


def login():

    print_encabezado("Iniciar Sesión")

    usuario = input("Ingrese Usuario: ")
    contrasenia = getpass.getpass("Ingres tu contraseña: ")

    global user_actual
    # user_actual:Usuario = None
    try:
        # Filtramos y traemos el primer usuario que coincida con la credencial
        user_actual = [u for u in usuarios if u.user ==
                       usuario and u.contrasenia == contrasenia][0]

    except:
        print("usuario o contraseña incorrectos")
        input("")
        login()
    else:
        menu_principal()


def lista_pedidos_disponibles():
    return [p for p in list_pedidos if p.get_estado() == "Pendiente" or p.get_estado() == "p/Entregar"]


def print_pedidos():
   
    pedidos_disponibles = lista_pedidos_disponibles()
    print_encabezado(f"Pedidos({len(pedidos_disponibles)})")
    # el formato se usa para establecer anchos fijos
    formato = "|{:<2} | {:<10} | {:<15} | {:<60} |{:<11}| {:<4} | {:<7} | {:<7}|"
    print(formato.format(
        * ("N°", "Estado", "Cliente", "Detalle", "Entrega", "Cant", "SubT", "Total")))
    print("—"*136)
    for p in pedidos_disponibles:
        print(formato.format(
            *(p.get_numero(), p.get_estado(), p.get_cliente(), "", p.get_fecha_entrega(), "", "", f"$ {p.get_total()}")))

        for dp in p.get_detallePedidos():
            print(formato.format(
                *("", "", "", dp.variedad.__str__(), "", dp.cantidad, f"$ {dp.precio_total()}",  "")))
        print("—"*136)

# Función genérica para imprimir una lista de opciones, la misma controla que sea una selección correcta


def print_opciones(encabezado, lista) -> int:
    opcion = -1
    while opcion < 0 or opcion > len(lista):

        print_encabezado(encabezado)
        for index, elemento in enumerate(lista):
            print(f"{index+1}: {elemento}")

        print(f"0: <- Volver")
        opcion = int(input("Ingrese codigo: "))

    return opcion


def agregar_detalle(pedido: Pedidos):

    def select_pizza():
        opcion = print_opciones("Seleccione una Pizza", pizzas)

        if opcion == 0:
            gestionar_pedido(pedido)
        else:
            select_coccion(pizzas[opcion-1])

    def select_coccion(pizza_seleccionada):
        opcion = print_opciones(
            f"Seleccione tipo de coccion disponible: \n{pizza_seleccionada}", tipos_cocciones)

        if opcion == 0:
            select_pizza()
        else:
            select_variedad(tipos_cocciones[opcion-1], pizza_seleccionada)

    def select_variedad(tipos_coccion, pizza_seleccionada):
        variedad_filtro = [variedad for variedad in variedades if variedad.pizza ==
                           pizza_seleccionada and variedad.tipo == tipos_coccion]

        opcion = print_opciones(
            f"Resultado de la Busqueda:", variedad_filtro)

        if opcion == 0:
            select_coccion(pizza_seleccionada)

        cantidad = int(input("ingrese la cantidad: "))

        pedido.get_detallePedidos().append(
            DetallePedidos(variedad_filtro[opcion-1], cantidad))
        gestionar_pedido(pedido)

    select_pizza()


def gestionar_pedido(pedido=None):
    global list_pedidos

    if pedido == None:
        pedido = Pedidos(0, datetime.now(), "", [], "Pendiente", user_actual)

    print_encabezado("Nuevo Pedido")

    if pedido.get_numero() == 0:
        pedido.set_numero(len(list_pedidos)+1)
        cliente = input("Ingrese nombre de cliente: ")
        pedido.set_cliente(cliente)

        print_encabezado("Gestion de Pedido")

    pedido.print_pedido()
    opcion = int(input("[(1)Agregar Piazza]  [(2)Guardar]   [(0)Salir]"))

    if opcion == 1:
        agregar_detalle(pedido)
    if opcion == 2:
        list_pedidos.append(pedido)
        pedido = Pedidos(0, datetime.now(), "", [], "Pendiente", user_actual)
    else:
        menu_principal()


def obtener_fecha():
    '''
       funcion que solicita fecha  y lo setea
    '''
    while True:
        try:
            fecha_str = input("Ingrese una fecha en el formato DD-MM-YYYY: ")
            fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
            return fecha
        except ValueError:
            print("Formato de fecha incorrecto. Intente de nuevo.")


def menu_estadisticas():
    pedidos_entregados = [
        p for p in list_pedidos if p.get_estado() == "Entregado"]

    def print_variedades_tipo():
        pizzas_vendidas = [{"pizza": pizza, "cant": 0} for pizza in pizzas]
        tipo_vendidas = [{"tipo": tipo, "cant": 0} for tipo in tipos_cocciones]

        venta_total = 0

        for pedido in pedidos_entregados:
            for detalle_pedido in pedido.get_detallePedidos():
                # Actualizar la lista pizzas_total
                for pt in pizzas_vendidas:
                    if pt["pizza"] == detalle_pedido.variedad.pizza:
                        pt["cant"] += detalle_pedido.cantidad

                # Actualizar la lista cant_tipo
                for tipo in tipo_vendidas:
                    if tipo["tipo"] == detalle_pedido.variedad.tipo:
                        tipo["cant"] += detalle_pedido.cantidad

                venta_total += detalle_pedido.cantidad

        # Ordenar pizzas_cant por cantidad de forma descendente
        pizzas_vendidas = sorted(
            pizzas_vendidas, key=lambda x: x["cant"], reverse=True)
        # Ordenar tipo_vendidas por cantidad de forma descendente
        tipo_vendidas = sorted(
            tipo_vendidas, key=lambda x: x["cant"], reverse=True)

        print_encabezado(f"Total de Ventas entregadas:{venta_total}")

        formato = "{:<20}  {:100}   {:<10}  "

        print(formato.format(* ("Pizza", "", "Ventas")))
        print(formato.format(* ("-----", "", "------")))
        for pt in pizzas_vendidas:
            porcentaje = (pt["cant"]/venta_total)*100 if venta_total > 0 else 0
            porcent_entero = math.trunc(porcentaje)

            print(formato.format(*
                                 (pt['pizza'].nombre, f"{'▓' * porcent_entero} {porcentaje:.2f}%", pt['cant'])))
            print()

        print("\n\n")
        print(formato.format(* ("Tipo", "", "Ventas")))
        print(formato.format(* ("-----", "", "------")))
        for pt in tipo_vendidas:
            porcentaje = (pt["cant"]/venta_total)*100 if venta_total > 0 else 0
            porcent_entero = math.trunc(porcentaje)

            print(formato.format(*
                                 (pt['tipo'].tipo, f"{'▓' * porcent_entero} {porcentaje:.2f}%", pt['cant'])))
            print()

        input("Enter para volver")
        menu_estadisticas()

    def print_ingresos():
        print_encabezado(f"Ingresos entregados por periodo")

        # Solicitar dos períodos de fecha
        print("Ingrese el primer período:")
        fecha_inicio = obtener_fecha()
        fecha_fin = obtener_fecha()
        fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)

        total_recuadacion = 0.0

        for pedido in pedidos_entregados:
            if fecha_inicio <= pedido.get_fecha() <= fecha_fin:
                total_recuadacion += pedido.get_total()

        print(f"Total de Ingresos: ${total_recuadacion:.2f}")
        input("Enter para volver")
        menu_estadisticas()

    def print_pedidos_periodo():
        print_encabezado(
            f"Pedidos (cantidad y monto) por períodos de tiempo (Pendiente - p/Entregar - Entregados )")

        # Solicitar dos períodos de fecha
        print("Ingrese el primer período:")
        fecha_inicio = obtener_fecha()
        fecha_fin = obtener_fecha()
        fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)

        total_recuadacion = 0.0

        for pedido in list_pedidos:
            if fecha_inicio <= pedido.get_fecha() <= fecha_fin:
                total_recuadacion += pedido.get_total()

        print(f"Total monto     : ${total_recuadacion:.2f}")
        print(f"Total de Pedidos: {len(list_pedidos)}")
        input("Enter para volver")
        menu_estadisticas()

    menu = [
        "Variedades y tipos de pizzas más pedidas por los clientes.",
        "Ingresos (recaudaciones) por períodos de tiempo.",
        "Pedidos (cantidad y monto) por períodos de tiempo."
    ]

    opcion = print_opciones("Seleccione opcion", menu)

    if opcion == 0:
        menu_principal()
    else:
        opcion -= 1
        if opcion == 0:
            print_variedades_tipo()
        elif opcion == 1:
            print_ingresos()
        elif opcion == 2:
            print_pedidos_periodo()


def menu_usuarios():
    pass


def cambiar_estado_pedido():
    pedidos_disponibles = lista_pedidos_disponibles()
     
    print_pedidos()
    print("[(0) volver]")
    num_pedido = int(input("Ingrese N° Pedido"))

    try:
        if num_pedido == 0:
            menu_principal()
         
        pedido = [p for p in pedidos_disponibles if p.get_numero() == num_pedido][0]  
    except:
        cambiar_estado_pedido()

    estado_pedido = [
        "Pendiente", "p/Entregar", "Entregado"]
    opcion = print_opciones(f"Seleccione Estado para {pedido}", estado_pedido)

    if opcion == 0:
        cambiar_estado_pedido()
    else:
        pedido.set_estado(estado_pedido[opcion-1])
        [p for p in list_pedidos if p.get_numero() == num_pedido][0] = pedido
         
        menu_principal()


def menu_principal():

    
    print_pedidos()

    opciones = []

    opciones.append({"op": "(1)Cambiar estado Pedido",
                     "funcion":  cambiar_estado_pedido
                     })

    if user_actual.rol == "admin" or user_actual.rol == "empleado":
        opciones.append({"op": "(2)Nuevo Pedido",
                         "funcion":  gestionar_pedido
                         })

    if user_actual.rol == "admin":
        opciones.append({"op": "(3)Estadisticas",
                         "funcion":  menu_estadisticas
                         })
        opciones.append({"op": "(4)Usuarios",
                         "funcion":  menu_usuarios
                         })
    opciones.append({"op": "(0)Salir"})

    menu = ""
    for op in opciones:
        menu += f"[{op['op']}]{' '*5}"

    print(menu)

    opcion = int(input("Opción: "))

    if opcion == 0:
        login()
    else:
        funcion_selecc = None
        try:
            # Verificamos si es una opcion valida y ejecutamos la accion
            funcion_selecc = opciones[opcion-1]["funcion"]
        except:
            print("Opción no valida")
            input("")
            menu_principal()
        else:
            funcion_selecc()


login()
