import os
from utils.python_utils import list_files


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


# noinspection SpellCheckingInspection
def analyze_interstellar_samples(_optimizer_type):
    optimizer_dir = "./interstellar-output/" + _optimizer_type + "/"
    layers = list_dirs(optimizer_dir)

    for layer in layers:
        layer_dir = optimizer_dir + layer + "/"
        if _optimizer_type == "dataflow":
            list_outputs(layer_dir)
        else:
            archs = list_dirs(layer_dir)
            for arch in archs:
                arch_dir = layer_dir + arch + "/"
                list_outputs(arch_dir)
        return
