import { Injectable } from '@angular/core';

import { BlogPost } from 'src/models';

const URL = 'http://localhost:3000/blog/';

const SAMPLE_BLOG_POSTS: BlogPost[] = [
  {
    id: 1,
    title: "KMNR's Best Albums of 2024",
    content: "As 2024 comes to a close, our DJs reflect on the year's most impactful albums. From Techno Tyler's electronic picks to Jazz Jessica's smooth selections, here's what kept our airwaves fresh this year. The standout album has to be Radiohead's surprise release 'Digital Ghosts' which perfectly captured the anxieties and hopes of our generation...",
    author: "KMNR Staff",
    publish_date: "2024-12-10",
    tags: ["music", "albums", "year-end", "reviews"],
    featured: true
  },
  {
    id: 2,
    title: "Interview: Local Rolla Band 'The Miners' on Their New EP",
    content: "We sat down with Rolla's hottest rock band 'The Miners' to discuss their latest EP 'Underground Sessions'. Formed by S&T students, they've been making waves in the local music scene. 'We wanted to capture the energy of college life while staying true to our mining heritage,' says lead singer Jake Peterson...",
    author: "Metal Miner",
    publish_date: "2024-12-05",
    tags: ["interview", "local-music", "rock", "rolla"],
    featured: true
  },
  {
    id: 3,
    title: "Throwback Thursday: The History of KMNR",
    content: "Did you know KMNR first went on the air in 1973? This week we're diving into the station's rich history, from its humble beginnings in the basement of the student union to becoming Missouri S&T's premier voice. We've uncovered some incredible archived recordings and photos that show just how far we've come...",
    author: "Retro Rachel",
    publish_date: "2024-11-28",
    tags: ["history", "throwback", "station", "archive"],
    featured: false
  },
  {
    id: 4,
    title: "Concert Review: Indie Night at The Forum",
    content: "Last weekend's indie showcase at The Forum was absolutely electric. Five local bands performed, including S&T student favorites 'Circuit Breaker' and 'Algorithm'. The energy was infectious and the sound quality was phenomenal. If you missed it, don't worry - we recorded the entire event and will be featuring highlights throughout the week...",
    author: "Indie Isaac",
    publish_date: "2024-11-25",
    tags: ["concert", "review", "indie", "local-venues"],
    featured: false
  },
  {
    id: 5,
    title: "New Music Friday: Electronic Underground",
    content: "This week's electronic picks are absolutely fire. From underground techno to mainstream EDM, here's what's been spinning in my booth. The standout track has to be 'Digital Dreams' by newcomer Synthwave Sally - it's got that perfect blend of retro and futuristic that gets me every time...",
    author: "Techno Tyler",
    publish_date: "2024-11-22",
    tags: ["new-music", "electronic", "edm", "recommendations"],
    featured: false
  },
  {
    id: 6,
    title: "Studying with Jazz: The Perfect Finals Playlist",
    content: "Finals season is upon us, and nothing helps concentration quite like smooth jazz. I've curated the perfect study playlist featuring Miles Davis, John Coltrane, and some contemporary artists that'll keep you focused without being distracting. Research shows that instrumental jazz can actually improve cognitive function...",
    author: "Jazz Jessica",
    publish_date: "2024-11-20",
    tags: ["jazz", "study", "finals", "playlist"],
    featured: false
  },
  {
    id: 7,
    title: "Equipment Spotlight: Our New Mixing Board",
    content: "We're excited to announce our latest studio upgrade - a state-of-the-art digital mixing board that's going to take our sound quality to the next level. Thanks to donations from alumni and local supporters, KMNR continues to modernize while maintaining our authentic sound...",
    author: "KMNR Engineering Team",
    publish_date: "2024-11-15",
    tags: ["equipment", "studio", "upgrades", "technology"],
    featured: false
  }
];

@Injectable({
  providedIn: 'root',
})
export class BlogService {
  constructor() {}

  public async getAllPosts(): Promise<BlogPost[]> {
    try {
      const data = await fetch(URL);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample blog data');
    }
    return SAMPLE_BLOG_POSTS;
  }

  public async getFeaturedPosts(): Promise<BlogPost[]> {
    try {
      const data = await fetch(URL + 'featured');
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample blog data');
    }
    return SAMPLE_BLOG_POSTS.filter(post => post.featured);
  }

  public async getPost(id: number): Promise<BlogPost> {
    try {
      const data = await fetch(URL + id);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample blog data');
    }
    
    const post = SAMPLE_BLOG_POSTS.find(p => p.id === id);
    if (!post) throw new Error('Blog post not found');
    return post;
  }

  public async getPostsByTag(tag: string): Promise<BlogPost[]> {
    try {
      const data = await fetch(URL + `tag/${tag}`);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample blog data');
    }
    return SAMPLE_BLOG_POSTS.filter(post => post.tags.includes(tag));
  }
}