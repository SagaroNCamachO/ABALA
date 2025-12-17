# Sistema de Gestión de Campeonatos de Básquetbol

Sistema completo y robusto para administrar campeonatos de básquetbol con múltiples categorías, generación automática de fixtures y gestión de tablas de posiciones.

## 🚀 Características

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

## 🛠️ Tecnologías

- **TypeScript** - Lenguaje principal
- **Node.js** - Runtime
- **Express** - Framework web para API REST
- **Vercel** - Plataforma de deployment

## 📁 Estructura del Proyecto

```
.
├── src/
│   ├── models/
│   │   ├── Team.ts          # Clase Team (equipos)
│   │   ├── Match.ts          # Clase Match (partidos)
│   │   ├── Standings.ts      # Clase Standings (tabla de posiciones)
│   │   ├── Category.ts       # Clase Category (gestión de categorías)
│   │   └── Championship.ts   # Clase principal Championship
│   ├── utils/
│   │   └── FixtureGenerator.ts # Generador de fixtures
│   └── api.ts                # API REST con Express
├── api/
│   └── index.ts              # Punto de entrada para Vercel
├── package.json              # Dependencias y scripts
├── tsconfig.json            # Configuración de TypeScript
├── vercel.json              # Configuración de Vercel
└── README.md                # Este archivo
```

## 📦 Instalación

### Requisitos
- Node.js 18.0.0 o superior
- npm o yarn

### Pasos

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/ABALA.git
cd ABALA
```

2. **Instalar dependencias:**
```bash
npm install
```

3. **Compilar TypeScript:**
```bash
npm run build
```

## 🚀 Uso

### Desarrollo Local

1. **Ejecutar en modo desarrollo:**
```bash
npm run dev
```

El servidor estará disponible en `http://localhost:3000`

2. **Compilar y ejecutar:**
```bash
npm run build
npm start
```

### API REST

Una vez ejecutando, la API estará disponible en `http://localhost:3000`

#### Endpoints Disponibles

- `GET /` - Información de la API
- `GET /health` - Verificar estado de la API
- `POST /api/championships` - Crear un nuevo campeonato
- `GET /api/championships` - Listar todos los campeonatos
- `GET /api/championships/:id` - Obtener un campeonato
- `POST /api/championships/:id/categories` - Agregar categoría
- `POST /api/championships/:id/results` - Registrar resultado
- `GET /api/championships/:id/standings/:category` - Obtener tabla de posiciones
- `GET /api/championships/:id/fixture/:category` - Obtener fixture
- `POST /api/championships/:id/penalty` - Aplicar multa

### Ejemplos de Uso de la API

#### 1. Crear un Campeonato

```bash
curl -X POST http://localhost:3000/api/championships \
  -H "Content-Type: application/json" \
  -d '{
    "id": "champ1",
    "name": "Campeonato Local 2024",
    "rounds": 2,
    "points_per_win": 2,
    "points_per_loss": 0
  }'
```

#### 2. Agregar una Categoría

```bash
curl -X POST http://localhost:3000/api/championships/champ1/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TC",
    "teams": ["Los Leones", "Los Tigres", "Los Halcones", "Las Águilas"]
  }'
```

O con número de equipos (nombres automáticos):

```bash
curl -X POST http://localhost:3000/api/championships/champ1/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Senior",
    "num_teams": 4
  }'
```

#### 3. Registrar un Resultado

```bash
curl -X POST http://localhost:3000/api/championships/champ1/results \
  -H "Content-Type: application/json" \
  -d '{
    "category": "TC",
    "team_a": "Los Leones",
    "team_b": "Los Tigres",
    "round_number": 1,
    "score_a": 95,
    "score_b": 82
  }'
```

#### 4. Obtener Tabla de Posiciones

```bash
curl http://localhost:3000/api/championships/champ1/standings/TC
```

#### 5. Obtener Fixture

```bash
# Todos los partidos
curl http://localhost:3000/api/championships/champ1/fixture/TC

# Partidos de una vuelta específica
curl http://localhost:3000/api/championships/champ1/fixture/TC?round=1
```

#### 6. Aplicar Multa/Bonificación

```bash
curl -X POST http://localhost:3000/api/championships/champ1/penalty \
  -H "Content-Type: application/json" \
  -d '{
    "category": "TC",
    "team": "Los Leones",
    "points": 2
  }'
```

## 🏗️ Clases Principales

### Championship
Clase principal que gestiona el campeonato completo.

**Métodos principales:**
- `addCategory()`: Agrega categoría con número de equipos
- `addCategoryWithTeams()`: Agrega categoría con nombres de equipos
- `registerMatchResult()`: Registra resultado de partido
- `getStandings()`: Obtiene tabla de posiciones
- `applyPenalty()`: Aplica multa/bonificación
- `toDict()`: Exporta a objeto JSON

### Category
Gestiona una categoría con sus equipos, partidos y tabla.

**Métodos principales:**
- `addTeams()`: Agrega equipos
- `generateFixture()`: Genera fixture automáticamente
- `registerMatchResult()`: Registra resultado
- `getStandings()`: Obtiene tabla de posiciones
- `getMatchesByRound()`: Filtra partidos por vuelta
- `getMatchesByTeam()`: Filtra partidos por equipo

### Team
Representa un equipo con sus estadísticas.

**Propiedades:**
- `pj`: Partidos jugados
- `pg`: Partidos ganados
- `pp`: Partidos perdidos
- `pf`: Puntos a favor
- `pc`: Puntos en contra
- `points`: Puntos totales
- `penaltyPoints`: Puntos de multa

### Match
Representa un partido entre dos equipos.

**Propiedades:**
- `teamA`, `teamB`: Equipos participantes
- `roundNumber`: Número de vuelta
- `matchType`: 'ida' o 'vuelta'
- `played`: Si el partido ya se jugó
- `scoreA`, `scoreB`: Resultados
- `winner`: Equipo ganador

### Standings
Gestiona la tabla de posiciones de una categoría.

**Métodos principales:**
- `addTeam()`: Agrega equipo
- `updateStandings()`: Recalcula posiciones
- `getSortedStandings()`: Obtiene tabla ordenada
- `applyPenalty()`: Aplica multa/bonificación

## 🔄 Algoritmo de Fixture

El sistema utiliza el algoritmo **Round-Robin** para generar fixtures:

- **Equipos pares**: Cada equipo juega contra todos los demás
- **Equipos impares**: Se agrega un "BYE" temporal
- **Localía**: Se alterna automáticamente
- **Ida y vuelta**: Se generan automáticamente según el número de vueltas

## 📊 Criterios de Desempate

La tabla de posiciones se ordena por:
1. **Puntos totales** (descendente)
2. **Diferencia de puntos** (PF - PC, descendente)
3. **Puntos a favor** (descendente)
4. **Nombre** (alfabético)

## 🚀 Despliegue

### Vercel (Recomendado)

1. **Instalar Vercel CLI:**
```bash
npm install -g vercel
```

2. **Iniciar sesión:**
```bash
vercel login
```

3. **Desplegar:**
```bash
vercel
```

4. **Para producción:**
```bash
vercel --prod
```

### Alternativa: Desde GitHub

1. Sube tu código a GitHub
2. Ve a [vercel.com](https://vercel.com)
3. Conecta tu repositorio
4. Vercel detectará automáticamente la configuración
5. Haz clic en "Deploy"

El archivo `vercel.json` ya está configurado para deployment automático.

## 📝 Scripts Disponibles

- `npm run dev` - Ejecutar en modo desarrollo con hot-reload
- `npm run build` - Compilar TypeScript a JavaScript
- `npm start` - Ejecutar la aplicación compilada
- `npm run type-check` - Verificar tipos sin compilar

## 🔧 Extensibilidad

El sistema está diseñado para ser extensible:

- **Nuevas reglas**: Agregar métodos en las clases correspondientes
- **Nuevos tipos de partidos**: Extender la clase `Match`
- **Nuevos criterios de desempate**: Modificar `getSortedStandings()` en `Standings`
- **Integración con base de datos**: Los métodos `toDict()` facilitan la serialización
- **Interfaz gráfica**: La estructura modular permite fácil integración

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso libre.

## 👤 Autor

Sistema desarrollado para gestión de campeonatos de básquetbol.
