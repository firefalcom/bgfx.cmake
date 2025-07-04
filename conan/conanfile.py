from conan import ConanFile
from conan.tools.files import copy
from os.path import join
from conan.tools.cmake import CMake
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata

class BgfxConan(ConanFile):
    name            = "bgfx"
    version         = "7816-38"
    description     = "Conan package for bgfx."
    url             = "https://github.com/bkaradzic/bgfx"
    license         = "BSD"
    settings        = "arch", "build_type", "compiler", "os"
    generators      = "CMakeToolchain", "CMakeDeps"
    options         = {
            "shared": [True, False],
            "multithreaded": [True, False],
            "maximum_vertex_stream": ["ANY"],
            "maximum_shader_count" : ["ANY"],
            "sort_key_num_bits_program" : ["ANY"],
            "renderer_allocator" : ["buddy", "offset"]
            }
    default_options = {
            "shared": False,
            "multithreaded": True,
            "maximum_vertex_stream" : 0,
            "maximum_shader_count" : 0,
            "sort_key_num_bits_program" : 0,
            "renderer_allocator": "buddy"
            }

    def export(self):
        git = Git(self, self.recipe_folder)
        scm_url, scm_commit = git.get_url_and_commit('origin', True)
        update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

    def source(self):

        sources = self.conan_data["sources"]

        git = Git(self)
        git.clone(url=sources["url"], target=".")
        git.checkout(commit=sources["commit"])
        self.run("git submodule update --init")

    def build(self):
        cmake = CMake(self)
        options = {
            "BUILD_SHARED_LIBS": self.options.shared,
            "BGFX_CONFIG_MULTITHREADED": self.options.multithreaded,
            "BGFX_BUILD_EXAMPLES": False,
            "BGFX_BUILD_TOOLS": False,
            "BGFX_OPENGL_VERSION": 33
            }

        if self.options.maximum_vertex_stream != 0:
            options.update(BGFX_CONFIG_MAX_VERTEX_STREAMS = self.options.maximum_vertex_stream)

        if self.options.maximum_shader_count != 0:
            options.update(BGFX_CONFIG_MAX_SHADERS = self.options.maximum_shader_count)

        if self.options.sort_key_num_bits_program != 0:
            options.update(BGFX_CONFIG_SORT_KEY_NUM_BITS_PROGRAM = self.options.sort_key_num_bits_program)

        if self.options.renderer_allocator == "buddy":
            options.update(BGFX_CONFIG_USE_BUDDY = 1)

        if self.options.renderer_allocator == "offset":
            options.update(BGFX_CONFIG_USE_OFFSET_ALLOCATOR = 1)

        cmake.configure(options)
        cmake.build()

    def collect_headers(self, include_folder):

        copy(self, "*.h"  , join(self.source_folder, include_folder), join(self.package_folder, "include"))
        copy(self, "*.hpp", join(self.source_folder, include_folder), join(self.package_folder, "include"))
        copy(self, "*.inl", join(self.source_folder, include_folder), join(self.package_folder, "include"))

    def package(self):
        self.collect_headers("bgfx/include")
        self.collect_headers("bimg/include")
        self.collect_headers("bx/include")
        copy(self, "*.sh" , join(self.source_folder, "bgfx/src"), join(self.package_folder, "include"))

        copy(self, "*.a" , self.build_folder, join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.so" , self.build_folder, join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.lib" , self.build_folder, join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.dll" , self.build_folder, join(self.package_folder, "bin"), keep_path=False)
        copy(self, "shaderc" , self.build_folder, join(self.package_folder, "bin"))
        copy(self, "*.exe" , self.build_folder, join(self.package_folder, "bin"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["bgfx", "bimg", "bx"]
        self.cpp_info.libs.extend(["astc-codec", "astc", "edtaa3", "etc1", "etc2", "iqa", "squish", "pvrtc", "tinyexr"])
        if self.settings.os != "Switch" and self.settings.os != "Orbis" and self.settings.os != "Prospero":
            self.cpp_info.libs.extend(["nvtt"])
        if self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["Cocoa", "QuartzCore", "OpenGL"])
            self.cpp_info.exelinkflags.extend(["-weak_framework", "Metal"])
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["GL", "X11", "pthread", "dl"])
        if self.settings.os == "Windows" or self.settings.os == "WindowsStore":
            self.cpp_info.includedirs = ["include", "include/compat/msvc"]
