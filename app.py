from productos import *
from usuarios import *
from carrito import *
from flask import *
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'ijnNHYY71FFDrfvcde1927wsx4d4x4xsfñ'
app.permanent_session_lifetime = timedelta(days=60)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def buscar():
    busqueda = request.form.get('busqueda')
    if busqueda:
        return redirect(url_for('resultados', busqueda=busqueda))
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    username = session.get('Nombre')
    resultados = Productos.mostrar_productos()
    if request.method == 'POST':
        resultado_busqueda = buscar()
        if resultado_busqueda:
            return resultado_busqueda
    return render_template('index.html', username=username, resultados=resultados)


@app.route('/resultados/<busqueda>', methods=['GET', 'POST'])
def resultados(busqueda):
    username = session.get('Nombre')
    if request.method == 'POST':
        resultado_busqueda = buscar()
        if resultado_busqueda:
            return resultado_busqueda
    resultados = Productos.buscar_productos(busqueda)
    return render_template('resultados.html', username=username, resultados=resultados)

@app.route('/gestion/<action>', methods=['GET', 'POST'])
def gestion(action):
    username = session.get('Nombre')
    mensaje = ''
    nombre, correo = 'Manuel Alonso', 'alonsomanuel082006@gmail.com'
    if session.get('Nombre') == nombre and session.get('Correo') == correo:
        if action == 'subir_productos':
            if request.method == 'POST':
                resultado_busqueda = buscar()
                if resultado_busqueda:
                    return resultado_busqueda
                categoria = request.form['Categoria']
                nombre = request.form['Nombre']
                precio = request.form['Precio']
                descripcion = request.form['Descripcion']
                stock = request.form['Stock']
                if 'images' not in request.files:
                    return 'No se subieron imágenes', 400
                archivos = request.files.getlist('images')
                urls_guardadas = []
                for archivo in archivos:
                    if archivo.filename == '':
                        continue
                    nombre_archivo = archivo.filename
                    ruta_relativa = f"uploads/{nombre_archivo}"
                    ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
                    archivo.save(ruta_guardado)
                    urls_guardadas.append(ruta_relativa)
                imagenes = ','.join(urls_guardadas)
                producto = Productos(categoria, nombre, precio, descripcion, stock, imagenes)
                mensaje = producto.subir_producto()
            return render_template('gestion.html', action=action, mensaje=mensaje, username=username)
        elif action == 'borrar_producto':
            if request.method == 'POST':
                resultado_busqueda = buscar()
                if resultado_busqueda:
                    return resultado_busqueda
                id = request.form['ID']
                mensaje = Productos.borrar_producto(id)
            return render_template('gestion.html', action=action, mensaje=mensaje, username=username)
        else:
            return 'No se encontró la acción solicitada', 404
    else:
        return redirect(url_for('index'))


@app.route('/producto/<int:id>', methods=['GET', 'POST'])
def ver_producto(id):
    if request.method == 'POST':
        resultado_busqueda = buscar()
        if resultado_busqueda:
            return resultado_busqueda
    username = session.get('Nombre')
    producto = Productos.ver_producto(id)
    imagenes = Productos.ver_imagenes(id)
    index_imagen = int(request.args.get('index', 0))
    imagen_actual = imagenes[index_imagen]
    return render_template(
        'ver_producto.html', 
        username=username, 
        producto=producto, 
        imagen_actual=imagen_actual, 
        index_imagen=index_imagen, 
        total_imagenes=len(imagenes)
    )
@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['Nombre']
        correo = request.form['Correo']
        direccion = Usuarios.obtener_direccion(correo)
        codigo = str(generar_codigo())
        session['Nombre'] = nombre
        session['Correo'] = correo
        session['Direccion'] = direccion
        session['Codigo'] = codigo
        session['Action'] = 'iniciar_sesion'
        usuario = Usuarios(nombre, correo, direccion)
        if Usuarios.verificar_mail(correo) == True:
            usuario.enviar_mail(codigo)
            return redirect(url_for('verificar'))
        else:
            mensaje = f'El correo {correo} no es valido'
        return redirect('verificar')
    return render_template('iniciar_sesion.html', mensaje=mensaje)

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['Nombre']
        correo = request.form['Correo']
        direccion = request.form['Direccion']
        codigo = str(generar_codigo())
        if verificar_usuario(correo) == False:
            session['Nombre'] = nombre
            session['Correo'] = correo
            session['Direccion'] = direccion
            session['Codigo'] = codigo
            session['Action'] = 'registrarse'
            usuario = Usuarios(nombre, correo, direccion)
            if Usuarios.verificar_mail(correo) == True:
                usuario.enviar_mail(codigo)
                return redirect(url_for('verificar'))
            else:
                mensaje = f'El correo {correo} no es valido'
        else:
            mensaje = 'El correo ya esta asociado a una cuenta'
    return render_template('registrarse.html', mensaje=mensaje)

@app.route('/verificacion', methods=['GET', 'POST'])
def verificar():
    mensaje = f"Enviamos un codigo de verificacion a {session.get('Correo')}"
    nombre, correo, direccion, codigo = session.get('Nombre'), session.get('Correo'), session.get('Direccion'), session.get('Codigo')
    if request.method == 'POST':
        codigo_ingresado = request.form['Codigo']
        usuario = Usuarios(nombre, correo, direccion)
        if codigo_ingresado == codigo:
            if session.get('Action') == 'iniciar_sesion':
                session.permanent = True
                mensaje = usuario.iniciar_sesion()
            else:
                session.permanent = True
                mensaje = usuario.registrar_usuario()
        else:
            mensaje = 'Codigo incorrecto'
    return render_template('verificacion.html', mensaje=mensaje)

@app.route('/mostrar_categorias', methods=['GET', 'POST'])
def mostrar_categorias():
    username = session.get('Nombre')
    if request.method == 'POST':
        resultado_busqueda = buscar()
        if resultado_busqueda:
            return resultado_busqueda
    return render_template('mostrar_categorias.html', username=username)

@app.route('/categorias/<categoria>', methods=['GET', 'POST'])
def categorias(categoria):
    username = session.get('Nombre')
    resultados = Productos.mostrar_categoria(categoria)
    if request.method == 'POST':
        resultado_busqueda = buscar()
        if resultado_busqueda:
            return resultado_busqueda
    return render_template('categorias.html', resultados=resultados, username=username)

@app.route('/info', methods=['GET', 'POST'])
def info():
    username = session.get('Nombre')
    if request.method == 'POST':
        resultado_busqueda = buscar()
        if resultado_busqueda:
            return resultado_busqueda
    return render_template('info.html', username=username)


@app.route('/carrito', methods=['GET','POST'])
def carrito():
    if session.get('Nombre'):
        username = session.get('Nombre')
        id_usuario = Usuarios.obtener_id(session.get('Correo'))
        id_usuario = int(id_usuario[0])
        resultados = mostrar_carrito(id_usuario)
        total = calcular_total(id_usuario)
        if request.method == 'POST':
            resultado_busqueda = buscar()
            if resultado_busqueda:
                return resultado_busqueda
        return render_template('carrito.html', username=username, total=total, resultados=resultados)
    return redirect(url_for('iniciar_sesion'))

   
@app.route('/eliminar_producto/<int:id_producto>', methods=['GET','POST'])
def eliminar_producto(id_producto):
    correo = session.get('Correo')
    id_usuario = Usuarios.obtener_id(correo)
    id_usuario = int(id_usuario[0])
    eliminar_del_carrito(id_usuario, id_producto)
    return redirect(url_for('carrito', id_usuario=id_usuario))

@app.route('/agregar_al_carrito/<int:id_producto>', methods=['GET','POST'])
def agregar_carrito(id_producto):
    if session.get('Correo') and session.get('Nombre'):
        correo = session.get('Correo')
        id_usuario = Usuarios.obtener_id(correo)
        id_usuario = int(id_usuario[0])
        agregar_al_carrito(id_usuario, id_producto)
        return redirect(url_for('ver_producto', id=id_producto))
    return redirect(url_for('iniciar_sesion'))

if __name__ == '__main__':
    app.run(debug=False, port=5000)

