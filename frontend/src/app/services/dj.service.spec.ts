import { TestBed } from '@angular/core/testing';

import { DJService } from './dj.service';

describe('DjService', () => {
  let service: DJService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DJService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
