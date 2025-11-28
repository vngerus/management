CREATE DATABASE IF NOT EXISTS mgmt_employee CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mgmt_employee;


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) DEFAULT 'admin'
);

CREATE TABLE IF NOT EXISTS departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    gerente VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE
);

CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion_enc TEXT,
    telefono_enc TEXT,  
    email VARCHAR(100) UNIQUE NOT NULL,
    inicio_contrato DATE,
    salario DECIMAL(10, 2),
    departamento_id INT,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS empleado_proyecto (
    empleado_id INT,
    proyecto_id INT,
    PRIMARY KEY (empleado_id, proyecto_id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS registro_tiempo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    proyecto_id INT,
    fecha DATE,
    horas DECIMAL(5, 2),
    descripcion TEXT,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS indicadores_economicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indicador VARCHAR(50) NOT NULL,
    valor DECIMAL(15, 4),
    fecha_valor DATE,      
    fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_consulta VARCHAR(50),
    empleado_nombre VARCHAR(100),
    empleado_correo VARCHAR(100),
    empleado_salario DECIMAL(10, 2),
    empleado_departamento VARCHAR(100),
    origen VARCHAR(100) DEFAULT 'mindicador.cl'
);