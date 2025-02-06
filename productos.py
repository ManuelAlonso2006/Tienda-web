import sqlite3


class Productos:
    def __init__(self, categoria, nombre, precio, descripcion, stock, imagenes, id=None):
        self.id = id
        self.categoria = categoria
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagenes = imagenes
        
    def mostrar_productos():
        conexion = None
        try:
            conexion = sqlite3.connect('persistent/database.db')
            cursor = conexion.cursor()
            cursor.execute("""SELECT id,
        nombre, 
        precio, 
       CASE 
           WHEN instr(imagenes, ',') > 0 
           THEN substr(imagenes, 1, instr(imagenes, ',') - 1)
           ELSE imagenes
       END AS primera_imagen
FROM Productos;
""")
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except sqlite3.Error:
            return 'Se produjo un error al cargar los productos'
        finally:
            if conexion:
                conexion.close()

    def ver_producto(id):
        conexion = None
        try:
            conexion = sqlite3.connect('persistent/database.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT id, nombre, precio, descripcion FROM Productos WHERE id == (?)', (id,))
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except sqlite3.Error:
            return 'Se produjo un error al mostrar el producto'
        finally:
            if conexion:
                conexion.close()
                
    def ver_imagenes(id):
        conexion = None
        try:
            conexion = sqlite3.connect('persistent/database.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT imagenes FROM Productos WHERE id == (?)', (id,))
            resultados = cursor.fetchall()
            conexion.close()
            return [imagen.strip() for imagen in resultados[0][0].split(',')]
        except sqlite3.Error:
            return 'Se produjo un error al mostrar el producto'
        finally:
            if conexion:
                conexion.close()
                
                
    def buscar_productos(busqueda):
        conexion = None
        try:
            conexion = sqlite3.connect('persistent/database.db')
            cursor = conexion.cursor()
            cursor.execute("""SELECT id,
        nombre, 
        precio, 
       CASE 
           WHEN instr(imagenes, ',') > 0 
           THEN substr(imagenes, 1, instr(imagenes, ',') - 1)
           ELSE imagenes
       END AS primera_imagen
FROM Productos WHERE nombre LIKE ? OR categoria LIKE ?;
""",(f'{busqueda}%', f'{busqueda}%'))
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except sqlite3.Error:
            return 'Se produjo un error al cargar los productos'
        finally:
            if conexion:
                conexion.close()             
        
    
                
    def mostrar_categoria(categoria):
        conexion = None
        try:
            conexion = sqlite3.connect('persistent/database.db')
            cursor = conexion.cursor()
            cursor.execute("""SELECT id,
        nombre, 
        precio, 
       CASE 
           WHEN instr(imagenes, ',') > 0 
           THEN substr(imagenes, 1, instr(imagenes, ',') - 1)
           ELSE imagenes
       END AS primera_imagen
FROM Productos WHERE categoria == (?);
""", (categoria,))
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except sqlite3.Error:
            return 'Se produjo un error al cargar los productos'
        finally:
            if conexion:
                conexion.close()
    
    def subir_producto(self):
        conexion = None
        try:
            conexion = sqlite3.connect('persistent/database.db')
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO Productos(categoria, nombre, precio, descripcion, stock, imagenes) VALUES(?, ?, ?, ?, ?, ?)', (self.categoria, self.nombre, self.precio, self.descripcion, self.stock, self.imagenes))
            conexion.commit()
            conexion.close()
            return f'Producto subido con exito'
        except sqlite3.Error:
            return 'Se produjo un error al procesar tu solicitud. Por favor, intenta nuevamente.'
        finally:
            if conexion:
                conexion.close()
                
    def borrar_producto(id):
        conexion = None
        try:
            conexion = sqlite3.connect('persistent/database.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM Productos WHERE id == ?', (id,))
            resultado = cursor.fetchone()
            if resultado != None:
                cursor.execute('DELETE FROM Productos WHERE id == ?', (id,))
                conexion.commit()
                conexion.close()
                return f'El producto se borro con exito'
            else:
                return f'El producto con id {id}, no existe'
        except sqlite3.Error:
            return 'Se produjo un error al procesar tu solicitud. Por favor, intenta nuevamente.'
        finally:
            if conexion:
                conexion.close()

                
