/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { AdminDJsComponent } from './admin-djs.component';

describe('AdminDjsComponent', () => {
  let component: AdminDJsComponent;
  let fixture: ComponentFixture<AdminDJsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AdminDJsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminDJsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
