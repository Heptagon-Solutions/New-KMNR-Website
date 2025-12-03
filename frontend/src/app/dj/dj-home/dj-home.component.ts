import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'dj-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dj-home.component.html',
  styleUrls: ['./dj-home.component.scss'],
})
export class DJHomeComponent {}
