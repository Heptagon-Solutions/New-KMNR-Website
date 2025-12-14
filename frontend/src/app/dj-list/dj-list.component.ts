import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';

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
  public djsPerPage = 6;
  public djList: DJ[] | undefined = undefined;
  public listStart = 0;

  constructor(private readonly djService: DJService, private router: Router) {}

  async ngOnInit() {
    console.log('🎧 DEBUG: DJ List component initializing...');
    try {
      this.djList = await this.djService.getAllDJs();
      console.log('✅ DEBUG: DJs loaded:', { count: this.djList?.length, djs: this.djList });
    } catch (error) {
      console.error('❌ DEBUG: Error loading DJs:', error);
    }
  }

  nextPage() {
    if (this.djList && this.listStart + this.djsPerPage < this.djList.length) {
      this.listStart += this.djsPerPage;
    }
  }

  previousPage() {
    if (this.listStart >= this.djsPerPage) {
      this.listStart -= this.djsPerPage;
    }
  }

  get canGoNext(): boolean {
    return this.djList ? this.listStart + this.djsPerPage < this.djList.length : false;
  }

  get canGoPrevious(): boolean {
    return this.listStart > 0;
  }

  navigateToDJ(djId: number) {
    this.router.navigate(['/djs', djId]);
  }
}
