import { Injectable } from '@angular/core';

import { ShowScheduleEntry } from 'src/models';

const URL = 'http://localhost:3000/schedule/';

const SAMPLE_SCHEDULE: ShowScheduleEntry[] = [
  // Sunday (0)
  { id: 1, show_name: "Sunday Morning Jazz", dj_id: 3, dj_name: "Jazz Jessica", day_of_week: 0, start_time: 8, end_time: 11, genre: "Jazz", description: "Start your Sunday with smooth jazz classics" },
  { id: 2, show_name: "Sunday Rock Revival", dj_id: 1, dj_name: "Mining Mike", day_of_week: 0, start_time: 14, end_time: 17, genre: "Classic Rock", description: "The best rock anthems from the 70s and 80s" },
  
  // Monday (1)
  { id: 3, show_name: "Monday Morning Metal", dj_id: 4, dj_name: "Metal Miner", day_of_week: 1, start_time: 7, end_time: 9, genre: "Heavy Metal", description: "Wake up with heavy riffs" },
  { id: 4, show_name: "The Indie Hour", dj_id: 7, dj_name: "Indie Isaac", day_of_week: 1, start_time: 16, end_time: 18, genre: "Indie Rock", description: "Discover new indie gems" },
  { id: 5, show_name: "Electronic Nights", dj_id: 2, dj_name: "Techno Tyler", day_of_week: 1, start_time: 20, end_time: 23, genre: "Electronic", description: "Dance the night away" },
  
  // Tuesday (2)
  { id: 6, show_name: "Top 40 Tuesday", dj_id: 5, dj_name: "Pop Princess", day_of_week: 2, start_time: 12, end_time: 15, genre: "Pop", description: "Today's biggest hits" },
  { id: 7, show_name: "Country Roads", dj_id: 6, dj_name: "Country Chris", day_of_week: 2, start_time: 17, end_time: 20, genre: "Country", description: "Country classics and new releases" },
  
  // Wednesday (3)
  { id: 8, show_name: "Wednesday Wind Down", dj_id: 9, dj_name: "Ambient Adam", day_of_week: 3, start_time: 19, end_time: 22, genre: "Ambient", description: "Chill vibes for midweek relaxation" },
  { id: 9, show_name: "Retro Wednesday", dj_id: 8, dj_name: "Retro Rachel", day_of_week: 3, start_time: 14, end_time: 17, genre: "80s/90s", description: "Throwback hits from the 80s and 90s" },
  
  // Thursday (4)
  { id: 10, show_name: "Punk Rock Thursday", dj_id: 10, dj_name: "Punk Pete", day_of_week: 4, start_time: 18, end_time: 21, genre: "Punk", description: "Raw energy and rebellion" },
  { id: 11, show_name: "Study Break Classics", dj_id: 12, dj_name: "Classical Clara", day_of_week: 4, start_time: 10, end_time: 12, genre: "Classical", description: "Focus music for studying" },
  
  // Friday (5)
  { id: 12, show_name: "Friday Night Party Mix", dj_id: 5, dj_name: "Pop Princess", day_of_week: 5, start_time: 21, end_time: 24, genre: "Dance/Pop", description: "Get the weekend started right" },
  { id: 13, show_name: "Alternative Friday", dj_id: 7, dj_name: "Indie Isaac", day_of_week: 5, start_time: 15, end_time: 18, genre: "Alternative", description: "Alternative rock for the weekend" },
  
  // Saturday (6)
  { id: 14, show_name: "Saturday Night Reggae", dj_id: 11, dj_name: "Reggae Ryan", day_of_week: 6, start_time: 19, end_time: 22, genre: "Reggae", description: "Island vibes and world music" },
  { id: 15, show_name: "Metal Saturday", dj_id: 4, dj_name: "Metal Miner", day_of_week: 6, start_time: 14, end_time: 17, genre: "Heavy Metal", description: "Saturday headbanging session" },
];

@Injectable({
  providedIn: 'root',
})
export class ScheduleService {
  constructor() {}

  public async getSchedule(): Promise<ShowScheduleEntry[]> {
    try {
      const data = await fetch(URL);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample schedule data');
    }
    return SAMPLE_SCHEDULE;
  }

  public async getScheduleForDay(dayOfWeek: number): Promise<ShowScheduleEntry[]> {
    try {
      const data = await fetch(URL + `day/${dayOfWeek}`);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample schedule data');
    }
    return SAMPLE_SCHEDULE.filter(entry => entry.day_of_week === dayOfWeek);
  }

  public async getShowsForDJ(djId: number): Promise<ShowScheduleEntry[]> {
    try {
      const data = await fetch(URL + `dj/${djId}`);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample schedule data');
    }
    return SAMPLE_SCHEDULE.filter(entry => entry.dj_id === djId);
  }

  public getTimeslots(): { [time: number]: ShowScheduleEntry[] } {
    const timeslots: { [time: number]: ShowScheduleEntry[] } = {};
    
    // Initialize all time slots
    for (let hour = 0; hour < 24; hour++) {
      timeslots[hour] = [];
    }
    
    // Group shows by start time
    SAMPLE_SCHEDULE.forEach(show => {
      for (let hour = show.start_time; hour < show.end_time; hour++) {
        if (!timeslots[hour]) timeslots[hour] = [];
        timeslots[hour].push(show);
      }
    });
    
    return timeslots;
  }
}