# 🚀 Instrucciones Rápidas - Despliegue

## Opción 1: Script Automatizado (MÁS FÁCIL) ⚡

Ejecuta este comando y sigue las instrucciones:

```powershell
.\deploy_completo.ps1
```

Este script te guiará paso a paso para:
1. ✅ Preparar los archivos
2. ✅ Subir a GitHub
3. ✅ Configurar Vercel

---

## Opción 2: Manual (Paso a Paso)

### 📦 Paso 1: Subir a GitHub

1. **Crea un repositorio en GitHub:**
   - Ve a: https://github.com/new
   - Nombre: `basketball-championship` (o el que prefieras)
   - **IMPORTANTE:** NO marques "Add a README file"
   - Haz clic en "Create repository"

2. **Copia la URL del repositorio:**
   - Ejemplo: `https://github.com/tu-usuario/basketball-championship.git`

3. **En PowerShell, ejecuta:**
   ```powershell
   git add .
   git commit -m "Initial commit: Sistema de Gestión de Campeonatos"
   git remote add origin https://github.com/tu-usuario/basketball-championship.git
   git branch -M main
   git push -u origin main
   ```

   ⚠️ **Si te pide credenciales:**
   - Usa un Personal Access Token de GitHub
   - Crea uno en: https://github.com/settings/tokens
   - Permisos: `repo` (todos los permisos de repositorio)

### 🚀 Paso 2: Desplegar en Vercel

#### Opción A: Desde la Web (Recomendado)

1. **Ve a Vercel:**
   - https://vercel.com
   - Inicia sesión con GitHub

2. **Importa tu proyecto:**
   - Haz clic en "Add New Project"
   - Selecciona "Import Git Repository"
   - Elige tu repositorio
   - Haz clic en "Import"

3. **Configuración:**
   - Framework Preset: **Other**
   - Build Command: (dejar vacío)
   - Output Directory: (dejar vacío)
   - Install Command: `pip install -r requirements.txt`
   - Root Directory: `./`

4. **Despliega:**
   - Haz clic en "Deploy"
   - Espera 1-2 minutos

5. **¡Listo!**
   - Tu API estará en: `https://tu-proyecto.vercel.app`

#### Opción B: Desde la CLI

```powershell
# Instalar Vercel CLI
npm install -g vercel

# Iniciar sesión
vercel login

# Desplegar
vercel

# Para producción
vercel --prod
```

---

## 🧪 Probar tu API

Una vez desplegado, prueba tu API:

```powershell
# Ver información de la API
curl https://tu-proyecto.vercel.app/

# Crear un campeonato
curl -X POST https://tu-proyecto.vercel.app/api/championships `
  -H "Content-Type: application/json" `
  -d '{\"id\":\"champ1\",\"name\":\"Campeonato 2024\",\"rounds\":1,\"points_per_win\":2}'
```

O desde el navegador:
- Ve a: `https://tu-proyecto.vercel.app/`
- Deberías ver la información de la API en JSON

---

## 📋 Checklist

Antes de desplegar, verifica:

- [ ] Todos los archivos están en el repositorio
- [ ] `requirements.txt` incluye Flask y flask-cors
- [ ] `vercel.json` está configurado correctamente
- [ ] `api/index.py` existe y exporta `handler`
- [ ] `.gitignore` incluye archivos temporales

---

## 🐛 Problemas Comunes

### Error: "Git no está instalado"
- Instala Git: https://git-scm.com/download/win

### Error: "Authentication failed" al hacer push
- Crea un Personal Access Token en GitHub
- Úsalo como contraseña cuando Git lo pida

### Error: "Module not found" en Vercel
- Verifica que `requirements.txt` tenga todas las dependencias
- Asegúrate de que los imports en `api/index.py` sean correctos

### Error: "Handler not found" en Vercel
- Verifica que `api/index.py` exporte `handler` o `application`

---

## 📚 Más Información

- Guía completa: [DEPLOY.md](DEPLOY.md)
- Documentación del proyecto: [README.md](README.md)

---

## ✅ ¡Listo!

Una vez desplegado, tu API estará disponible públicamente y podrás:
- Crear campeonatos
- Agregar categorías
- Registrar resultados
- Ver tablas de posiciones
- Obtener fixtures

¡Feliz despliegue! 🎉


