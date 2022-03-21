import os
from utils.python_utils import name_of, list_files


def file_name(_path):
    name = name_of(_path)
    return name[0:name.rfind(".")]


def list_dirs(_dir):
    (_, dirs, _) = next(os.walk(_dir))
    return dirs


# noinspection SpellCheckingInspection
def list_outputs(_arch):
    o_files = []

    o_dirs = list_dirs(_arch)
    for o_dir in o_dirs:
        dir_path = _arch + o_dir + "/"
        o_subdirs = list_dirs(dir_path)
        for o_subdir in o_subdirs:
            subdir_path = dir_path + o_subdir + "/"
            subdir_o_files = list_files(subdir_path)
            for subdir_o_file in subdir_o_files:
                o_files.append(subdir_path + subdir_o_file)

    for o_file in list_files(_arch):
        o_files.append(_arch + o_file)

    return o_files


def identify_subdir(_parent_dir, _file):
    return _file[_file.rfind(_parent_dir) + len(_parent_dir):_file.rfind('/')]


layers_set = set()
archs_set = set()
schedules_set = set()
outputs_set = set()


def save_outputs(_optimizer_type, _outputs):
    print(len(layers_set))
    print(len(archs_set))
    print(len(schedules_set))
    print(len(outputs_set))


def analyze_interstellar_samples(_optimizer_type):
    optimizer_dir = "./interstellar-output/" + _optimizer_type + "/"
    layers = list_dirs(optimizer_dir)

    outputs = {}

    for layer in layers:
        outputs[layer] = {}
        layer_dir = optimizer_dir + layer + "/"
        if _optimizer_type == "dataflow":
            for output in list_outputs(layer_dir):
                outputs[layer][file_name(output)] = identify_subdir(layer, output)
                outputs_set.add(identify_subdir(layer, output))
                archs_set.add(file_name(output))
        else:
            archs = list_dirs(layer_dir)
            for arch in archs:
                outputs[layer][arch] = {}
                arch_dir = layer_dir + arch + "/"
                for output in list_outputs(arch_dir):
                    outputs[layer][arch][file_name(output)] = identify_subdir(arch, output)
                    outputs_set.add(identify_subdir(arch, output))
                    schedules_set.add(file_name(output))
                archs_set.add(arch)
        layers_set.add(layer)

    save_outputs(_optimizer_type, outputs)
