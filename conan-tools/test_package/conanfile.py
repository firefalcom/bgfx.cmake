import os

from conans import ConanFile, CMake, tools


class BgfxTestConan(ConanFile):
    settings = "os", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if self.settings.os == "Windows":
            self.run("shaderc.exe -i . -f test.fs -o test.out --type f", cwd="../../")
        else:
            self.run("shaderc -i . -f test.fs -o test.out --type f", cwd="../../")