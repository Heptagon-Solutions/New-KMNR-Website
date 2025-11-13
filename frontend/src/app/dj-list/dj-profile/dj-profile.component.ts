import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { DJProfile } from 'src/models/dj';

import { OnAirComponent } from '../../shared/on-air/on-air.component';
import { DJService } from '../../services/dj.service';

@Component({
  selector: 'dj-profile',
  standalone: true,
  imports: [CommonModule, OnAirComponent],
  templateUrl: './dj-profile.component.html',
  styleUrls: ['./dj-profile.component.scss'],
})
export class DJProfileComponent {
  public dj: DJProfile | undefined = undefined;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly djService: DJService
  ) {
    // TO DO: Use `route` to get real DJ's id. 1 is placeholder here
    let djId = route.snapshot.paramMap.get('id');
    if (djId !== null) {
      djService
        .getDJProfile(Number(djId))
        .subscribe((dj: DJProfile) => (this.dj = dj));
    }
  }
}
