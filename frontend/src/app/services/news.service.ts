import { Injectable } from '@angular/core';

import { API_URL } from 'src/constants';
import {
  TownAndCampusNewsEntry,
  TownAndCampusNewsEntryDetailed,
} from 'src/models';

const URL = 'http://localhost:3000/townAndCampusNews/';

const SAMPLE_NEWS_BASIC: TownAndCampusNewsEntry[] = [
  {
    title: "S&T Engineering Career Fair",
    location: "Havener Center",
    contact_email: "career@mst.edu",
    description: "Annual career fair featuring 200+ companies recruiting S&T students for internships and full-time positions."
  },
  {
    title: "Rolla Downtown Holiday Festival",
    location: "Downtown Rolla",
    contact_email: "events@rollacity.org",
    description: "Holiday lights, local vendors, and live music featuring KMNR DJs spinning holiday classics."
  },
  {
    title: "Miner Football vs GVSU",
    location: "Allgood-Bailey Stadium",
    contact_email: "athletics@mst.edu",
    description: "Miners take on Grand Valley State in crucial conference matchup. Tailgate starts at 4 PM."
  },
  {
    title: "Solar Car Team Open House",
    location: "Kummer Student Design Center",
    contact_email: "solarcar@mst.edu",
    description: "See the latest solar car design and learn about renewable energy research at Missouri S&T."
  }
];

const SAMPLE_NEWS_DETAILED: TownAndCampusNewsEntryDetailed[] = [
  {
    id: 1,
    title: "S&T Engineering Career Fair",
    organization: "Missouri S&T Career Opportunities Center",
    description: "The largest career fair in the region featuring companies like Boeing, Caterpillar, ExxonMobil, and more. Students from all majors welcome.",
    location: "Havener Center",
    website: "https://career.mst.edu/careerfair",
    contact_name: "Sarah Johnson",
    contact_email: "career@mst.edu",
    approved: true,
    submit_date: "2024-11-15",
    expiration_date: "2025-02-15"
  },
  {
    id: 2,
    title: "Rolla Downtown Holiday Festival",
    organization: "City of Rolla",
    description: "Annual holiday celebration featuring local businesses, food trucks, and live entertainment. KMNR will be broadcasting live from the event.",
    location: "Downtown Rolla Pine Street",
    website: "https://rollacity.org/events",
    contact_name: "Mike Stevens",
    contact_email: "events@rollacity.org",
    approved: true,
    submit_date: "2024-11-20",
    expiration_date: "2024-12-20"
  },
  {
    id: 3,
    title: "Miner Football vs GVSU",
    organization: "Missouri S&T Athletics",
    description: "Critical GLVC conference game. Listen to live coverage on KMNR 89.7 FM with play-by-play coverage starting at 6:30 PM.",
    location: "Allgood-Bailey Stadium",
    website: "https://minerathletics.com",
    contact_name: "Athletics Department",
    contact_email: "athletics@mst.edu",
    approved: true,
    submit_date: "2024-11-01",
    expiration_date: "2024-12-15"
  },
  {
    id: 4,
    title: "Study Abroad Information Session",
    organization: "International Affairs Office",
    description: "Learn about study abroad opportunities in over 30 countries. Scholarships and financial aid information available.",
    location: "Norwood Hall 204",
    website: "https://international.mst.edu",
    contact_name: "Dr. Emily Chen",
    contact_email: "studyabroad@mst.edu",
    approved: true,
    submit_date: "2024-12-01",
    expiration_date: "2025-01-15"
  },
  {
    id: 5,
    title: "Formula SAE Team Fundraiser",
    organization: "Missouri S&T Formula SAE",
    description: "Help fund our team's trip to competition at Michigan International Speedway. BBQ dinner and car display.",
    location: "Student Design Center Parking Lot",
    website: "https://fsae.mst.edu",
    contact_name: "Alex Rodriguez",
    contact_email: "fsae@mst.edu",
    approved: false,
    submit_date: "2024-12-10",
    expiration_date: "2025-01-30"
  }
];

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  constructor() {}

  public async getNewsEntries(): Promise<TownAndCampusNewsEntry[]> {
    try {
      const data = await fetch(URL);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample news data');
    }
    return SAMPLE_NEWS_BASIC;
  }

  public async getAllNewsEntries(): Promise<TownAndCampusNewsEntryDetailed[]> {
    try {
      const data = await fetch(API_URL + 'admin/news');
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample detailed news data');
    }
    return SAMPLE_NEWS_DETAILED;
  }
}
