import { Category } from './Category';

/**
 * Gestiona un campeonato completo de básquetbol.
 */
export class Championship {
  name: string;
  rounds: number;
  pointsPerWin: number;
  pointsPerLoss: number;
  categories: Map<string, Category> = new Map();

  constructor(
    name: string = "Campeonato de Básquetbol",
    rounds: number = 1,
    pointsPerWin: number = 2,
    pointsPerLoss: number = 0
  ) {
    this.name = name;
    this.rounds = rounds;
    this.pointsPerWin = pointsPerWin;
    this.pointsPerLoss = pointsPerLoss;
  }

  /**
   * Agrega una categoría al campeonato.
   */
  addCategory(
    categoryName: string,
    numTeams: number,
    pointsPerWin?: number,
    pointsPerLoss?: number
  ): void {
    if (this.categories.has(categoryName)) {
      throw new Error(`La categoría '${categoryName}' ya existe`);
    }

    const pointsWin = pointsPerWin ?? this.pointsPerWin;
    const pointsLoss = pointsPerLoss ?? this.pointsPerLoss;

    const category = new Category(categoryName, this.rounds, pointsWin, pointsLoss);

    // Generar nombres de equipos automáticamente
    const teamNames = Array.from(
      { length: numTeams },
      (_, i) => `${categoryName} Equipo ${i + 1}`
    );
    category.addTeams(teamNames);

    // Generar fixture automáticamente
    category.generateFixture();

    this.categories.set(categoryName, category);
  }

  /**
   * Agrega una categoría con nombres de equipos específicos.
   */
  addCategoryWithTeams(
    categoryName: string,
    teamNames: string[],
    pointsPerWin?: number,
    pointsPerLoss?: number
  ): void {
    if (this.categories.has(categoryName)) {
      throw new Error(`La categoría '${categoryName}' ya existe`);
    }

    const pointsWin = pointsPerWin ?? this.pointsPerWin;
    const pointsLoss = pointsPerLoss ?? this.pointsPerLoss;

    const category = new Category(categoryName, this.rounds, pointsWin, pointsLoss);
    category.addTeams(teamNames);
    category.generateFixture();

    this.categories.set(categoryName, category);
  }

  /**
   * Obtiene una categoría por su nombre.
   */
  getCategory(categoryName: string): Category | undefined {
    return this.categories.get(categoryName);
  }

  /**
   * Registra el resultado de un partido.
   */
  registerMatchResult(
    categoryName: string,
    teamA: string,
    teamB: string,
    roundNumber: number,
    scoreA: number,
    scoreB: number,
    matchType?: string
  ): boolean {
    const category = this.getCategory(categoryName);
    if (category === undefined) {
      return false;
    }

    return category.registerMatchResult(teamA, teamB, roundNumber, scoreA, scoreB, matchType);
  }

  /**
   * Aplica una multa o bonificación de puntos a un equipo.
   */
  applyPenalty(categoryName: string, teamName: string, points: number): void {
    const category = this.getCategory(categoryName);
    if (category) {
      category.applyPenalty(teamName, points);
    }
  }

  /**
   * Obtiene la tabla de posiciones de una categoría.
   */
  getStandings(categoryName: string) {
    const category = this.getCategory(categoryName);
    if (category === undefined) {
      return null;
    }

    return category.getStandings();
  }

  /**
   * Convierte el campeonato completo a un objeto JSON.
   */
  toDict(): Record<string, any> {
    const categoriesDict: Record<string, any> = {};
    for (const [name, cat] of this.categories.entries()) {
      categoriesDict[name] = cat.toDict();
    }

    return {
      name: this.name,
      rounds: this.rounds,
      points_per_win: this.pointsPerWin,
      points_per_loss: this.pointsPerLoss,
      categories: categoriesDict
    };
  }

  toString(): string {
    return `Championship(name='${this.name}', rounds=${this.rounds}, categories=${this.categories.size})`;
  }
}

