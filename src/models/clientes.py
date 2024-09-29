#crear la tabla de la base de datos!!!
from sqlalchemy import Column, Integer, String, Boolean
from .data_base import Base

class Clientes(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para cada cliente
    tipo_documento = Column(String(2), nullable=False)  # Tipo de Documento (CC, TI, CE, PS)
    numero_documento = Column(String(20), unique=True, nullable=False)  # Número de Documento único
    nombre = Column(String(100), nullable=False)  # Nombre del Cliente
    apellido = Column(String(100), nullable=False)  # Apellido del Cliente
    telefono = Column(String(20), nullable=False)  # Teléfono del Cliente
    direccion = Column(String(200), nullable=False)  # Dirección del Cliente
    email = Column(String(100), nullable=False)  # Email del Cliente
    is_active = Column(Boolean, default=True)  # Cliente activo por defecto
    is_deleted = Column(Boolean, default=False)  # Eliminación lógica (false por defecto)

#crear cliente!!!

from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from models.data_base import SessionLocal
from models.clientes import Clientes  # Asegúrate de importar el modelo Clientes

# Definir el blueprint para las rutas relacionadas con clientes
clientes_bp = Blueprint('clientes', __name__)

# Ruta para mostrar el formulario de creación de cliente (GET)
@clientes_bp.route('/clientes_crear', methods=['GET'])
def mostrar_formulario_crear_cliente():
    return render_template('form_crear_cliente.html', titulo_pagina = "Crear cliente") # Renderiza la plantilla HTML del formulario

# Ruta para recibir los datos del formulario y crear un cliente (POST)
@clientes_bp.route('/clientes_crear', methods=['POST'])
def crear_cliente():
    db = SessionLocal()

    # Recibir los datos enviados desde el formulario
    tipo_documento = request.form['tipoDocumento']
    numero_documento = request.form['numeroDocumento']
    nombre = request.form['nombreCliente']
    apellido = request.form['apellidoCliente']
    telefono = request.form['telefonoCliente']
    direccion = request.form['direccionCliente']
    email = request.form['emailCliente']

    # Crear una nueva instancia del cliente
    nuevo_cliente = Clientes(
        tipo_documento=tipo_documento,
        numero_documento=numero_documento,
        nombre=nombre,
        apellido=apellido,
        telefono=telefono,
        direccion=direccion,
        email=email,
        is_active=True  # Por defecto el cliente está activo
    )

    # Guardar el cliente en la base de datos
    try:
        db.add(nuevo_cliente)
        db.commit()
        flash('Cliente creado con éxito', 'success')  # Muestra un mensaje de éxito
    except Exception as e:
        db.rollback()  # Deshacer cambios si hay error
        flash(f'Error al crear cliente: {str(e)}', 'danger')  # Muestra un mensaje de error
    finally:
        db.close()

    # Redirigir al formulario después de crear el cliente
    return redirect(url_for('clientes.mostrar_formulario_crear_cliente'))  # Redirige a la misma página

#ver cliente!!
@clientes_bp.route('/clientes_ver', methods=['GET'])
def ver_clientes():
    db = SessionLocal()
    clientes = db.query(Clientes).all()  # Consultar todos los clientes de la base de datos
    db.close()

    # Renderizar la plantilla con la lista de clientes
    return render_template('form_ver_cliente.html', titulo_pagina="Ver Clientes", clientes=clientes)


#editar el cliente!!!

# Ruta para mostrar el formulario de edición de cliente (GET)
@clientes_bp.route('/clientes_editar', methods=['GET'])
def mostrar_formulario_editar_cliente():
    return render_template('form_editar_cliente.html', titulo_pagina="Editar Cliente")

# Ruta para buscar un cliente según su tipo y número de documento (GET)
@clientes_bp.route('/clientes_buscar', methods=['GET'])
def buscar_cliente():
    tipo_documento = request.args.get('tipoDocumento')
    numero_documento = request.args.get('numeroDocumento')

    db = SessionLocal()
    cliente = db.query(Clientes).filter_by(tipo_documento=tipo_documento, numero_documento=numero_documento).first()
    db.close()

    if cliente:
        return jsonify({
            'id': cliente.id,
            'tipo_documento': cliente.tipo_documento,
            'numero_documento': cliente.numero_documento,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'email': cliente.email,
            'is_active': cliente.is_active
        })
    else:
        return jsonify({'error': 'Cliente no encontrado'}), 404

# Ruta para actualizar un cliente (POST)
@clientes_bp.route('/clientes_actualizar', methods=['POST'])
def actualizar_cliente():
    db = SessionLocal()

     # Recibe los datos del formulario, incluido el estado del cliente
    cliente_id = request.form['clienteId']
    tipo_documento = request.form['tipoDocumento']
    numero_documento = request.form['cedulaCliente']
    nombre = request.form['nombreCliente']
    apellido = request.form['apellidoCliente']
    telefono = request.form['telefonoCliente']
    direccion = request.form['direccionCliente']
    email = request.form['emailCliente']
    estado_cliente = request.form['estadoCliente']  # <-- Asegúrate de recibir el estado del cliente

    # Imprime los datos recibidos para verificar
    print(f'Datos recibidos: {cliente_id}, {tipo_documento}, {numero_documento}, {nombre}, {apellido}, {telefono}, {direccion}, {email}')

    # Busca al cliente en la base de datos
    cliente = db.query(Clientes).filter_by(id=cliente_id).first()

    if cliente:
        cliente.tipo_documento = tipo_documento
        cliente.numero_documento = numero_documento
        cliente.nombre = nombre
        cliente.apellido = apellido
        cliente.telefono = telefono
        cliente.direccion = direccion
        cliente.email = email
        cliente.is_active = estado_cliente.lower() == 'activo'  # Actualiza el estado (Activo o Inactivo)
        # Guardar los cambios
        db.commit()
        flash('Cambios guardados correctamente', 'success')
    else:
        flash('Error al guardar los cambios', 'danger')

    db.close()

    # Redirigir al formulario de edición
    return redirect(url_for('clientes.mostrar_formulario_editar_cliente'))
