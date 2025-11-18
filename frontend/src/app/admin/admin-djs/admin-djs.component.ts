import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DJ } from 'src/models/dj';

import { DJService } from 'src/app/services/dj.service';

@Component({
  selector: 'app-admin-djs',
  templateUrl: './admin-djs.component.html',
  styleUrls: ['./admin-djs.component.scss'],
  standalone: true,
  imports: [CommonModule],
})
export class AdminDJsComponent {
  protected djList: DJ[] | undefined = undefined;
  protected page: number = 0;

  /** Returns undefined if we're still waiting on an API response. */
  protected get totalPages(): number | undefined {
    if (this.totalDJs) {
      return Math.ceil(this.totalDJs / this.djsPerPage);
    } else {
      return undefined;
    }
  }

  private readonly djsPerPage: number = 25;

  private totalDJs: number | undefined = undefined;

  constructor(private readonly djService: DJService) {
    djService.getDJCount().subscribe(userCount => (this.totalDJs = userCount));

    this.goToPage(0);
  }

  public goToPage(newPage: number) {
    if (newPage >= 0) {
      this.page = newPage;

      this.djService
        .getDJs(this.djsPerPage, this.page)
        .subscribe((users: DJ[]) => (this.djList = users));
    }
  }
}
