import { Injectable } from '@angular/core';

import { ContactInfo, ExecutiveBoard } from 'src/models';

const URL = 'http://localhost:3000/';

@Injectable({
  providedIn: 'root',
})
export class AboutService {
  constructor() {}

  async getAdvisor(): Promise<string> {
    const data = await fetch(URL + 'misc');
    return (await data.json())?.advisor;
  }

  async getContactInfo(): Promise<ContactInfo> {
    const data = await fetch(URL + 'contactInfo');
    return await data.json();
  }

  async getEboard(): Promise<ExecutiveBoard> {
    const data = await fetch(URL + 'executiveBoard');
    return await data.json();
  }
}
