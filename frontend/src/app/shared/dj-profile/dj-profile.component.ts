import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OnAirComponent } from '../on-air/on-air.component';
import { DJ } from 'src/models';
import { DJService } from '../dj.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'dj-profile',
  standalone: true,
  imports: [CommonModule, OnAirComponent],
  templateUrl: './dj-profile.component.html',
  styleUrls: ['./dj-profile.component.scss'],
})
export class DJProfileComponent {
  public dj: DJ | undefined = undefined;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly djService: DJService
  ) {
    // TO DO: Use `route` to get real DJ's id. 1 is placeholder here
    djService.getDJ(1).then((dj: DJ) => (this.dj = dj));
  }
}
