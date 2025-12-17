/**
 * Representa un partido entre dos equipos.
 */
export class Match {
  teamA: string;
  teamB: string;
  roundNumber: number;
  matchType: string; // 'ida' o 'vuelta'
  played: boolean = false;
  scoreA: number | null = null;
  scoreB: number | null = null;
  winner: string | null = null;

  constructor(teamA: string, teamB: string, roundNumber: number, matchType: string = "ida") {
    this.teamA = teamA;
    this.teamB = teamB;
    this.roundNumber = roundNumber;
    this.matchType = matchType;
  }

  /**
   * Registra el resultado del partido.
   */
  registerResult(scoreA: number, scoreB: number): void {
    this.scoreA = scoreA;
    this.scoreB = scoreB;
    this.played = true;

    if (scoreA > scoreB) {
      this.winner = this.teamA;
    } else if (scoreB > scoreA) {
      this.winner = this.teamB;
    } else {
      this.winner = "Empate";
    }
  }

  /**
   * Convierte el partido a un objeto JSON.
   */
  toDict(): Record<string, any> {
    return {
      team_a: this.teamA,
      team_b: this.teamB,
      round_number: this.roundNumber,
      match_type: this.matchType,
      played: this.played,
      score_a: this.scoreA,
      score_b: this.scoreB,
      winner: this.winner
    };
  }

  toString(): string {
    if (this.played && this.scoreA !== null && this.scoreB !== null) {
      return `Match(${this.teamA} ${this.scoreA} - ${this.scoreB} ${this.teamB})`;
    }
    return `Match(${this.teamA} vs ${this.teamB}, Round ${this.roundNumber}, ${this.matchType})`;
  }
}

