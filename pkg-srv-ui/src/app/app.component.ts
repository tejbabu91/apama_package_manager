import { Component, OnInit } from '@angular/core';
import { PackageServerService } from './package-server.service';
import {PackageManifest} from './models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'pkg-srv-ui';
  packages: PackageManifest[];

  constructor(private pss: PackageServerService) {
  }

  ngOnInit(): void {
    this.pss.getPackages().toPromise().then((val: PackageManifest[]) => {
      this.packages = val;
    });
  }

}
