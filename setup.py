from pathlib import Path 
import os
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.editable_wheel import editable_wheel


# Helper function to build gaussian.so
def build_gaussian_so():
    root = Path(__file__).parent.resolve()
    source = root / "src" / "xmcinter" / "gaussian.c"
    output = root / "src" / "xmcinter" / "gaussian.so"

    compiler = os.environ.get("CC", "cc")

    subprocess.check_call([
        compiler,
        "-shared",
        "-fPIC",
        "-O3",
        str(source),
        "-o",
        str(output),
    ])

class BuildPyWithGaussian(build_py):
    def run(self):
        build_gaussian_so()
        super().run()

class EditableWheelWithGaussian(editable_wheel):
    def run(self):
        build_gaussian_so()
        super().run()

setup(
    cmdclass={
        "build_py": BuildPyWithGaussian,
        "editable_wheel": EditableWheelWithGaussian,
    },
)