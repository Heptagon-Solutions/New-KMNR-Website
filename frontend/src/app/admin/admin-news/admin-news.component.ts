import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
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
  protected newsEntries: TownAndCampusNewsEntryDetailed[] | undefined =
    undefined;
  protected page: number = 0;

  /** Returns undefined if we're still waiting on an API response. */
  protected get totalPages(): number | undefined {
    if (this.totalEntries) {
      return Math.ceil(this.totalEntries / this.entriesPerPage);
    } else {
      return undefined;
    }
  }

  private readonly entriesPerPage: number = 25;

  private totalEntries: number | undefined = undefined;

  public newNews: Partial<TownAndCampusNewsEntryDetailed> = {
    title: '',
    description: '',
  };

  constructor(private readonly newsService: NewsService) {
    newsService.getNewsCount().subscribe(count => (this.totalEntries = count));

    this.goToPage(0);
  }

  public goToPage(newPage: number) {
    if (newPage >= 0) {
      this.page = newPage;

      this.newsService
        .getNewsEntries(this.entriesPerPage, this.page)
        .subscribe(
          (entries: TownAndCampusNewsEntryDetailed[]) =>
            (this.newsEntries = entries)
        );
    }
  }

  editNews(entry: TownAndCampusNewsEntryDetailed) {
    // TODO: Implement edit functionality
    console.log('Edit news:', entry);
  }

  deleteNews(entryId: number): void {
    if (confirm('Are you sure you want to delete this news entry?')) {
      this.newsService
        .deleteNewsEntry(entryId.toString())
        .then(() => {
          if (this.newsEntries) {
            this.newsEntries = this.newsEntries.filter(
              entry => entry.id !== entryId
            );
          }
        })
        .catch(error => {
          console.error('Error deleting news:', error);
        });
    }
  }
}
