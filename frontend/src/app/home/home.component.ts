import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BannerComponent } from '../shared/banner/banner.component';

@Component({
  selector: 'home',
  standalone: true,
  imports: [CommonModule, BannerComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {}
