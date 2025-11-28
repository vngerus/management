# Instrucciones — configurar y ejecutar la app

1. Crear y activar el entorno virtual (desde la carpeta `management/`):

```bash
python -m venv .venv

source .venv/Scripts/activate
```

2. Actualizar herramientas e instalar dependencias:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3. Variables de entorno / configuración (opcional):

```bash
cp .env.example .env
```

4. Inicializar la base de datos (si usas la DB local/XAMPP):

```bash
python scripts/setup_database.py
```

5. Ejecutar la aplicación:

```bash
python main.py
```
