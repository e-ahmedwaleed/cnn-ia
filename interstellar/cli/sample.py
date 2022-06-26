import threading

from cli.utils import create_dir, list_files, name_of
from cli.test import run_python


def list_samples(_type):
    samples = []
    samples_dir = "./samples/" + _type + "/"
    for sample in list_files(samples_dir):
        if ".json" in sample:
            samples.append(samples_dir + sample)
    return samples


# noinspection SpellCheckingInspection
def run_dataflow_samples(_timeout):
    _optimizer_type = "dataflow_explore"

    layers = list_samples("layer")
    archs = list_samples("arch")

    output_dir = "interstellar-output"
    create_dir(output_dir)

    optimizer_dir = output_dir + "/"
    optimizer_dir += "dataflow"
    optimizer_dir += '-' + str(_timeout)
    create_dir(optimizer_dir)

    for layer in layers:
        layer_dir = optimizer_dir + "/" + name_of(layer)
        create_dir(layer_dir)
        threads = []
        for arch in archs:
            arch_dir = layer_dir + "/" + name_of(arch)

            cmd = "./run_optimizer.py -v dataflow_explore " + arch + " " + layer
            output = arch_dir + ".txt"

            t = threading.Thread(target=run_python, args=(cmd, output, False, _timeout,), daemon=True)
            threads.append(t)
            t.start()

        for arch_thread in threads:
            arch_thread.join()

    return
