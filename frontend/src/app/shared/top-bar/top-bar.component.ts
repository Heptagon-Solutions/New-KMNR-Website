import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';

interface ButtonPosition {
  left: number;
  right: number;
  up: number;
  down: number;
}

interface ButtonConfig {
  buttons: Record<string, ButtonPosition>;
}

@Component({
  selector: 'app-top-bar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.scss']
})
export class TopBarComponent implements OnInit {
  buttonConfig: ButtonConfig | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadButtonConfig();
  }

  private loadButtonConfig() {
    this.http.get<ButtonConfig>('/assets/button-config.json').subscribe({
      next: (config) => {
        this.buttonConfig = config;
        this.applyButtonPositions();
      },
      error: (error) => {
        console.error('Error loading button config:', error);
      }
    });
  }

  private applyButtonPositions() {
    if (!this.buttonConfig) return;

    Object.entries(this.buttonConfig.buttons).forEach(([className, position]) => {
      const element = document.querySelector(`.${className}`) as HTMLElement;
      if (element) {
        const style = element.style;
        style.transform = `translate(${position.left - position.right}px, ${position.up - position.down}px)`;
      }
    });
  }
}
