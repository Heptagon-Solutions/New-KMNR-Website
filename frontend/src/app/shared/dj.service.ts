import { Injectable } from '@angular/core';

import { DJ } from 'src/models';

const URL = 'http://localhost:8971/djs/';

const SAMPLE_DJS: DJ[] = [
  { 
    id: 1, 
    name: "Mining Mike", 
    genres: "Classic Rock, Alternative",
    image: "assets/img/dj1.png",
    bio: "S&T Engineering major who's been rocking the airwaves for 3 years. Known for his deep dives into classic rock history and discovering hidden gems from the 70s and 80s."
  },
  { 
    id: 2, 
    name: "Techno Tyler", 
    genres: "Electronic, Dubstep",
    image: "assets/img/dj2.png",
    bio: "Computer Science student with a passion for electronic beats. Produces his own tracks and hosts late-night dance parties that get the whole campus moving."
  },
  { 
    id: 3, 
    name: "Jazz Jessica", 
    genres: "Jazz, Blues, Soul",
    image: "assets/img/dj3.jpg",
    bio: "Music Performance major who brings sophistication to Sunday mornings. Her jazz knowledge is encyclopedic, and she's performed with the S&T Jazz Ensemble."
  },
  { 
    id: 4, 
    name: "Metal Miner", 
    genres: "Heavy Metal, Hard Rock",
    image: "assets/img/dj4.png",
    bio: "Mechanical Engineering student who believes every morning should start with heavy riffs. Plays in a local Rolla metal band called 'Molten Core'."
  },
  { 
    id: 5, 
    name: "Pop Princess", 
    genres: "Top 40, Pop, Hip-Hop",
    image: "assets/img/dj5.jpg",
    bio: "Marketing major who keeps KMNR current with the latest hits. Always first to discover new artists and has an uncanny ability to predict chart toppers."
  },
  { 
    id: 6, 
    name: "Country Chris", 
    genres: "Country, Folk, Bluegrass",
    image: "assets/img/dj1.png",
    bio: "Missouri native who grew up on country music. Agricultural Engineering student who brings authentic country vibes and stories from small-town Missouri."
  },
  { 
    id: 7, 
    name: "Indie Isaac", 
    genres: "Indie Rock, Alternative",
    image: "assets/img/dj2.png",
    bio: "Philosophy major with an ear for underground music. Constantly discovering new indie bands and has connections with the St. Louis music scene."
  },
  { 
    id: 8, 
    name: "Retro Rachel", 
    genres: "80s, 90s, Classic Hits",
    image: "assets/img/dj3.jpg",
    bio: "History major who believes the best music was made before she was born. Known for her 'Throwback Thursday' segments and extensive vinyl collection."
  },
  { 
    id: 9, 
    name: "Ambient Adam", 
    genres: "Ambient, Chill, Lo-fi",
    image: "assets/img/dj4.png",
    bio: "Psychology major who curates the perfect study soundtracks. His shows are popular during finals week for their calming, focus-inducing vibes."
  },
  { 
    id: 10, 
    name: "Punk Pete", 
    genres: "Punk, Ska, Hardcore",
    image: "assets/img/dj5.jpg",
    bio: "Chemistry major with explosive energy to match his music taste. Active in the campus punk scene and organizes underground shows in Rolla."
  },
  { 
    id: 11, 
    name: "Reggae Ryan", 
    genres: "Reggae, Dub, World Music",
    image: "assets/img/dj1.png",
    bio: "International Studies major who spent a semester in Jamaica. Brings global music perspectives and positive vibes to weekend programming."
  },
  { 
    id: 12, 
    name: "Classical Clara", 
    genres: "Classical, Opera, Chamber Music",
    image: "assets/img/dj2.png",
    bio: "Music Education major and concert pianist. Provides classical music education during her shows and has performed at Carnegie Hall."
  }
];

@Injectable({
  providedIn: 'root',
})
export class DJService {
  constructor() {}

  public async getAllDJs(): Promise<DJ[]> {
    console.log('🎧 DEBUG: Fetching DJs from URL:', URL);
    try {
      const data = await fetch(URL);
      console.log('📡 DEBUG: DJ Fetch response:', { status: data.status, ok: data.ok });
      if (data.ok) {
        const result = await data.json();
        console.log('✅ DEBUG: DJ API returned data:', { count: result.length, djs: result });
        return result;
      } else {
        console.log('❌ DEBUG: DJ API response not ok, using sample data');
      }
    } catch (error) {
      console.log('❌ DEBUG: DJ Fetch error, using sample data:', error);
    }
    console.log('📋 DEBUG: Returning sample DJ data, count:', SAMPLE_DJS.length);
    return SAMPLE_DJS;
  }

  public async getDJ(id: number): Promise<DJ> {
    try {
      const data = await fetch(URL + id);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample DJ data');
    }
    
    const dj = SAMPLE_DJS.find(d => d.id === id);
    if (!dj) throw new Error('DJ not found');
    return dj;
  }
}
