# Guía de Despliegue - GitHub y Vercel

Esta guía te ayudará a subir tu proyecto a GitHub y desplegarlo en Vercel.

## 📦 Paso 1: Subir a GitHub

### Opción A: Usando los scripts de PowerShell

1. **Configurar Git (primera vez):**
   ```powershell
   .\setup_github.ps1
   ```

2. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Crea un nuevo repositorio
   - **NO** inicialices con README, .gitignore o licencia
   - Copia la URL del repositorio (ej: `https://github.com/tu-usuario/tu-repo.git`)

3. **Subir código:**
   ```powershell
   .\deploy_to_github.ps1 -RepositoryUrl "https://github.com/tu-usuario/tu-repo.git"
   ```

### Opción B: Manualmente

1. **Inicializar Git (si no lo has hecho):**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: Sistema de Gestión de Campeonatos de Básquetbol"
   ```

2. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Crea un nuevo repositorio
   - **NO** inicialices con README, .gitignore o licencia

3. **Conectar y subir:**
   ```powershell
   git remote add origin https://github.com/tu-usuario/tu-repo.git
   git branch -M main
   git push -u origin main
   ```

## 🚀 Paso 2: Desplegar en Vercel

### Opción A: Desde la interfaz web de Vercel

1. **Instalar Vercel CLI (opcional pero recomendado):**
   ```powershell
   npm install -g vercel
   ```

2. **Ir a Vercel:**
   - Ve a https://vercel.com
   - Inicia sesión con tu cuenta (puedes usar GitHub)

3. **Importar proyecto:**
   - Haz clic en "Add New Project"
   - Selecciona "Import Git Repository"
   - Conecta tu cuenta de GitHub si es necesario
   - Selecciona tu repositorio
   - Vercel detectará automáticamente la configuración de Python

4. **Configurar proyecto:**
   - Framework Preset: Other
   - Build Command: (dejar vacío)
   - Output Directory: (dejar vacío)
   - Install Command: `pip install -r requirements.txt`
   - Haz clic en "Deploy"

### Opción B: Desde la línea de comandos

1. **Instalar Vercel CLI:**
   ```powershell
   npm install -g vercel
   ```

2. **Iniciar sesión:**
   ```powershell
   vercel login
   ```

3. **Desplegar:**
   ```powershell
   vercel
   ```
   - Sigue las instrucciones en pantalla
   - Para producción: `vercel --prod`

## 📋 Verificación

### Verificar en GitHub:
- Tu código debe estar visible en: `https://github.com/tu-usuario/tu-repo`

### Verificar en Vercel:
- Tu API estará disponible en: `https://tu-proyecto.vercel.app`
- Endpoint raíz: `https://tu-proyecto.vercel.app/`
- Endpoint de API: `https://tu-proyecto.vercel.app/api/championships`

## 🧪 Probar la API

Una vez desplegado, puedes probar la API con:

```bash
# Obtener información de la API
curl https://tu-proyecto.vercel.app/

# Crear un campeonato
curl -X POST https://tu-proyecto.vercel.app/api/championships \
  -H "Content-Type: application/json" \
  -d '{
    "id": "champ1",
    "name": "Campeonato 2024",
    "rounds": 1,
    "points_per_win": 2
  }'
```

## 🔧 Configuración de Vercel

El proyecto ya incluye:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `api/index.py` - Punto de entrada para serverless functions
- ✅ `.gitignore` - Archivos a ignorar

## 📝 Notas Importantes

1. **Variables de entorno:** Si necesitas variables de entorno, configúralas en el dashboard de Vercel (Settings > Environment Variables)

2. **Límites de Vercel:**
   - Las funciones serverless tienen un timeout de 10 segundos (hobby) o 60 segundos (pro)
   - El almacenamiento en memoria se pierde entre invocaciones (considera usar una base de datos para producción)

3. **Base de datos:** Para producción, considera usar:
   - Vercel Postgres
   - MongoDB Atlas
   - Supabase
   - O cualquier otra base de datos compatible

## 🐛 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` incluya todas las dependencias
- Asegúrate de que los imports en `api/index.py` sean correctos

### Error: "Handler not found"
- Verifica que `api/index.py` exporte `handler` o `application`

### Error al hacer push a GitHub
- Verifica tus credenciales: `git config --global user.name` y `git config --global user.email`
- Si usas autenticación por token, asegúrate de tener el token correcto

## 📚 Recursos

- [Documentación de Vercel](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [GitHub Guides](https://guides.github.com/)

