import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DJ } from 'src/models/dj';

import { OnAirComponent } from '../shared/on-air/on-air.component';
import { DJService } from '../services/dj.service';

@Component({
  selector: 'dj-list',
  standalone: true,
  imports: [CommonModule, RouterModule, OnAirComponent],
  templateUrl: './dj-list.component.html',
  styleUrls: ['./dj-list.component.scss'],
})
export class DJListComponent {
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

  private readonly djsPerPage: number = 9;

  private totalDJs: number | undefined = undefined;

  constructor(private readonly djService: DJService) {
    djService.getDJCount().subscribe(djCount => (this.totalDJs = djCount));

    this.goToPage(0);
  }

  public goToPage(newPage: number) {
    if (newPage >= 0) {
      this.page = newPage;

      this.djService
        .getDJs(this.djsPerPage, this.page)
        .subscribe((djs: DJ[]) => (this.djList = djs));
    }
  }
}
