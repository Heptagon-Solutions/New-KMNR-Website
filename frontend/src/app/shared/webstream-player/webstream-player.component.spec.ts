import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebstreamPlayerComponent } from './webstream-player.component';

describe('WebstreamPlayerComponent', () => {
  let component: WebstreamPlayerComponent;
  let fixture: ComponentFixture<WebstreamPlayerComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [WebstreamPlayerComponent]
    });
    fixture = TestBed.createComponent(WebstreamPlayerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
