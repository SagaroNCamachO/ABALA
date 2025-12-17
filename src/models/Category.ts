import { Team } from './Team';
import { Match } from './Match';
import { Standings } from './Standings';
import { FixtureGenerator } from '../utils/FixtureGenerator';

/**
 * Gestiona una categoría completa del campeonato.
 */
export class Category {
  name: string;
  rounds: number;
  teams: Map<string, Team> = new Map();
  matches: Match[] = [];
  standings: Standings;
  fixtureGenerated: boolean = false;

  constructor(name: string, rounds: number, pointsPerWin: number = 2, pointsPerLoss: number = 0) {
    this.name = name;
    this.rounds = rounds;
    this.standings = new Standings(name, pointsPerWin, pointsPerLoss);
  }

  /**
   * Agrega equipos a la categoría.
   */
  addTeams(teamNames: string[]): void {
    for (const name of teamNames) {
      if (!this.teams.has(name)) {
        const team = new Team(name, this.name);
        this.teams.set(name, team);
        this.standings.addTeam(team);
      }
    }
  }

  /**
   * Genera el fixture automáticamente basado en los equipos y vueltas.
   */
  generateFixture(): void {
    if (this.teams.size < 2) {
      throw new Error("Se necesitan al menos 2 equipos para generar el fixture");
    }

    const teamNames = Array.from(this.teams.keys());
    this.matches = FixtureGenerator.generateFixture(teamNames, this.rounds);
    this.fixtureGenerated = true;
  }

  /**
   * Registra el resultado de un partido.
   */
  registerMatchResult(
    teamA: string,
    teamB: string,
    roundNumber: number,
    scoreA: number,
    scoreB: number,
    matchType?: string
  ): boolean {
    // Buscar el partido (buscar en ambos sentidos: A vs B o B vs A)
    let match: Match | undefined = undefined;
    for (const m of this.matches) {
      // Verificar que los equipos coincidan (en cualquier orden)
      const teamsMatch =
        (m.teamA === teamA && m.teamB === teamB) ||
        (m.teamA === teamB && m.teamB === teamA);

      if (teamsMatch && m.roundNumber === roundNumber) {
        if (matchType === undefined || m.matchType === matchType) {
          match = m;
          break;
        }
      }
    }

    if (match === undefined) {
      return false;
    }

    // Ajustar el orden de los puntajes según el orden del partido
    let finalScoreA: number;
    let finalScoreB: number;
    if (match.teamA === teamA) {
      // El orden coincide
      finalScoreA = scoreA;
      finalScoreB = scoreB;
    } else {
      // El orden está invertido
      finalScoreA = scoreB;
      finalScoreB = scoreA;
    }

    // Registrar resultado en el partido
    match.registerResult(finalScoreA, finalScoreB);

    // Actualizar estadísticas de los equipos
    const teamAObj = this.teams.get(teamA);
    const teamBObj = this.teams.get(teamB);

    if (!teamAObj || !teamBObj) {
      return false;
    }

    teamAObj.addMatchResult(scoreA, scoreB, scoreA > scoreB);
    teamBObj.addMatchResult(scoreB, scoreA, scoreB > scoreA);

    // Recalcular tabla de posiciones
    this.standings.updateStandings();

    return true;
  }

  /**
   * Aplica una multa o bonificación de puntos a un equipo.
   */
  applyPenalty(teamName: string, points: number): void {
    this.standings.applyPenalty(teamName, points);
  }

  /**
   * Obtiene la tabla de posiciones ordenada.
   */
  getStandings(): Team[] {
    return this.standings.getSortedStandings();
  }

  /**
   * Obtiene los partidos de una vuelta específica.
   */
  getMatchesByRound(roundNumber: number): Match[] {
    return FixtureGenerator.getMatchesByRound(this.matches, roundNumber);
  }

  /**
   * Obtiene los partidos de un equipo específico.
   */
  getMatchesByTeam(teamName: string): Match[] {
    return FixtureGenerator.getMatchesByTeam(this.matches, teamName);
  }

  /**
   * Convierte la categoría a un objeto JSON.
   */
  toDict(): Record<string, any> {
    return {
      name: this.name,
      rounds: this.rounds,
      teams: Array.from(this.teams.values()).map(team => team.toDict()),
      matches: this.matches.map(match => match.toDict()),
      standings: this.standings.toDict()
    };
  }

  toString(): string {
    return `Category(name='${this.name}', teams=${this.teams.size}, rounds=${this.rounds})`;
  }
}

