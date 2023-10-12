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
export class HomeComponent {
  public msg: string = 'nothing recieved from backend';

  constructor() {
    this.getMsg().then(msg => (this.msg = msg));
  }

  // This is an example of how to communicate to the Flask API
  private async getMsg(): Promise<string> {
    const response = await fetch('http://localhost:5000/data');
    return (await response.json()).msg;
  }
}
