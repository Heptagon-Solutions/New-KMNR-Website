import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

/** This service contains information on where the footer is positioned relative to the viewport (user's screen). It is used mainly by WebstreamPopupComponent to decide its placement. */
@Injectable({
  providedIn: 'root',
})
export class FooterPositionService {
  /** The y position of the top of the footer component, relative to the user's screen, if it is in the viewport. If it is not visible (outside of viewport), value will be 0. */
  public readonly topOfFooterPosition = new BehaviorSubject<number>(0);
}
