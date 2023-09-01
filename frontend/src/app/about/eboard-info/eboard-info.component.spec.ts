import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EBoardInfoComponent } from './eboard-info.component';

describe('EboardInfoComponent', () => {
  let component: EBoardInfoComponent;
  let fixture: ComponentFixture<EBoardInfoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [EBoardInfoComponent],
    });
    fixture = TestBed.createComponent(EBoardInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
