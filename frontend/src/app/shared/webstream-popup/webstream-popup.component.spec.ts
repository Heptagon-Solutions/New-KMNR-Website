import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebstreamPopupComponent } from './webstream-popup.component';

describe('WebstreamPopupComponent', () => {
  let component: WebstreamPopupComponent;
  let fixture: ComponentFixture<WebstreamPopupComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [WebstreamPopupComponent]
    });
    fixture = TestBed.createComponent(WebstreamPopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
