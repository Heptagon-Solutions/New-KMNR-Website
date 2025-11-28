import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { NewsService } from 'src/app/services/news.service';
import { TownAndCampusNewsEntryDetailed } from 'src/models/town-and-campus-news';

@Component({
  selector: 'app-admin-news',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-news.component.html',
  styleUrls: ['./admin-news.component.scss'],
})
export class AdminNewsComponent {
  public newsEntries: TownAndCampusNewsEntryDetailed[] | undefined = undefined;
  public newNews: Partial<TownAndCampusNewsEntryDetailed> = {
    title: '',
    description: ''
  };

  constructor(private readonly newsService: NewsService) {
    newsService
      .getNewsEntries()
      .subscribe(
        (entries: TownAndCampusNewsEntryDetailed[]) =>
          (this.newsEntries = entries)
      )
  }

  addNews(): void {
    if (this.newNews.title && this.newNews.description) {
      this.newsService.createNewsEntry(this.newNews as TownAndCampusNewsEntryDetailed)
        .then((entry: TownAndCampusNewsEntryDetailed) => {
          if (this.newsEntries) {
            this.newsEntries.push(entry);
          } else {
            this.newsEntries = [entry];
          }
          this.newNews = { title: '', description: '' };
        })
        .catch(error => {
          console.error('Error creating news:', error);
        });
    }
  }

  editNews(entry: TownAndCampusNewsEntryDetailed): void {
    // TODO: Implement edit functionality
    console.log('Edit news:', entry);
  }

  deleteNews(entryId: number): void {
    if (confirm('Are you sure you want to delete this news entry?')) {
      this.newsService.deleteNewsEntry(entryId.toString())
        .then(() => {
          if (this.newsEntries) {
            this.newsEntries = this.newsEntries.filter(entry => entry.id !== entryId);
          }
        })
        .catch(error => {
          console.error('Error deleting news:', error);
        });
    }
  }
}
