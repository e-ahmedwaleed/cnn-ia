import os
from cli.utils import create_dir, list_files, list_dirs, name_of


def file_name(_path):
    name = name_of(_path)
    return name[0:name.rfind(".")]


# noinspection SpellCheckingInspection
def list_outputs(_arch):
    o_files = []

    o_dirs = list_dirs(_arch)
    for o_dir in o_dirs:
        dir_path = _arch + o_dir + '/'
        o_subdirs = list_dirs(dir_path)
        for o_subdir in o_subdirs:
            subdir_path = dir_path + o_subdir + '/'
            subdir_o_files = list_files(subdir_path)
            for subdir_o_file in subdir_o_files:
                o_files.append(subdir_path + subdir_o_file)

    for o_file in list_files(_arch):
        o_files.append(_arch + o_file)

    return o_files


def identify_output_label(_parent_dir, _file, _timeout):
    subdir = _file[_file.rfind(_parent_dir) + len(_parent_dir):_file.rfind('/')]

    if subdir:
        if "exceptions" in subdir:
            label = "exception {" + subdir[subdir.rfind('/') + 1:] + "}"
        else:
            label = "timeout {" + str(_timeout) + "}"
    else:
        label = "ok {" + str(_timeout) + "}"

    return label


layers_set = set()
archs_set = set()
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


def save_dataflow(_dir, _outputs):
    create_dir(_dir)

    _layers_set = sorted(layers_set)
    _archs_set = sorted(archs_set)

    save_output_item(_outputs, _dir + 'summary', _layers_set, _archs_set)


def save_outputs(_optimizer_type, _outputs, _timeout):
    output_dir = "./interstellar-output-analysis/"
    create_dir(output_dir)
    optimizer_dir = output_dir + _optimizer_type + '-' + str(_timeout) + '/'
    create_dir(optimizer_dir)

    save_dataflow(optimizer_dir, _outputs)

    file = open(optimizer_dir + 'labels.txt', 'w')
    for label in sorted(outputs_set):
        file.write(str(label) + '\n')
    file.close()


def analyze_dataflow_samples(_timeout):
    _optimizer_type = "dataflow"

    optimizer_dir = "./interstellar-output/" + _optimizer_type + '-' + str(_timeout) + '/'
    layers = list_dirs(optimizer_dir)

    outputs = {}

    for layer in layers:
        outputs[layer] = {}
        layer_dir = optimizer_dir + layer + '/'
        for output in list_outputs(layer_dir):
            outputs[layer][file_name(output)] = identify_output_label(layer, output, _timeout)
            outputs_set.add(identify_output_label(layer, output, _timeout))
            archs_set.add(file_name(output))
        layers_set.add(layer)

    save_outputs(_optimizer_type, outputs, _timeout)
