import sqlite3

def agregar_al_carrito(id_usuario, id_producto):
    conexion = None
    try:
        conexion = sqlite3.connect('database/database.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT carrito FROM Usuarios WHERE id == (?)', (id_usuario,))
        resultados = cursor.fetchone() 
        if resultados and resultados[0]:
            cadena = resultados[0]
            lista_nueva = [int(x) for x in cadena.split(",")]
        else:
            lista_nueva = []
        lista_nueva.append(id_producto)
        productos = ','.join(map(str, lista_nueva))  # Corrección aquí
        cursor.execute('UPDATE Usuarios SET carrito = ? WHERE id = ?', (productos, id_usuario))
        conexion.commit()
        conexion.close()
        return 'El producto se añadio al carrito'
    except sqlite3.Error:
        return 'Se produjo un error al procesar tu solicitud'
    finally:
        if conexion:
            conexion.close()

            
def eliminar_del_carrito(id_usuario, id_producto):
    conexion = None
    try:
        conexion = sqlite3.connect('database/database.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT carrito FROM Usuarios WHERE id == (?)', (id_usuario,))
        resultados = cursor.fetchone()
        if resultados and resultados[0]:
            cadena = resultados[0]
            lista_nueva = [int(x) for x in cadena.split(",")]  # Corregido aquí, sin el espacio
            lista_nueva.remove(id_producto)
            productos = ','.join(map(str, lista_nueva))
            cursor.execute('UPDATE Usuarios SET carrito = ? WHERE id = ?', (productos, id_usuario))
            conexion.commit()
            conexion.close()
            return 'Se elimino el producto correctamente'
        else:
            return 'Carrito vacio'    
    except sqlite3.Error:
        return 'Se produjo un error al procesar tu solicitud'
    finally:
        if conexion:
            conexion.close()



def calcular_total(id_usuario):
    conexion = None
    try:
        total = 0
        conexion = sqlite3.connect('database/database.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT carrito FROM Usuarios WHERE id == ?', (id_usuario,))
        resultados = cursor.fetchone()     
        if resultados and resultados[0]:
            cadena = resultados[0]
            lista_ids = [int(x) for x in cadena.split(',')]  # Corregido aquí
            cursor.execute(f"SELECT SUM(precio) FROM Productos WHERE id IN ({','.join(['?'] * len(lista_ids))})", lista_ids)
            total = cursor.fetchone()[0] or 0
        conexion.close()
        return total
    except sqlite3.Error as e:
        return 'Se produjo un error'
    finally:
        if conexion:
            conexion.close()


def mostrar_carrito(id_usuario):
    conexion = None
    try:
        conexion = sqlite3.connect('database/database.db')
        cursor = conexion.cursor()

        # Obtener la lista de productos en el carrito del usuario
        cursor.execute('SELECT carrito FROM Usuarios WHERE id = ?', (id_usuario,))
        resultados = cursor.fetchone()

        if not resultados or not resultados[0]:  
            return []  # Carrito vacío, retornamos lista vacía

        # Convertimos la cadena de productos en una lista de IDs
        lista_ids = [int(x) for x in resultados[0].split(",")]

        # Si no hay productos, devolvemos una lista vacía antes de ejecutar la consulta
        if not lista_ids:
            return []

        # Generamos la consulta de forma dinámica sin usar f-strings directamente
        query = """
        SELECT id, nombre, precio, 
            CASE 
                WHEN instr(imagenes, ',') > 0 
                THEN substr(imagenes, 1, instr(imagenes, ',') - 1)
                ELSE imagenes
            END AS primera_imagen
        FROM Productos WHERE id IN ({})
        """.format(','.join(['?'] * len(lista_ids)))

        # Pasamos los valores correctamente como una tupla
        cursor.execute(query, tuple(lista_ids))

        productos = cursor.fetchall()
        conexion.close()
        return productos  # Devuelve una lista de tuplas

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return []
    finally:
        if conexion:
            conexion.close()

