import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import { PackageManifest } from './models';

@Injectable({
  providedIn: 'root'
})
export class PackageServerService {

  packagesUrl = '/packages';

  constructor(private http: HttpClient) { }

  getPackages(): Observable<PackageManifest[]> {
    return this.http.get<{'packages': PackageManifest[]}>(this.packagesUrl).pipe(
      map(x => x.packages)
    );
  }
}
