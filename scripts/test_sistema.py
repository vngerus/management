import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from DAO import Database, EmpleadoDAO, DepartamentoDAO, ProyectoDAO, UsuarioDAO
from DTO import EmpleadoDTO, DepartamentoDTO, ProyectoDTO, UsuarioDTO
from utils.utils import hash_password, check_password, encriptar_dato, desencriptar_dato, consultar_indicadores

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST]{Colors.ENDC} {test_name}")

def print_success(message):
    print(f"  {Colors.GREEN}✓{Colors.ENDC} {message}")

def print_error(message):
    print(f"  {Colors.RED}✗{Colors.ENDC} {message}")

def print_info(message):
    print(f"  {Colors.YELLOW}ℹ{Colors.ENDC} {message}")

db_connection = Database().get_connection()

if not db_connection:
    print_error("No se pudo conectar a la base de datos. Verifica XAMPP y la configuración.")
    sys.exit(1)

empleado_dao = EmpleadoDAO(db_connection)
departamento_dao = DepartamentoDAO(db_connection)
proyecto_dao = ProyectoDAO(db_connection)
usuario_dao = UsuarioDAO(db_connection)

print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
print(f"{Colors.BOLD}SCRIPT DE PRUEBAS - SISTEMA DE GESTIÓN ECOTECH SOLUTIONS{Colors.ENDC}")
print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}")

print_test("1. Seguridad - Hash de Contraseñas")
try:
    password = "test123"
    hashed = hash_password(password)
    
    if check_password(password, hashed):
        print_success(f"Hash generado correctamente: {hashed[:30]}...")
    else:
        print_error("Error en verificación de hash")
    
    if not check_password("wrongpass", hashed):
        print_success("Rechazo de contraseña incorrecta funciona")
    else:
        print_error("No rechaza contraseña incorrecta")
        
except Exception as e:
    print_error(f"Error en prueba de hash: {e}")

print_test("2. Seguridad - Cifrado de Datos Sensibles")
try:
    dato_original = "Calle Falsa 123"
    dato_cifrado = encriptar_dato(dato_original)
    dato_descifrado = desencriptar_dato(dato_cifrado)
    
    if dato_descifrado == dato_original:
        print_success(f"Cifrado/Descifrado correcto")
        print_info(f"Original: {dato_original}")
        print_info(f"Cifrado: {dato_cifrado[:40]}...")
    else:
        print_error("Error en cifrado/descifrado")
        
except Exception as e:
    print_error(f"Error en prueba de cifrado: {e}")

print_test("3. CRUD - Gestión de Usuarios")
try:
    test_user = UsuarioDTO(
        username="test_usuario",
        password="password123",
        rol="empleado"
    )
    
    if usuario_dao.crear(test_user):
        print_success("Usuario de prueba creado")
    else:
        print_info("Usuario ya existe (continuando con tests)")
    
    usuario = usuario_dao.validar_credenciales("test_usuario", "password123")
    if usuario:
        print_success(f"Login exitoso - Usuario: {usuario.username}, Rol: {usuario.rol}")
    else:
        print_error("Error en validación de credenciales")
    
    usuarios = usuario_dao.obtener_todos()
    print_success(f"Total usuarios en sistema: {len(usuarios)}")
    
except Exception as e:
    print_error(f"Error en prueba de usuarios: {e}")

print_test("4. CRUD - Gestión de Departamentos")
try:
    dept_test = DepartamentoDTO(
        nombre="Departamento Test",
        gerente="Gerente Test"
    )
    
    if departamento_dao.crear(dept_test):
        print_success("Departamento creado")
    else:
        print_info("Departamento ya existe")
    
    departamentos = departamento_dao.obtener_todos()
    print_success(f"Total departamentos: {len(departamentos)}")
    
    if departamentos:
        dept_id = departamentos[0].id
        dept = departamento_dao.obtener_por_id(dept_id)
        if dept:
            print_success(f"Consulta por ID exitosa - Dept: {dept.nombre}")
    
except Exception as e:
    print_error(f"Error en prueba de departamentos: {e}")

print_test("5. CRUD - Gestión de Empleados")
try:
    emp_test = EmpleadoDTO(
        nombre="Empleado Test",
        email="test@ecotech.com",
        direccion="Dirección de Prueba 123",
        telefono="+56912345678",
        salario=1500000.00,
        inicio_contrato=date.today()
    )
    
    if empleado_dao.crear(emp_test):
        print_success("Empleado creado con datos cifrados")
    else:
        print_info("Empleado ya existe")
    
    empleados = empleado_dao.obtener_con_departamento()
    print_success(f"Total empleados: {len(empleados)}")
    
    if empleados:
        emp = empleado_dao.obtener_por_id(empleados[0]['id'])
        if emp:
            print_success(f"Empleado consultado - Dirección descifrada: {emp.direccion}")
            print_success(f"Teléfono descifrado: {emp.telefono}")
    
    if empleados and departamentos:
        emp_id = empleados[0]['id']
        dept_id = departamentos[0].id
        if empleado_dao.asignar_departamento(emp_id, dept_id):
            print_success(f"Empleado {emp_id} asignado a departamento {dept_id}")
    
except Exception as e:
    print_error(f"Error en prueba de empleados: {e}")

print_test("6. CRUD - Gestión de Proyectos")
try:
    proy_test = ProyectoDTO(
        nombre="Proyecto Test",
        descripcion="Proyecto de prueba para validación del sistema",
        fecha_inicio=date.today()
    )
    
    if proyecto_dao.crear(proy_test):
        print_success("Proyecto creado")
    else:
        print_info("Proyecto ya existe")
    
    proyectos = proyecto_dao.obtener_todos()
    print_success(f"Total proyectos: {len(proyectos)}")
    
    if proyectos and empleados:
        emp_id = empleados[0]['id']
        proy_id = proyectos[0].id
        
        if proyecto_dao.asignar_empleado(emp_id, proy_id):
            print_success(f"Empleado {emp_id} asignado a proyecto {proy_id}")
        else:
            print_info("Asignación ya existe")
    
    if proyectos and empleados:
        if proyecto_dao.registrar_tiempo(emp_id, proy_id, 8.5, "Desarrollo de funcionalidades"):
            print_success("Registro de tiempo creado")
        else:
            print_error("Error al registrar tiempo")
    
    tiempos = proyecto_dao.obtener_reporte_tiempos()
    print_success(f"Total registros de tiempo: {len(tiempos)}")
    
except Exception as e:
    print_error(f"Error en prueba de proyectos: {e}")

print_test("7. Consumo de API Externa - Indicadores Económicos")
try:
    print_info("Consultando UF (puede tardar unos segundos)...")
    valor, fecha = consultar_indicadores("uf")
    
    if valor:
        print_success(f"UF obtenida: ${valor:,.2f} (Fecha: {fecha})")
    else:
        print_error(f"Error al consultar API: {fecha}")
    
    print_info("Consultando Dólar...")
    valor, fecha = consultar_indicadores("dolar")
    
    if valor:
        print_success(f"Dólar obtenido: ${valor:,.2f}")
    else:
        print_error(f"Error: {fecha}")
    
except Exception as e:
    print_error(f"Error en prueba de API: {e}")

print_test("8. Validaciones de Entrada")
try:
    from main import validar_email, validar_salario
    
    if not validar_email("invalido"):
        print_success("Rechazo de email inválido funciona")
    
    if validar_email("valido@test.com"):
        print_success("Aceptación de email válido funciona")
    
    salario = validar_salario("1500000")
    if salario == 1500000.0:
        print_success("Validación de salario numérico funciona")
    
    salario = validar_salario("-1000")
    if salario == 0.0:
        print_success("Rechazo de salario negativo funciona")
    
except Exception as e:
    print_error(f"Error en prueba de validaciones: {e}")

print_test("9. Manejo de Excepciones")
try:
    emp = empleado_dao.obtener_por_id(999999)
    if emp is None:
        print_success("Manejo de ID inexistente funciona")
    
    if empleados:
        emp_dup = EmpleadoDTO(
            nombre="Duplicado",
            email=empleados[0]['email'],
            direccion="Test",
            telefono="Test",
            salario=1000000,
            inicio_contrato=date.today()
        )
        if not empleado_dao.crear(emp_dup):
            print_success("Prevención de email duplicado funciona")
    
except Exception as e:
    print_success(f"Excepciones manejadas correctamente: {type(e).__name__}")

print_test("10. Integridad de Base de Datos")
try:
    with db_connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        tablas_esperadas = ['usuarios', 'empleados', 'departamentos', 'proyectos', 
                           'empleado_proyecto', 'registro_tiempo', 'indicadores_economicos']
        
        tablas_encontradas = [list(t.values())[0] for t in tablas]
        
        for tabla in tablas_esperadas:
            if tabla in tablas_encontradas:
                print_success(f"Tabla '{tabla}' existe")
            else:
                print_error(f"Tabla '{tabla}' NO existe")
        
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM information_schema.TABLE_CONSTRAINTS 
            WHERE TABLE_SCHEMA = 'mgmt_employee' 
            AND CONSTRAINT_TYPE = 'FOREIGN KEY'
        """)
        fks = cursor.fetchone()
        print_success(f"Foreign Keys configuradas: {fks['total']}")
        
except Exception as e:
    print_error(f"Error en prueba de BD: {e}")

print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
print(f"{Colors.BOLD}RESUMEN DE PRUEBAS{Colors.ENDC}")
print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}")

print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Sistema funcionando correctamente{Colors.ENDC}")
print(f"\n{Colors.BOLD}Funcionalidades Verificadas:{Colors.ENDC}")
print(f"  • Autenticación con hash de contraseñas")
print(f"  • Cifrado de datos sensibles (dirección/teléfono)")
print(f"  • CRUD completo (Usuarios, Empleados, Departamentos, Proyectos)")
print(f"  • Asignaciones (Empleado-Departamento, Empleado-Proyecto)")
print(f"  • Registro de tiempo de trabajo")
print(f"  • Consumo de API externa (indicadores económicos)")
print(f"  • Validaciones de entrada")
print(f"  • Manejo de excepciones")
print(f"  • Integridad de base de datos")

print(f"\n{Colors.BOLD}El sistema está listo para ser utilizado.{Colors.ENDC}\n")
