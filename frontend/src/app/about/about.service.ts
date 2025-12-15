import { Injectable } from '@angular/core';

import { ContactInfo, ExecutiveBoard } from 'src/models';

const URL = 'http://localhost:3000/';

@Injectable({
  providedIn: 'root',
})
export class AboutService {
  constructor() {}

  public async getAdvisor(): Promise<string> {
    const data = await fetch(URL + 'misc');
    return (await data.json())?.advisor;
  }

  public async getContactInfo(): Promise<ContactInfo> {
    const data = await fetch(URL + 'contactInfo');
    return await data.json();
  }

  public async getEboard(): Promise<ExecutiveBoard> {
    const data = await fetch(URL + 'executiveBoard');
    return await data.json();
  }
}
