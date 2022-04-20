import os
from utils.python_utils import name_of, list_files, create_dir, TIMEOUT


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


def identify_output_label(_parent_dir, _file):
    subdir = _file[_file.rfind(_parent_dir) + len(_parent_dir):_file.rfind('/')]

    if subdir:
        if "exceptions" in subdir:
            label = "exception {" + subdir[subdir.rfind("/") + 1:] + "}"
        else:
            label = "timeout {" + str(TIMEOUT) + "}"
    else:
        label = "ok {" + str(TIMEOUT) + "}"

    return label


layers_set = set()
archs_set = set()
schedules_set = set()
outputs_set = set()


def save_output_item(_item, _name, _rows, _cols):
    file = open(_name + '.tsv', 'w')
    for col in _cols:
        file.write(" \t" + col)
    file.write("\t\n")
    for row in _rows:
        file.write(row + "\t")
        for col in _cols:
            value = _item[row][col]
            file.write(value + "\t")
        file.write('\n')
    file.close()


def save_output_set(_dir, _set, _outputs):
    create_dir(_dir)

    _layers_set = sorted(layers_set)
    _archs_set = sorted(archs_set)
    _schedules_set = sorted(schedules_set)

    for item in _set:
        item_name = _dir + str(item)
        save_output_item(_outputs[item], item_name, _archs_set, _schedules_set)


def save_dataflow(_dir, _outputs):
    create_dir(_dir)

    _layers_set = sorted(layers_set)
    _archs_set = sorted(archs_set)

    save_output_item(_outputs, _dir + 'summary', _layers_set, _archs_set)


def save_outputs(_optimizer_type, _outputs):
    output_dir = "./interstellar-output-analysis/"
    create_dir(output_dir)
    optimizer_dir = output_dir + _optimizer_type + "/"
    create_dir(optimizer_dir)

    if _optimizer_type != "dataflow":
        layers_dir = optimizer_dir + "layer/"
        save_output_set(layers_dir, layers_set, _outputs)
    else:
        save_dataflow(optimizer_dir, _outputs)

    file = open(optimizer_dir + 'labels.txt', 'w')
    for label in sorted(outputs_set):
        file.write(str(label) + '\n')
    file.close()


def analyze_interstellar_samples(_optimizer_type):
    optimizer_dir = "./interstellar-output/" + _optimizer_type + "/"
    layers = list_dirs(optimizer_dir)

    outputs = {}

    for layer in layers:
        outputs[layer] = {}
        layer_dir = optimizer_dir + layer + "/"
        if _optimizer_type == "dataflow":
            for output in list_outputs(layer_dir):
                outputs[layer][file_name(output)] = identify_output_label(layer, output)
                outputs_set.add(identify_output_label(layer, output))
                archs_set.add(file_name(output))
        else:
            archs = list_dirs(layer_dir)
            for arch in archs:
                outputs[layer][arch] = {}
                arch_dir = layer_dir + arch + "/"
                for output in list_outputs(arch_dir):
                    outputs[layer][arch][file_name(output)] = identify_output_label(arch, output)
                    outputs_set.add(identify_output_label(arch, output))
                    schedules_set.add(file_name(output))
                archs_set.add(arch)
        layers_set.add(layer)

    save_outputs(_optimizer_type, outputs)
