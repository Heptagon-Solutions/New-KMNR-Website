import { TestBed } from '@angular/core/testing';

import { FooterPositionService } from './footer-position.service';

describe('FooterPositionService', () => {
  let service: FooterPositionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FooterPositionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
