import { Injectable } from '@angular/core';

import { DJ } from 'src/models';

const URL = 'http://localhost:3000/djs/';

@Injectable({
  providedIn: 'root',
})
export class DJService {
  constructor() {}

  public async getAllDJs(): Promise<DJ[]> {
    const data = await fetch(URL);
    return await data.json();
  }

  public async getDJ(id: number): Promise<DJ> {
    const data = await fetch(URL + id);
    return await data.json();
  }
}
