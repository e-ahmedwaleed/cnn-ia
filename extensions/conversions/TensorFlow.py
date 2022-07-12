# WARNING: FILE NAME SHOULD BE A VALID MODULE NAME (NO SPACES OR UNACCEPTABLE CHARACTERS)
import os

from gui import utils
from tf2onnx.version import version
from distutils.dir_util import copy_tree

# Saved models are expected to be files by default
MODEL_IS_DIR = True


# TensorFlow (model_path) -> converted to onnx and saved (onnx_path)
def to_onnx(model_path):
    # Dummy print to make sure the required library is available
    print("Conversion to onnx will be done using tf2onnx==" + str(version))

    model_path = model_path.replace('\\', '/')
    output_dir = os.path.basename(model_path).replace(' ', '')
    onnx_path = output_dir + ".onnx"

    # Copy model to project dir to avoid any problems with paths
    copy_tree(model_path, output_dir)

    utils.run_python('-m tf2onnx.convert --saved-model ' + output_dir + ' --output ' + onnx_path)

    # Deleted the copied model after conversion is done
    utils.delete_folder(output_dir)

    return onnx_path
