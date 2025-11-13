import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DJ } from 'src/models';

import { OnAirComponent } from '../shared/on-air/on-air.component';
import { DJService } from '../shared/dj.service';

@Component({
  selector: 'dj-list',
  standalone: true,
  imports: [CommonModule, RouterModule, OnAirComponent],
  templateUrl: './dj-list.component.html',
  styleUrls: ['./dj-list.component.scss'],
})
export class DJListComponent implements OnInit {
  public readonly djsPerPage = 9;

  public djList: DJ[] | undefined = undefined;
  public currentPage = 0;

  constructor(private readonly djService: DJService) {}

  ngOnInit(): void {
    this.loadDJs();
  }

  loadDJs(): void {
    this.djService
      .getAllDJs()
      .then((djs: DJ[]) => (this.djList = djs))
      .catch(error => {
        console.error('Error loading DJs:', error);
      });
  }

  get currentPageDJs(): DJ[] {
    if (!this.djList) return [];
    const startIndex = this.currentPage * this.djsPerPage;
    return this.djList.slice(startIndex, startIndex + this.djsPerPage);
  }

  get totalPages(): number {
    if (!this.djList) return 0;
    return Math.ceil(this.djList.length / this.djsPerPage);
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages - 1) {
      this.currentPage++;
    }
  }

  previousPage(): void {
    if (this.currentPage > 0) {
      this.currentPage--;
    }
  }
}
