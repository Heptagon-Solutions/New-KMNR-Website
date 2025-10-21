import { Injectable } from '@angular/core';

import { ContactInfo, ExecutiveBoard } from 'src/models/models';

@Injectable({
  providedIn: 'root',
})
export class AboutService {
  constructor() {}

  public async getAdvisor(): Promise<string> {
    return 'Prof. Dummy data';
  }

  public async getContactInfo(): Promise<ContactInfo> {
    return {
      twitter: 'fake-twitter',
      email: 'dummy@data.com',
      phoneNumbers: {
        request: '123-456-7890',
        office: '123-456-7890',
        texter: '123-456-7890',
      },
      address: {
        line1: 'KMNR',
        line2: '100 Fake St.',
        cityStateZip: 'Rolla, MO 65401',
      },
    };
  }

  public async getEboard(): Promise<ExecutiveBoard> {
    return {
      stationManager: 'Mr. Dummy Data',
      programDirector: 'Mr. Dummy Data',
      chiefEngineer: 'Mr. Dummy Data',
      personnelDirector: 'Mr. Dummy Data',
      businessDirector: 'Mr. Dummy Data',
      publicRelations: 'Mr. Dummy Data',
      musicDirector: 'Mr. Dummy Data',
      roadshowDirectors: 'Mr. Dummy Data',
      newsDirector: 'Mr. Dummy Data',
      productions: 'Mr. Dummy Data',
      historian: 'Mr. Dummy Data',
    };
  }
}
