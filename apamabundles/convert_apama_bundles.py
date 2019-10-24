#!/usr/bin/env python3

import os, glob, shutil, subprocess, json
import xml.etree.ElementTree as ET

scriptDir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
cliPath = os.path.abspath(os.path.join(scriptDir, '..', 'cli', 'apm.py'))

def main():
    apHome = os.path.abspath(os.environ['APAMA_HOME'])
    apHomeLen = len(apHome) + 1
    stageDir = 'stage/'
    if os.path.exists(stageDir): shutil.rmtree(stageDir)
    os.makedirs(stageDir, exist_ok=True)
    for f in glob.glob(apHome + '/**/*.bnd', recursive=True):
        root = ET.parse(f).getroot()
        apamaPackageName = 'Apama ' + os.path.basename(f)[:-4]

        description = root.find('description')
        if description is not None:
            description = description.text.strip() if description.text is not None else None

        monFiles = list()
        for monitors in root.findall('monitors'):
            for c in monitors:
                if c.tag == 'fileset':
                    dir = c.attrib['dir'] if 'dir' in c.attrib else None
                    for cc in c:
                        if cc.tag == 'include':
                            name = cc.attrib['name'] if 'name' in cc.attrib else None
                            if name is None: continue
                            monName = ((dir + '/') if dir is not None else '') + name
                            if monName.startswith('${APAMA_HOME}'):
                                monName = os.path.abspath(monName.replace('${APAMA_HOME}', apHome))
                            else:
                                monName = os.path.abspath(os.path.join(os.path.dirname(f), monName))
                            if not os.path.exists(monName) and len(glob.glob(monName)) == 0:
                                print(monName)
                                raise Exception(f'Unable to resolve monitor with name {name} in fileset={dir} in {os.path.basename(f)}')
                            monFiles.extend(glob.glob(monName))
                        else:
                            raise Exception(f'Unknown tag {cc.tag}')
                elif c.tag == 'file':
                    name = c.attrib['name'] if 'name' in c.attrib else None
                    if name is None: continue
                    if name.startswith('${APAMA_HOME}'):
                        monName = os.path.abspath(name.replace('${APAMA_HOME}', apHome))
                    else:
                        monName = os.path.abspath(os.path.join(os.path.dirname(f), name))
                    if not os.path.exists(monName) and glob.glob(monName):
                        raise Exception(f'Unable to resolve monitor with name {name} in {os.path.basename(f)}')
                    monFiles.extend(glob.glob(monName))
                else:
                    raise Exception(f'Unknown tag {c.tag}')

        evtFiles = list()
        for evtFile in root.findall('events'):
            for c in evtFile:
                if c.tag == 'fileset':
                    dir = c.attrib['dir'] if 'dir' in c.attrib else None
                    for cc in c:
                        if cc.tag == 'include':
                            name = cc.attrib['name'] if 'name' in cc.attrib else None
                            if name is None: continue
                            evt = ((dir + '/') if dir is not None else '') + name
                            if evt.startswith('${APAMA_HOME}'):
                                evt = os.path.abspath(evt.replace('${APAMA_HOME}', apHome))
                            else:
                                evt = os.path.abspath(os.path.join(os.path.dirname(f), evt))
                            if not os.path.exists(evt) and len(glob.glob(evt)) == 0:
                                raise Exception(f'Unable to resolve event file with name {name} in fileset={dir} in {os.path.basename(f)}')
                            evtFiles.extend(glob.glob(evt))
                        else:
                            raise Exception(f'Unknown tag {cc.tag}')
                elif c.tag == 'file':
                    name = c.attrib['name'] if 'name' in c.attrib else None
                    if name is None: continue
                    if name.startswith('${APAMA_HOME}'):
                        evt = os.path.abspath(name.replace('${APAMA_HOME}', apHome))
                    else:
                        evt = os.path.abspath(os.path.join(os.path.dirname(f), name))
                    if not os.path.exists(evt) and len(glob.glob(evt)) == 0:
                        raise Exception(f'Unable to resolve monitor with name {name} in {os.path.basename(f)}')
                    evtFiles.extend(glob.glob(evt))
                else:
                    raise Exception(f'Unknown tag {c.tag}')

        dependencies = list()
        for c in root.findall('dependencies'):
            for cc in c:
                dependencyFileName = cc.attrib['bundle-filename'] if 'bundle-filename' in cc.attrib else None
                dependencies.append('Apama ' + os.path.basename(dependencyFileName)[:-4])

        if os.path.exists(stageDir + apamaPackageName): shutil.rmtree(stageDir + apamaPackageName)
        rootDir = os.getcwd()
        try:
            os.chdir(stageDir)
            subprocess.call([cliPath, 'init', apamaPackageName])

            with open(os.path.join(apamaPackageName, 'apama_packages.json')) as fp:
                manifestData = json.load(fp)
            manifestData['description'] = description
            manifestData['dependencies'] = [{'name': x, 'version': '1.0.0'} for x in dependencies]
            with open(os.path.join(apamaPackageName, 'apama_packages.json'), 'w') as fp:
                json.dump(manifestData, fp, indent=2)

            os.chdir(apamaPackageName)

            #copy monitors
            for file_to_copy in monFiles + evtFiles:
                relPath = file_to_copy[apHomeLen :]
                os.makedirs(os.path.dirname(relPath), exist_ok=True)
                shutil.copy(file_to_copy, relPath)

            subprocess.call([cliPath, 'publish'])

        finally:
            os.chdir(rootDir)

if __name__ == '__main__':
    main()