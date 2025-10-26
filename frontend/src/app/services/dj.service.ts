import { Injectable } from '@angular/core';

import { DJ } from 'src/models/dj';

@Injectable({
  providedIn: 'root',
})
export class DJService {
  constructor() {}

  public async getAllDJs(): Promise<DJ[]> {
    return [
      {
        id: 1,
        name: 'Fake DJ 1',
        genres: 'noise',
      },
      {
        id: 2,
        name: 'Fake DJ 2',
        genres: 'math rock',
      },
    ];
  }

  public async getDJ(id: number): Promise<DJ> {
    return {
      id: id,
      name: 'Fake DJ 1',
      genres: 'noise',
    };
  }
}
