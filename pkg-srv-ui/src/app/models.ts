
export interface Dependency {
    name: string;
    version: string;
}

export interface PackageManifest {
    name: string;
    description: string;
    version: string;
    tags: string[];
    dependencies: Dependency[];
    monitors: string[];
    events: string[];
    connectivityPlugins: string[];
}
