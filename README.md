# Sistema de Gestión de Campeonatos de Básquetbol

Sistema completo y robusto para administrar campeonatos de básquetbol con múltiples categorías, generación automática de fixtures y gestión de tablas de posiciones.

## Características

### ✅ Configuración del Campeonato
- Configuración de cantidad de vueltas (1 o más)
- Gestión de múltiples categorías (TC, Senior, Super Senior)
- Configuración personalizada de puntos por victoria/derrota por categoría

### ✅ Generación Automática de Fixtures
- Generación automática de calendarios usando algoritmo round-robin
- Soporte para partidos ida y vuelta
- Evita duplicación incorrecta de emparejamientos
- Salida estructurada en formato JSON

### ✅ Tabla de Posiciones
- Tabla independiente por categoría
- Estadísticas completas: PJ, PG, PP, PF, PC, Diferencia, Puntos
- Configuración de puntos por victoria/derrota
- Sistema de multas/restricciones de puntos
- Recalculo automático al ingresar resultados

### ✅ Gestión de Resultados
- Registro de resultados de partidos
- Actualización automática de estadísticas
- Actualización automática de tabla de posiciones

## Estructura del Proyecto

```
.
├── championship.py      # Clase principal Championship
├── category.py          # Clase Category (gestión de categorías)
├── team.py              # Clase Team (equipos)
├── match.py             # Clase Match (partidos)
├── standings.py         # Clase Standings (tabla de posiciones)
├── fixture_generator.py # Generador de fixtures
├── main.py              # Archivo principal con ejemplos
└── README.md           # Este archivo
```

## Instalación

No se requieren dependencias externas. El sistema utiliza solo la biblioteca estándar de Python 3.6+.

```bash
# Clonar o descargar el proyecto
# No se requiere instalación adicional
```

## Uso Básico

### Crear un Campeonato

```python
from championship import Championship

# Crear campeonato con 2 vueltas
champ = Championship(
    name="Campeonato Local 2024",
    rounds=2,
    points_per_win=2,
    points_per_loss=0
)
```

### Agregar Categorías

```python
# Opción 1: Agregar con número de equipos (nombres automáticos)
champ.add_category("TC", num_teams=4)
champ.add_category("Senior", num_teams=3)

# Opción 2: Agregar con nombres de equipos personalizados
champ.add_category_with_teams(
    "Super Senior",
    ["Equipo A", "Equipo B", "Equipo C", "Equipo D"]
)

# Opción 3: Con configuración personalizada de puntos
champ.add_category_with_teams(
    "TC",
    ["Los Leones", "Los Tigres", "Los Halcones"],
    points_per_win=3,  # 3 puntos por victoria
    points_per_loss=0
)
```

### Registrar Resultados

```python
# Registrar resultado de un partido
champ.register_match_result(
    category_name="TC",
    team_a="Los Leones",
    team_b="Los Tigres",
    round_number=1,
    score_a=95,  # Puntos del equipo A
    score_b=82   # Puntos del equipo B
)
```

### Consultar Tabla de Posiciones

```python
# Obtener tabla de posiciones ordenada
standings = champ.get_standings("TC")

for pos, team in enumerate(standings, 1):
    print(f"{pos}. {team.name} - {team.points} puntos")
```

### Aplicar Multas/Bonificaciones

```python
# Restar 2 puntos (multa)
champ.apply_penalty("TC", "Los Leones", 2)

# Sumar 1 punto (bonificación)
champ.apply_penalty("TC", "Los Tigres", -1)
```

### Obtener Fixture

```python
category = champ.get_category("TC")

# Todos los partidos
all_matches = category.matches

# Partidos de una vuelta específica
matches_round_1 = category.get_matches_by_round(1)

# Partidos de un equipo
team_matches = category.get_matches_by_team("Los Leones")
```

### Exportar a JSON

```python
import json

# Exportar todo el campeonato
data = champ.to_dict()
json_output = json.dumps(data, indent=2, ensure_ascii=False)

# Guardar en archivo
with open("championship.json", "w", encoding="utf-8") as f:
    f.write(json_output)
```

## Ejecutar Ejemplos

El archivo `main.py` contiene ejemplos completos de uso:

```bash
python main.py
```

Esto ejecutará tres ejemplos:
1. **Ejemplo básico**: Campeonato simple con una vuelta
2. **Ejemplo completo**: Campeonato con múltiples vueltas y equipos personalizados
3. **Ejemplo de exportación**: Generación de archivo JSON

## Clases Principales

### Championship
Clase principal que gestiona el campeonato completo.

**Métodos principales:**
- `add_category()`: Agrega categoría con número de equipos
- `add_category_with_teams()`: Agrega categoría con nombres de equipos
- `register_match_result()`: Registra resultado de partido
- `get_standings()`: Obtiene tabla de posiciones
- `apply_penalty()`: Aplica multa/bonificación
- `to_dict()`: Exporta a diccionario/JSON

### Category
Gestiona una categoría con sus equipos, partidos y tabla.

**Métodos principales:**
- `add_teams()`: Agrega equipos
- `generate_fixture()`: Genera fixture automáticamente
- `register_match_result()`: Registra resultado
- `get_standings()`: Obtiene tabla de posiciones
- `get_matches_by_round()`: Filtra partidos por vuelta
- `get_matches_by_team()`: Filtra partidos por equipo

### Team
Representa un equipo con sus estadísticas.

**Propiedades:**
- `pj`: Partidos jugados
- `pg`: Partidos ganados
- `pp`: Partidos perdidos
- `pf`: Puntos a favor
- `pc`: Puntos en contra
- `points`: Puntos totales
- `penalty_points`: Puntos de multa

### Match
Representa un partido entre dos equipos.

**Propiedades:**
- `team_a`, `team_b`: Equipos participantes
- `round_number`: Número de vuelta
- `match_type`: 'ida' o 'vuelta'
- `played`: Si el partido ya se jugó
- `score_a`, `score_b`: Resultados
- `winner`: Equipo ganador

### Standings
Gestiona la tabla de posiciones de una categoría.

**Métodos principales:**
- `add_team()`: Agrega equipo
- `update_standings()`: Recalcula posiciones
- `get_sorted_standings()`: Obtiene tabla ordenada
- `apply_penalty()`: Aplica multa/bonificación

## Algoritmo de Fixture

El sistema utiliza el algoritmo **Round-Robin** para generar fixtures:

- **Equipos pares**: Cada equipo juega contra todos los demás
- **Equipos impares**: Se agrega un "BYE" temporal
- **Localía**: Se alterna automáticamente
- **Ida y vuelta**: Se generan automáticamente según el número de vueltas

## Criterios de Desempate

La tabla de posiciones se ordena por:
1. **Puntos totales** (descendente)
2. **Diferencia de puntos** (PF - PC, descendente)
3. **Puntos a favor** (descendente)
4. **Nombre** (alfabético)

## Extensibilidad

El sistema está diseñado para ser extensible:

- **Nuevas reglas**: Agregar métodos en las clases correspondientes
- **Nuevos tipos de partidos**: Extender la clase `Match`
- **Nuevos criterios de desempate**: Modificar `get_sorted_standings()` en `Standings`
- **Integración con base de datos**: Los métodos `to_dict()` facilitan la serialización
- **Interfaz gráfica**: La estructura modular permite fácil integración

## Ejemplo Completo

```python
from championship import Championship

# 1. Crear campeonato
champ = Championship("Campeonato 2024", rounds=2, points_per_win=2)

# 2. Agregar categorías
champ.add_category_with_teams(
    "TC",
    ["Leones", "Tigres", "Halcones", "Águilas"]
)

# 3. El fixture se genera automáticamente
category = champ.get_category("TC")
print(f"Total de partidos: {len(category.matches)}")

# 4. Registrar resultados
champ.register_match_result("TC", "Leones", "Tigres", 1, 95, 82)
champ.register_match_result("TC", "Halcones", "Águilas", 1, 88, 75)

# 5. Ver tabla de posiciones
standings = champ.get_standings("TC")
for pos, team in enumerate(standings, 1):
    print(f"{pos}. {team.name}: {team.points} pts")

# 6. Aplicar multa
champ.apply_penalty("TC", "Leones", 2)

# 7. Exportar
import json
with open("champ.json", "w") as f:
    json.dump(champ.to_dict(), f, indent=2, ensure_ascii=False)
```

## Despliegue

### GitHub

1. Inicializar el repositorio (si no está inicializado):
```bash
git init
git add .
git commit -m "Initial commit: Sistema de gestión de campeonatos"
```

2. Conectar con GitHub:
```bash
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### Vercel

Este proyecto incluye una API REST construida con Flask que puede desplegarse en Vercel.

#### Pasos para desplegar en Vercel:

1. **Instalar Vercel CLI** (si no lo tienes):
```bash
npm install -g vercel
```

2. **Iniciar sesión en Vercel**:
```bash
vercel login
```

3. **Desplegar el proyecto**:
```bash
vercel
```

4. **Para producción**:
```bash
vercel --prod
```

#### Alternativa: Desplegar desde GitHub

1. Sube tu código a GitHub
2. Ve a [vercel.com](https://vercel.com)
3. Conecta tu repositorio de GitHub
4. Vercel detectará automáticamente la configuración de Python
5. Haz clic en "Deploy"

### API Endpoints

Una vez desplegado, la API estará disponible en:
- `GET /` - Información de la API
- `POST /api/championships` - Crear campeonato
- `GET /api/championships` - Listar campeonatos
- `GET /api/championships/<id>` - Obtener campeonato
- `POST /api/championships/<id>/categories` - Agregar categoría
- `POST /api/championships/<id>/results` - Registrar resultado
- `GET /api/championships/<id>/standings/<category>` - Tabla de posiciones
- `GET /api/championships/<id>/fixture/<category>` - Fixture
- `POST /api/championships/<id>/penalty` - Aplicar multa

### Ejemplo de uso de la API

```bash
# Crear campeonato
curl -X POST https://tu-app.vercel.app/api/championships \
  -H "Content-Type: application/json" \
  -d '{
    "id": "champ1",
    "name": "Campeonato 2024",
    "rounds": 2,
    "points_per_win": 2
  }'

# Agregar categoría
curl -X POST https://tu-app.vercel.app/api/championships/champ1/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TC",
    "teams": ["Equipo A", "Equipo B", "Equipo C"]
  }'
```

## 🚀 Despliegue

### Desplegar en GitHub

1. **Usando el script automatizado (recomendado):**
   ```powershell
   .\deploy_completo.ps1
   ```

2. **Manual:**
   - Crea un repositorio en GitHub
   - Ejecuta:
   ```powershell
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/tu-usuario/tu-repo.git
   git branch -M main
   git push -u origin main
   ```

### Desplegar en Vercel

1. **Desde la interfaz web:**
   - Ve a https://vercel.com/new
   - Conecta tu repositorio de GitHub
   - Vercel detectará automáticamente la configuración

2. **Desde la CLI:**
   ```powershell
   npm install -g vercel
   vercel login
   vercel
   ```

Para más detalles, consulta [DEPLOY.md](DEPLOY.md)

## 📡 API REST

El proyecto incluye una API REST completa usando Flask. Una vez desplegado en Vercel, puedes acceder a:

- `GET /` - Información de la API
- `POST /api/championships` - Crear campeonato
- `GET /api/championships` - Listar campeonatos
- `GET /api/championships/<id>` - Obtener campeonato
- `POST /api/championships/<id>/categories` - Agregar categoría
- `POST /api/championships/<id>/results` - Registrar resultado
- `GET /api/championships/<id>/standings/<category>` - Tabla de posiciones
- `GET /api/championships/<id>/fixture/<category>` - Fixture
- `POST /api/championships/<id>/penalty` - Aplicar multa

## 📝 Archivos del Proyecto

- `championship.py` - Clase principal Championship
- `category.py` - Gestión de categorías
- `team.py` - Clase Team
- `match.py` - Clase Match
- `standings.py` - Tabla de posiciones
- `fixture_generator.py` - Generador de fixtures
- `main.py` - Ejemplos de uso
- `app.py` - API Flask
- `api/index.py` - Punto de entrada para Vercel
- `vercel.json` - Configuración de Vercel
- `requirements.txt` - Dependencias

## Licencia

Este proyecto es de código abierto y está disponible para uso libre.

## Autor

Sistema desarrollado para gestión de campeonatos de básquetbol.

