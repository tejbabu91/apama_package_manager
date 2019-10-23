import { Pipe, PipeTransform } from '@angular/core';
import { PackageManifest } from './models';

@Pipe({
  name: 'filterpackages'
})
export class FilterpackagesPipe implements PipeTransform {

  transform(value: PackageManifest[], name: string): PackageManifest[] {
    const newpkglist: PackageManifest[] = [];
    value.forEach((x) => {
      if (x.name.indexOf(name) >= 0) {
        newpkglist.push(x);
      }
    });
    return newpkglist;
  }

}
