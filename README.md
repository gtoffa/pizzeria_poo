# Sistema de Pizzería

Este repositorio contiene el código fuente para un sistema de pizzería que gestiona pedidos de clientes. La aplicación se ejecuta en la terminal y permite a los usuarios, con roles específicos, interactuar con el sistema para crear, gestionar y analizar pedidos de pizzas.

## Instrucciones de Ejecución

1. **Clonar el Repositorio:**
   ```bash
   git clone https://github.com/gtoffa/pizzeria_poo.git
   cd sistema-de-pizzeria
   ```

2. **Ejecución del Programa:**
   ```bash
   python app.py
   ```
   El programa se ejecutará en la terminal.

3. **Usuarios:**
    
   Todos los usuarios tiene la contraseña 1234.
   | Usuario | Rol          |
   | :---:   | :---:        |
   | empleado| Empleado     |
   | admin   | Administrador|
   | cocina  | chef         |

## Características

- **Creación de Variedades de Pizza al Iniciar:** Al ejecutar el programa, se crean las variedades de pizza (tipos de pizza, tipo de cocción y cantidad de porciones).

- **Cálculo de Precio:** El sistema calcula automáticamente el precio total de una variedad de pizza. Utiliza el precio por porción de pizza y el precio por unidad de tipo de cocción, multiplicado por la cantidad de porciones seleccionadas (8, 10, 12).

- **Roles de Usuario:** El sistema tiene diferentes roles de usuario, como empleado y administrador. Cada rol tiene permisos específicos para realizar acciones en el sistema.

- **Gestión de Pedidos:** El empleado puedo agregar nuevos pedidos y todos los roles pueden cambiar el estado de un pedido a (entregado, pendiente/para entregar y entregado). Este cambio de estado facilita la filtración de pedidos para estadísticas o para mostrar únicamente los pedidos actuales.

- **Acciones Específicas por Rol:**
  - *Empleado:* Puede agregar nuevos pedidos y cambiar el estado de los pedidos.
  - *Administrador:* Además de las acciones de empleado, puede ver estadísticas y la lista de usuarios.

 
## Código Abierto

Este sistema de pizzería es un proyecto de código abierto, lo que significa que el código fuente está disponible para que la comunidad lo explore, modifique y mejore. 
