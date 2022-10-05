from   conans       import ConanFile, CMake
from   distutils.dir_util import copy_tree
import os

class BgfxConan(ConanFile):
    name            = "bgfx-tools"
    version         = "7816-8"
    description     = "Conan package for bgfx."
    url             = "https://github.com/bkaradzic/bgfx"
    license         = "BSD"
    settings        = "arch", "build_type", "compiler", "os"
    generators      = "cmake"

    scm ={
        "type": "git",
        "url": "auto",
        "revision": "auto",
        "submodule": "shallow"
    }

    def build(self):
        cmake          = CMake(self)
        options = {
            "BGFX_BUILD_EXAMPLES": False,
            "BGFX_BUILD_TOOLS": True,
            "BGFX_OPENGL_VERSION": 33
            }

        cmake.configure(None, options)
        cmake.build()

    def collect_headers(self, include_folder):
        self.copy("*.h"  , dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)

    def package(self):
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("shaderc", dst="bin")
        self.copy("texturec", dst="bin")
        self.copy("*.exe", dst="bin", keep_path=False)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
