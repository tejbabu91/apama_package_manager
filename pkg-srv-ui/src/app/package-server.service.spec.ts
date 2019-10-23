import { TestBed } from '@angular/core/testing';

import { PackageServerService } from './package-server.service';

describe('PackageServerService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: PackageServerService = TestBed.get(PackageServerService);
    expect(service).toBeTruthy();
  });
});
