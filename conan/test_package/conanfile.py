import os
from conan import ConanFile
from conan.tools.files import copy
from os.path import join
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run

class BgfxTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def layout(self):
        cmake_layout(self)

    def test(self):
        if can_run(self):
            if self.settings.os == "Windows":
                cmd = os.path.join(self.cpp.build.bindir, "bgfx_test.exe")
            else:
                cmd = os.path.join(self.cpp.build.bindir, "bgfx_test")

            self.run(cmd, env="conanrun")
