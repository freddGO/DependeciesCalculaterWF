####
###Author: Alfredo Guillen. alfredo.guillen@nokia.com
####

import json
import shutil
from pprint import pprint
from os import listdir
from os.path import isfile, join


visited = set()
dependencies = set()
wfs = {}
wfs_from_git= {}

wfs_alt = {}
files_needed = []
NO_NAME = "NOT_FOUND"

CONFIG_HOME = "C:\\Motive\\SMP\\TEFCL\\config\\"
XDEV_HOME = CONFIG_HOME + "XDEV\\"
CONFIG_321 = XDEV_HOME + "Config_321"
GIT_HOME = "C:\\Motive\\SMP\\TEFCL\\GIT\\"
CL_SSC_HSI_WORKFLOWS = GIT_HOME + "CL_SSC" + "\\smp\\Configuration\\workflow\\"
COMMON_WORKFLOWS = GIT_HOME + "Common\\Configuration\\workflow\\"
CL_WORKFLOWS = GIT_HOME + "CL\\Configuration\\workflow\\"
CL_SSC_WORKFLOWS = GIT_HOME + "CL_SSC\\smp\\Configuration\\workflow\\"
EXPORTED_WORkFLOWS = CONFIG_HOME + "ConfigDownload"

EXT = ".mwf"


def get_dependency_from_file(file, _dir):
    global visited
    global EXT
    global wfs
    global wfs_alt
    global NO_NAME
    global files_needed

    if file in visited:
        return []
    elif NO_NAME is file:
        return []

    # print("[INFO] file=" + file)

    visited.add(file)

    try:
        data = json.load(open(_dir + file))
    except:
        data = json.load(open(alt_dir + file))
        print("[INFO] Need to copy " + file + " to " + _dir)
        files_needed.append(file)
    list = []
    # pprint(data);
    # print("data.repr_guid=" + data['repr_guid'])
    # print("data.repr_Type=" + data['repr_title'])
    workflow_contents = data['workflow_contents']
    child_shapes = workflow_contents['childShapes']
    for shape in child_shapes:
        if 'properties' in shape:
            if 'processid' in shape['properties']:
                processId = shape['properties']['processid']
                if processId in wfs:
                    wf_name = wfs[processId]
                elif processId in wfs_alt:
                    wf_name = wfs_alt[processId]
                    print("[WARNING] " + wf_name + " found in alt dir")
                else:
                    wf_name = NO_NAME
                    print("[WARNING] processId " + processId + " not found" )

                dependency = Dependency(shape['properties']['processid'],
                                        wf_name,
                                        file)
                list.append(dependency)
        else: print("[DEBUG]" + file + " has no dependencies")

    return list


class Dependency:
    def __init__(self, process_id, name, parent):
        self.processId = process_id
        self.name = name
        self.parent = parent

    def __str__(self):
        return "- " + self.name


def dfs(ssc_chile_wfs_dir, file, level):
    global dependencies
    for dependency in get_dependency_from_file(file, ssc_chile_wfs_dir):
        tab = ""
        for i in range(level):
            tab += "\t"
        print("%s %s" % (tab, dependency))
        dependencies.add(dependency.name)
        dfs(ssc_chile_wfs_dir, dependency.name, level + 1)


def get_wfs(dir):
    workflows = [x for x in listdir(dir) if x.endswith(EXT)]
    return workflows


def map_wf(dir, wfs):
    list_of_files = get_wfs(dir)
    for file in list_of_files:
        try:
            data = json.load(open(dir + file))
            wfs[data['repr_guid']] = file
        except ValueError:
            print(file)
            print(ValueError)


number_of_files = 0


def copy_file(origin_dir, destination_dir, file):
    global number_of_files
    try:
        origin_file = origin_dir + file
        shutil.copy(origin_file, destination_dir)
    except shutil.Error as e:
        print("[ERROR] %s" % e)
        number_of_files = number_of_files - 1
    except IOError as e:
        print("[ERROR] io %s " %e.strerror)
        print("[ERROR] destination_dir=" + destination_dir)
        number_of_files = number_of_files - 1


def move_wf_needed(origin, destination):
    global dependencies
    global number_of_files

    number_of_files = len(dependencies)

    print("[INFO] Trying to copy " + str(number_of_files) + " files")
    for dependency in dependencies:
        copy_file(origin, destination, dependency)
    print("[INFO] Has been copied [%d] files" % number_of_files)


# DIR = CONFIG_321 + "\\workflow\\"
DIR = EXPORTED_WORkFLOWS + "\\workflow\\"

workflows_hsi = get_wfs(CL_SSC_HSI_WORKFLOWS)
map_wf(DIR, wfs)
# map_wf(alt_dir, wfs_alt);

print("------------------------------------------------------------------------------------------------------------")
print("[INFO] Number of files found in " + DIR + " dir are: " + str(len(wfs)))
print("------------------------------------------------------------------------------------------------------------")
MAIN_WF_FILE = "CT_SSC_DTH" + EXT
print("------------------------------------------------------------------------------------------------------------")
print("-" + MAIN_WF_FILE)
dfs(DIR, MAIN_WF_FILE, 0)  # Gets the
print("------------------------------------------------------------------------------------------------------------")
print("Number of Workflows to be copied" + str(dependencies))
print("------------------------------------------------------------------------------------------------------------")

print("------------------------------------------------------------------------------------------------------------")
# move_wf_needed(ssc_chile_wfs_dir, ssc_chile_wfs_needed_destination_dir)
print("------------------------------------------------------------------------------------------------------------")

# for _file in files_needed:
    # copy_file(_file)
    # print(_file + " has been copied")

disjoint_workflows = set()
for workflow in dependencies:
    if workflow not in workflows_hsi:
        disjoint_workflows.add(workflow)
print("Workflows to be added to DTH branch - " + str(sorted(disjoint_workflows)))
print("------------------------------------------------------------------------------------------------------------")
for workflow in sorted(disjoint_workflows):
    print(workflow)

#### How to copy just SSC WFS?