import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

const WEBSTREAM_SRC_URL = 'https://boombox.kmnr.org/webstream.mp3';

@Component({
  selector: 'webstream-player',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './webstream-player.component.html',
  styleUrls: ['./webstream-player.component.scss'],
})
export class WebstreamPlayerComponent implements OnInit {
  @Input() public invertColor: boolean = false;

  protected audioElement: HTMLAudioElement | null = null;
  protected audioSrc: string = WEBSTREAM_SRC_URL;

  protected isPlaying: boolean = false;

  public ngOnInit() {
    this.audioElement = document.getElementById(
      'audioElement'
    ) as HTMLAudioElement;
  }

  public play() {
    if (this.audioElement) {
      this.isPlaying = true;
      this.audioElement.play();
    }
  }

  public stop() {
    if (this.audioElement) {
      this.isPlaying = false;
      this.audioElement.pause();

      // Changing the src URL makes the browser flush its cached audio.
      // This means on load(), it pulls the current, live webstream
      // Then, upon play() it starts at the current live webstream instead of resuming where paused.
      this.audioElement.src = WEBSTREAM_SRC_URL + '?_=' + new Date().getTime();
      this.audioElement.load();
    }
  }
}
