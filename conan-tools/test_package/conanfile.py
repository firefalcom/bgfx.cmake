import os
from conan import ConanFile
from conan.tools.files import copy
from os.path import join
from conan.tools.build import can_run

class BgfxTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "VirtualBuildEnv"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def test(self):
        if can_run(self):
            shaderc = "shaderc"
            if self.settings.os == "Windows":
                shaderc = shaderc + ".exe"

            cmd = shaderc + " -i . -f test.fs -o test.out --type fragment"
            self.run("cd", env="conanrun")
            self.run("echo %PATH%", env="conanrun")
            self.run( cmd, env="conanrun")
