import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DJ } from 'src/models/dj';

import { OnAirComponent } from '../shared/on-air/on-air.component';
import { DJService } from '../shared/dj.service';

@Component({
  selector: 'dj-list',
  standalone: true,
  imports: [CommonModule, RouterModule, OnAirComponent],
  templateUrl: './dj-list.component.html',
  styleUrls: ['./dj-list.component.scss'],
})
export class DJListComponent {
  public readonly djsPerPage = 9;

  public djList: DJ[] | undefined = undefined;
  public listStart = 0;

  constructor(private readonly djService: DJService) {
    djService.getAllDJs().then((djs: DJ[]) => (this.djList = djs));
  }
}
