import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { NewsService } from 'src/app/services/news.service';
import { PaginatorComponent } from 'src/app/shared/paginator/paginator.component';
import { TownAndCampusNewsEntryDetailed } from 'src/models/town-and-campus-news';

@Component({
  selector: 'app-admin-news',
  standalone: true,
  imports: [CommonModule, FormsModule, PaginatorComponent, RouterModule],
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

  private readonly entriesPerPage: number = 10;

  private totalEntries: number | undefined = undefined;

  constructor(
    private readonly newsService: NewsService,
    private readonly router: Router,
    private readonly route: ActivatedRoute
  ) {
    newsService.getNewsCount().subscribe(count => (this.totalEntries = count));

    this.goToPage(0);
  }

  protected backToAdmin() {
    this.router.navigate(['..'], { relativeTo: this.route });
  }

  protected goToPage(newPage: number) {
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

  protected deleteNews(entryId: number): void {
    if (confirm('Are you sure you want to delete this news entry?')) {
      this.newsService.deleteNewsEntry(entryId).subscribe({
        next: (success: boolean) => {
          if (success) {
            console.log('Successfully deleted news entry');
          } else {
            console.log('Could not delete news entry');
          }
        },
      });
    }
  }
}
