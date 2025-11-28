import sys
from datetime import datetime, date
from DAO import Database, EmpleadoDAO, DepartamentoDAO, ProyectoDAO, UsuarioDAO
from DTO import EmpleadoDTO, DepartamentoDTO, ProyectoDTO, UsuarioDTO
from utils.utils import consultar_indicadores, generar_excel, generar_pdf

db_connection = Database().get_connection()
empleado_dao = EmpleadoDAO(db_connection)
departamento_dao = DepartamentoDAO(db_connection)
proyecto_dao = ProyectoDAO(db_connection)
usuario_dao = UsuarioDAO(db_connection)

def input_seguro(mensaje: str) -> str:
    val = input(mensaje)
    return val.strip()

def validar_email(email: str) -> bool:
    return "@" in email and "." in email

def validar_salario(salario_str: str) -> float:
    try:
        salario = float(salario_str)
        return salario if salario >= 0 else 0.0
    except ValueError:
        return 0.0

def login() -> str:
    print("\n=== INICIAR SESIÓN ===")
    username = input_seguro("Usuario: ")
    password = input_seguro("Contraseña: ")
    
    usuario = usuario_dao.validar_credenciales(username, password)
    
    if usuario:
        print(f"Acceso concedido. Bienvenido {usuario.username} (Rol: {usuario.rol})")
        return usuario.username
    else:
        print("Credenciales inválidas.")
        return ""

def menu_empleados():
    while True:
        print("\n--- GESTIÓN EMPLEADOS ---")
        print("1. Crear Empleado")
        print("2. Listar Empleados")
        print("3. Buscar Empleado por ID")
        print("4. Actualizar Empleado")
        print("5. Asignar a Departamento")
        print("6. Eliminar Empleado")
        print("7. Volver")
        
        opcion = input("Opción: ")
        
        if opcion == '1':
            crear_empleado()
        elif opcion == '2':
            listar_empleados()
        elif opcion == '3':
            buscar_empleado()
        elif opcion == '4':
            actualizar_empleado()
        elif opcion == '5':
            asignar_empleado_departamento()
        elif opcion == '6':
            eliminar_empleado()
        elif opcion == '7':
            break

def crear_empleado():
    print("\n--- CREAR EMPLEADO ---")
    
    nombre = input_seguro("Nombre: ")
    email = input_seguro("Email: ")
    
    if not validar_email(email):
        print("Email inválido.")
        return
    
    direccion = input_seguro("Dirección: ")
    telefono = input_seguro("Teléfono: ")
    salario_str = input_seguro("Salario: ")
    salario = validar_salario(salario_str)
    
    empleado_dto = EmpleadoDTO(
        nombre=nombre,
        email=email,
        direccion=direccion,
        telefono=telefono,
        salario=salario,
        inicio_contrato=date.today()
    )
    
    if empleado_dao.crear(empleado_dto):
        print("Empleado creado exitosamente.")
    else:
        print("Error al crear empleado.")

def listar_empleados():
    print("\n--- LISTADO DE EMPLEADOS ---")
    
    empleados_data = empleado_dao.obtener_con_departamento()
    
    if not empleados_data:
        print("No hay empleados registrados.")
        return
    
    for emp in empleados_data:
        depto_nombre = emp.get('departamento_nombre') or 'Sin asignar'
        print(f"ID: {emp['id']} | {emp['nombre']} | Email: {emp['email']} | "
              f"Salario: ${emp['salario']} | Departamento: {depto_nombre}")

def buscar_empleado():
    emp_id = input_seguro("ID del empleado: ")
    try:
        empleado = empleado_dao.obtener_por_id(int(emp_id))
        if empleado:
            print(f"\n--- EMPLEADO ENCONTRADO ---")
            print(f"ID: {empleado.id}")
            print(f"Nombre: {empleado.nombre}")
            print(f"Email: {empleado.email}")
            print(f"Dirección: {empleado.direccion}")
            print(f"Teléfono: {empleado.telefono}")
            print(f"Salario: ${empleado.salario}")
            print(f"Inicio contrato: {empleado.inicio_contrato}")
        else:
            print("Empleado no encontrado.")
    except ValueError:
        print("ID inválido.")

def actualizar_empleado():
    emp_id = input_seguro("ID del empleado a actualizar: ")
    try:
        empleado = empleado_dao.obtener_por_id(int(emp_id))
        if not empleado:
            print("Empleado no encontrado.")
            return
        
        print(f"\nActualizando empleado: {empleado.nombre}")
        print("(Presiona Enter para mantener el valor actual)")
        
        nuevo_nombre = input_seguro(f"Nombre [{empleado.nombre}]: ") or empleado.nombre
        nuevo_email = input_seguro(f"Email [{empleado.email}]: ") or empleado.email
        nueva_direccion = input_seguro(f"Dirección [{empleado.direccion}]: ") or empleado.direccion
        nuevo_telefono = input_seguro(f"Teléfono [{empleado.telefono}]: ") or empleado.telefono
        nuevo_salario_str = input_seguro(f"Salario [{empleado.salario}]: ")
        nuevo_salario = validar_salario(nuevo_salario_str) if nuevo_salario_str else empleado.salario
        
        empleado_actualizado = EmpleadoDTO(
            id=empleado.id,
            nombre=nuevo_nombre,
            email=nuevo_email,
            direccion=nueva_direccion,
            telefono=nuevo_telefono,
            salario=nuevo_salario,
            inicio_contrato=empleado.inicio_contrato,
            departamento_id=empleado.departamento_id
        )
        
        if empleado_dao.actualizar(empleado_actualizado):
            print("Empleado actualizado exitosamente.")
        else:
            print("Error al actualizar empleado.")
            
    except ValueError:
        print("ID inválido.")

def asignar_empleado_departamento():
    emp_id = input_seguro("ID Empleado: ")
    dept_id = input_seguro("ID Departamento: ")
    
    try:
        if empleado_dao.asignar_departamento(int(emp_id), int(dept_id)):
            print("Empleado asignado al departamento.")
        else:
            print("Error en la asignación.")
    except ValueError:
        print("IDs inválidos.")

def eliminar_empleado():
    emp_id = input_seguro("ID del empleado a eliminar: ")
    try:
        empleado = empleado_dao.obtener_por_id(int(emp_id))
        if not empleado:
            print("Empleado no encontrado.")
            return
        
        confirmar = input(f"¿Está seguro de eliminar a {empleado.nombre}? (s/N): ")
        if confirmar.lower() == 's':
            if empleado_dao.eliminar(int(emp_id)):
                print("Empleado eliminado.")
            else:
                print("Error al eliminar empleado.")
        else:
            print("Operación cancelada.")
    except ValueError:
        print("ID inválido.")

def menu_departamentos():
    while True:
        print("\n--- GESTIÓN DEPARTAMENTOS ---")
        print("1. Crear Departamento")
        print("2. Listar Departamentos")
        print("3. Buscar Departamento")
        print("4. Actualizar Departamento")
        print("5. Eliminar Departamento")
        print("6. Volver")
        
        opcion = input("Opción: ")
        
        if opcion == '1':
            crear_departamento()
        elif opcion == '2':
            listar_departamentos()
        elif opcion == '3':
            buscar_departamento()
        elif opcion == '4':
            actualizar_departamento()
        elif opcion == '5':
            eliminar_departamento()
        elif opcion == '6':
            break

def crear_departamento():
    print("\n--- CREAR DEPARTAMENTO ---")
    
    nombre = input_seguro("Nombre del departamento: ")
    gerente = input_seguro("Nombre del gerente: ")
    
    departamento_dto = DepartamentoDTO(
        nombre=nombre,
        gerente=gerente
    )
    
    if departamento_dao.crear(departamento_dto):
        print("Departamento creado exitosamente.")
    else:
        print("Error al crear departamento.")

def listar_departamentos():
    print("\n--- LISTADO DE DEPARTAMENTOS ---")
    
    departamentos = departamento_dao.obtener_todos()
    
    if not departamentos:
        print("No hay departamentos registrados.")
        return
    
    for dept in departamentos:
        print(f"ID: {dept.id} | Nombre: {dept.nombre} | Gerente: {dept.gerente}")

def buscar_departamento():
    dept_id = input_seguro("ID del departamento: ")
    try:
        departamento = departamento_dao.obtener_por_id(int(dept_id))
        if departamento:
            print(f"\n--- DEPARTAMENTO ENCONTRADO ---")
            print(f"ID: {departamento.id}")
            print(f"Nombre: {departamento.nombre}")
            print(f"Gerente: {departamento.gerente}")
        else:
            print("Departamento no encontrado.")
    except ValueError:
        print("ID inválido.")

def actualizar_departamento():
    dept_id = input_seguro("ID del departamento a actualizar: ")
    try:
        departamento = departamento_dao.obtener_por_id(int(dept_id))
        if not departamento:
            print("Departamento no encontrado.")
            return
        
        print(f"\nActualizando departamento: {departamento.nombre}")
        nuevo_nombre = input_seguro(f"Nombre [{departamento.nombre}]: ") or departamento.nombre
        nuevo_gerente = input_seguro(f"Gerente [{departamento.gerente}]: ") or departamento.gerente
        
        departamento_actualizado = DepartamentoDTO(
            id=departamento.id,
            nombre=nuevo_nombre,
            gerente=nuevo_gerente
        )
        
        if departamento_dao.actualizar(departamento_actualizado):
            print("Departamento actualizado exitosamente.")
        else:
            print("Error al actualizar departamento.")
            
    except ValueError:
        print("ID inválido.")

def eliminar_departamento():
    dept_id = input_seguro("ID del departamento a eliminar: ")
    try:
        departamento = departamento_dao.obtener_por_id(int(dept_id))
        if not departamento:
            print("Departamento no encontrado.")
            return
        
        confirmar = input(f"¿Está seguro de eliminar el departamento '{departamento.nombre}'? (s/N): ")
        if confirmar.lower() == 's':
            if departamento_dao.eliminar(int(dept_id)):
                print("Departamento eliminado.")
            else:
                print("Error al eliminar departamento.")
        else:
            print("Operación cancelada.")
    except ValueError:
        print("ID inválido.")

def menu_proyectos():
    while True:
        print("\n--- GESTIÓN PROYECTOS ---")
        print("1. Crear Proyecto")
        print("2. Listar Proyectos")
        print("3. Asignar Empleado a Proyecto")
        print("4. Registrar Horas de Trabajo")
        print("5. Eliminar Proyecto")
        print("6. Volver")
        
        opcion = input("Opción: ")
        
        if opcion == '1':
            crear_proyecto()
        elif opcion == '2':
            listar_proyectos()
        elif opcion == '3':
            asignar_empleado_proyecto()
        elif opcion == '4':
            registrar_horas()
        elif opcion == '5':
            eliminar_proyecto()
        elif opcion == '6':
            break

def crear_proyecto():
    print("\n--- CREAR PROYECTO ---")
    
    nombre = input_seguro("Nombre del proyecto: ")
    descripcion = input_seguro("Descripción: ")
    
    proyecto_dto = ProyectoDTO(
        nombre=nombre,
        descripcion=descripcion,
        fecha_inicio=date.today()
    )
    
    if proyecto_dao.crear(proyecto_dto):
        print("Proyecto creado exitosamente.")
    else:
        print("Error al crear proyecto.")

def listar_proyectos():
    print("\n--- LISTADO DE PROYECTOS ---")
    
    proyectos = proyecto_dao.obtener_todos()
    
    if not proyectos:
        print("No hay proyectos registrados.")
        return
    
    for proy in proyectos:
        print(f"ID: {proy.id} | Proyecto: {proy.nombre} | Inicio: {proy.fecha_inicio}")
        print(f"   Descripción: {proy.descripcion}")

def asignar_empleado_proyecto():
    emp_id = input_seguro("ID Empleado: ")
    proy_id = input_seguro("ID Proyecto: ")
    
    try:
        if proyecto_dao.asignar_empleado(int(emp_id), int(proy_id)):
            print("Empleado asignado al proyecto.")
        else:
            print("Error en la asignación (posiblemente ya está asignado).")
    except ValueError:
        print("IDs inválidos.")

def registrar_horas():
    emp_id = input_seguro("ID Empleado: ")
    proy_id = input_seguro("ID Proyecto: ")
    horas_str = input_seguro("Horas trabajadas: ")
    descripcion = input_seguro("Descripción del trabajo realizado: ")
    
    try:
        horas = float(horas_str)
        if proyecto_dao.registrar_tiempo(int(emp_id), int(proy_id), horas, descripcion):
            print("Tiempo registrado correctamente.")
        else:
            print("Error al registrar tiempo.")
    except ValueError:
        print("Datos inválidos.")

def eliminar_proyecto():
    proy_id = input_seguro("ID del proyecto a eliminar: ")
    try:
        proyecto = proyecto_dao.obtener_por_id(int(proy_id))
        if not proyecto:
            print("Proyecto no encontrado.")
            return
        
        confirmar = input(f"¿Está seguro de eliminar el proyecto '{proyecto.nombre}'? (s/N): ")
        if confirmar.lower() == 's':
            if proyecto_dao.eliminar(int(proy_id)):
                print("Proyecto eliminado.")
            else:
                print("Error al eliminar proyecto.")
        else:
            print("Operación cancelada.")
    except ValueError:
        print("ID inválido.")

def menu_indicadores(usuario: str):
    print("\n--- INDICADORES ECONÓMICOS ---")
    print("Indicadores disponibles: uf, dolar, euro, utm, ipc, ivp")
    indicador = input("Indicador: ").lower()
    fecha_consulta = input("Fecha (dd-mm-yyyy) [Enter para hoy]: ")
    
    print("Consultando API externa...")
    valor, fecha_respuesta = consultar_indicadores(indicador, fecha_consulta if fecha_consulta else None)
    
    if valor:
        print(f"Resultado: {indicador.upper()} = {valor} (Fecha: {fecha_respuesta})")
        
        # Obtener datos del usuario actual para almacenar en el historial
        usuario_actual = usuario_dao.obtener_por_username(usuario)
        datos_empleado = None
        
        if usuario_actual:
            # Buscar si el usuario tiene un perfil de empleado asociado
            try:
                with db_connection.cursor() as cursor:
                    sql = "SELECT nombre, email, salario, d.nombre as departamento FROM empleados e LEFT JOIN departamentos d ON e.departamento_id = d.id WHERE e.email LIKE %s OR e.nombre LIKE %s LIMIT 1"
                    cursor.execute(sql, (f"%{usuario}%", f"%{usuario}%"))
                    datos_empleado = cursor.fetchone()
            except Exception as e:
                print(f"Error al buscar datos del empleado: {e}")
        
        # Guardar en historial con datos completos
        try:
            with db_connection.cursor() as cursor:
                fecha_sql = fecha_respuesta[:10] if fecha_respuesta else None
                
                if datos_empleado:
                    sql = """INSERT INTO indicadores_economicos 
                           (indicador, valor, fecha_valor, usuario_consulta, empleado_nombre, 
                            empleado_correo, empleado_salario, empleado_departamento) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (
                        indicador, valor, fecha_sql, usuario,
                        datos_empleado['nombre'], 
                        datos_empleado['email'],
                        float(datos_empleado['salario']) if datos_empleado['salario'] else 0.0,
                        datos_empleado['departamento'] or 'Sin asignar'
                    ))
                else:
                    # Si no encuentra datos del empleado, guardar solo datos básicos
                    sql = """INSERT INTO indicadores_economicos 
                           (indicador, valor, fecha_valor, usuario_consulta, empleado_nombre) 
                           VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (indicador, valor, fecha_sql, usuario, usuario))
                
                print("Consulta guardada en el historial con datos del empleado.")
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    else:
        print(f"Error en consulta: {fecha_respuesta}")
def menu_reportes():
    print("\n--- GENERAR REPORTES ---")
    print("1. Reporte de Empleados (Excel)")
    print("2. Reporte de Proyectos (PDF)")
    print("3. Reporte de Registro de Tiempos (Excel)")
    print("4. Historial de Consultas de Indicadores")
    print("5. Volver")
    
    opcion = input("Opción: ")
    
    if opcion == '1':
        generar_reporte_empleados()
    elif opcion == '2':
        generar_reporte_proyectos()
    elif opcion == '3':
        generar_reporte_tiempos()
    elif opcion == '4':
        mostrar_historial_indicadores()
    elif opcion == '5':
        return

def generar_reporte_empleados():
    empleados_data = empleado_dao.obtener_con_departamento()
    
    if empleados_data:
        datos_excel = []
        for emp in empleados_data:
            datos_excel.append({
                'ID': emp['id'],
                'Nombre': emp['nombre'],
                'Email': emp['email'],
                'Salario': emp['salario'],
                'Departamento': emp.get('departamento_nombre') or 'Sin asignar'
            })
        
        generar_excel(datos_excel, "Reporte_Empleados.xlsx")
    else:
        print("No hay empleados para reportar.")

def generar_reporte_proyectos():
    proyectos = proyecto_dao.obtener_todos()
    
    if proyectos:
        lista_texto = []
        for proy in proyectos:
            lista_texto.append(f"• {proy.nombre} (Inicio: {proy.fecha_inicio})")
            lista_texto.append(f"  Descripción: {proy.descripcion}")
            lista_texto.append("")
        
        generar_pdf("Listado de Proyectos", lista_texto, "Reporte_Proyectos.pdf")
    else:
        print("No hay proyectos para reportar.")

def generar_reporte_tiempos():
    datos_tiempos = proyecto_dao.obtener_reporte_tiempos()
    
    if datos_tiempos:
        generar_excel(datos_tiempos, "Reporte_Tiempos.xlsx")
    else:
        print("No hay registros de tiempo para reportar.")

def mostrar_historial_indicadores():
    print("\n--- HISTORIAL DE CONSULTAS DE INDICADORES ---")
    
    try:
        with db_connection.cursor() as cursor:
            sql = """SELECT indicador, valor, fecha_valor, fecha_consulta, usuario_consulta, 
                           empleado_nombre, empleado_correo, empleado_salario, empleado_departamento 
                    FROM indicadores_economicos 
                    ORDER BY fecha_consulta DESC 
                    LIMIT 20"""
            cursor.execute(sql)
            consultas = cursor.fetchall()
            
            if not consultas:
                print("No hay consultas de indicadores registradas.")
                return
            
            for consulta in consultas:
                print(f"\n📊 {consulta['indicador'].upper()}: {consulta['valor']}")
                print(f"   Fecha del indicador: {consulta['fecha_valor']}")
                print(f"   Consultado: {consulta['fecha_consulta']}")
                print(f"   Usuario: {consulta['usuario_consulta']}")
                
                if consulta['empleado_nombre']:
                    print(f"   Empleado: {consulta['empleado_nombre']}")
                    print(f"   Email: {consulta['empleado_correo'] or 'N/A'}")
                    print(f"   Salario: ${consulta['empleado_salario'] or 'N/A'}")
                    print(f"   Departamento: {consulta['empleado_departamento'] or 'N/A'}")
                
                print("   " + "-" * 50)
                
    except Exception as e:
        print(f"Error al obtener historial: {e}")

def inicializar_sistema():
    try:
        if usuario_dao.contar_usuarios() == 0:
            print("\n=== INICIALIZACIÓN DEL SISTEMA ===")
            print("No hay usuarios en el sistema.")
            print("Se creará automáticamente un usuario administrador por defecto.")
            print("Credenciales: admin/admin123")
            print("El administrador puede crear nuevos usuarios desde el menú de gestión.")
            
            admin_dto = UsuarioDTO(
                username="admin",
                password="admin123",
                rol="admin"
            )
            
            if usuario_dao.crear(admin_dto):
                print("Usuario administrador creado exitosamente.")
            else:
                print("Error al crear el usuario administrador por defecto.")
    except Exception as e:
        print(f"[ERROR] Error en inicialización: {e}")

def menu_usuarios():
    while True:
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("1. Crear Usuario")
        print("2. Listar Usuarios")
        print("3. Actualizar Usuario")
        print("4. Eliminar Usuario")
        print("5. Volver")
        
        opcion = input("Opción: ")
        
        if opcion == '1':
            crear_usuario()
        elif opcion == '2':
            listar_usuarios()
        elif opcion == '3':
            actualizar_usuario_menu()
        elif opcion == '4':
            eliminar_usuario()
        elif opcion == '5':
            break

def crear_usuario():
    print("\n--- CREAR USUARIO ---")
    
    username = input_seguro("Nombre de usuario: ")
    
    # Verificar que el username no exista
    if usuario_dao.obtener_por_username(username):
        print("El nombre de usuario ya existe.")
        return
    
    password = input_seguro("Contraseña: ")
    
    print("Roles disponibles:")
    print("1. admin - Acceso completo al sistema")
    print("2. empleado - Acceso limitado")
    
    rol_opcion = input("Seleccione el rol (1-2): ")
    
    if rol_opcion == '1':
        rol = 'admin'
    elif rol_opcion == '2':
        rol = 'empleado'
    else:
        print("Opción de rol inválida.")
        return
    
    usuario_dto = UsuarioDTO(
        username=username,
        password=password,
        rol=rol
    )
    
    if usuario_dao.crear(usuario_dto):
        print(f"Usuario '{username}' creado exitosamente con rol '{rol}'.")
    else:
        print("Error al crear usuario.")

def listar_usuarios():
    print("\n--- LISTADO DE USUARIOS ---")
    
    usuarios = usuario_dao.obtener_todos()
    
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    for usuario in usuarios:
        print(f"ID: {usuario.id} | Usuario: {usuario.username} | Rol: {usuario.rol}")

def actualizar_usuario_menu():
    user_id = input_seguro("ID del usuario a actualizar: ")
    try:
        usuario = usuario_dao.obtener_por_id(int(user_id))
        if not usuario:
            print("Usuario no encontrado.")
            return
        
        print(f"\nActualizando usuario: {usuario.username}")
        print("(Presiona Enter para mantener el valor actual)")
        
        nuevo_username = input_seguro(f"Nombre de usuario [{usuario.username}]: ") or usuario.username
        nueva_password = input_seguro("Nueva contraseña (dejar vacío para no cambiar): ")
        
        print(f"Rol actual: {usuario.rol}")
        print("1. admin - Acceso completo")
        print("2. empleado - Acceso limitado")
        rol_opcion = input("Nuevo rol (1-2) [Enter para mantener]: ")
        
        if rol_opcion == '1':
            nuevo_rol = 'admin'
        elif rol_opcion == '2':
            nuevo_rol = 'empleado'
        else:
            nuevo_rol = usuario.rol
        
        usuario_actualizado = UsuarioDTO(
            id=usuario.id,
            username=nuevo_username,
            password=nueva_password if nueva_password else "",
            rol=nuevo_rol
        )
        
        if usuario_dao.actualizar(usuario_actualizado):
            print("Usuario actualizado exitosamente.")
        else:
            print("Error al actualizar usuario.")
            
    except ValueError:
        print("ID inválido.")

def eliminar_usuario():
    user_id = input_seguro("ID del usuario a eliminar: ")
    try:
        usuario = usuario_dao.obtener_por_id(int(user_id))
        if not usuario:
            print("Usuario no encontrado.")
            return
        
        if usuario.username == 'admin':
            print("No se puede eliminar el usuario administrador principal.")
            return
        
        confirmar = input(f"¿Está seguro de eliminar al usuario '{usuario.username}'? (s/N): ")
        if confirmar.lower() == 's':
            if usuario_dao.eliminar(int(user_id)):
                print("Usuario eliminado.")
            else:
                print("Error al eliminar usuario.")
        else:
            print("Operación cancelada.")
    except ValueError:
        print("ID inválido.")

def menu_principal(usuario: str):
    # Obtener información del usuario actual para verificar permisos
    usuario_actual = usuario_dao.obtener_por_username(usuario)
    es_admin = usuario_actual and usuario_actual.rol == 'admin'
    
    while True:
        print(f"\n=== SISTEMA ECOTECH SOLUTIONS ===")
        print(f"Usuario: {usuario} | Rol: {usuario_actual.rol if usuario_actual else 'N/A'}")
        print("=" * 50)
        print("1. Gestión de Empleados")
        print("2. Gestión de Departamentos")
        print("3. Gestión de Proyectos y Tiempos")
        print("4. Consulta de Indicadores Económicos")
        print("5. Generar Reportes (PDF/Excel)")
        
        if es_admin:
            print("6. Gestión de Usuarios (Solo Admin)")
        
        print("0. Cerrar Sesión")
        
        if not es_admin:
            print("\n[NOTA] Acceso como empleado - Funciones limitadas")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            menu_empleados()
        elif opcion == '2':
            menu_departamentos()
        elif opcion == '3':
            menu_proyectos()
        elif opcion == '4':
            menu_indicadores(usuario)
        elif opcion == '5':
            menu_reportes()
        elif opcion == '6' and es_admin:
            menu_usuarios()
        elif opcion == '0':
            print("Sesión cerrada. ¡Hasta luego!")
            break
        else:
            if opcion == '6' and not es_admin:
                print("Acceso denegado. Solo los administradores pueden gestionar usuarios.")
            else:
                print("Opción inválida.")

def main():
    if not db_connection:
        print("FATAL: No se pudo conectar a la Base de Datos. Revisa XAMPP y la configuración.")
        return
    
    print("=== SISTEMA DE GESTIÓN DE EMPLEADOS ECOTECH ===")
    
    # Inicializar sistema (crear admin si no existe ningún usuario)
    inicializar_sistema()
    
    # Login directo
    usuario_actual = login()
    if not usuario_actual:
        print("No se pudo autenticar. Saliendo del sistema.")
        return
    
    menu_principal(usuario_actual)

if __name__ == "__main__":
    main()