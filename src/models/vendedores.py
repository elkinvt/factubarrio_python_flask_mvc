from sqlalchemy import Column, Integer, String, Boolean
from .data_base import Base

class Vendedores(Base):
    __tablename__ = 'vendedores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para cada vendedor
    tipo_documento = Column(String(2), nullable=False)  # Tipo de Documento (CC, TI, CE, PS)
    numero_documento = Column(String(20), unique=True, nullable=False)  # Número de Documento único
    nombre = Column(String(100), nullable=False)  # Nombre del vendedor
    apellido = Column(String(100), nullable=False)  # Apellido del vendedor
    telefono = Column(String(20), nullable=False)  # Teléfono del vendedor
    direccion = Column(String(200), nullable=False)  # Dirección del vendedor
    email = Column(String(100), nullable=False)  # Email del vendedor
    is_deleted = Column(Boolean, default=False)  # Eliminación lógica (false por defecto)

    #crear vendedor!!!

from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from models.data_base import SessionLocal


# Definir el blueprint para las rutas relacionadas con vendedores
vendedores_bp = Blueprint('vendedores', __name__)

@vendedores_bp.route('/vendedores_crear', methods=['GET', 'POST'])
def crear_vendedor():
    if request.method == 'POST':
        db = SessionLocal()

        # Recibir los datos enviados desde el formulario
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre = request.form['nombreVendedor']
        apellido = request.form['apellidoVendedor']
        telefono = request.form['telefonoVendedor']
        direccion = request.form['direccionVendedor']
        email = request.form['emailVendedor']

        # Crear una nueva instancia del vendedor
        nuevo_vendedor = Vendedores(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            email=email
        )

        try:
            db.add(nuevo_vendedor)
            db.commit()
            flash('Vendedor creado con éxito', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error al crear vendedor: {str(e)}', 'danger')
        finally:
            db.close()

        return redirect(url_for('vendedores.crear_vendedor'))  # Redirigir después de crear el vendedor

    # Si es un GET, mostrar el formulario
    return render_template('form_crear_vendedor.html', titulo_pagina="Crear vendedor")


#ver vendedor!!
@vendedores_bp.route('/vendedores_ver', methods=['GET'])
def ver_vendedores():
    db = SessionLocal()
    vendedores = db.query(Vendedores).filter_by(is_deleted=False).all()  # Solo vendedores que no están eliminados
    db.close()

    # Renderizar la plantilla con la lista de vendedores
    return render_template('form_ver_vendedor.html', titulo_pagina="Ver Vendedores", vendedores=vendedores)


