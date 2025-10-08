from conan import ConanFile
from conan.tools.files import copy
from os.path import join
from conan.tools.cmake import CMake
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata

class BgfxConan(ConanFile):
    name            = "bgfx_tools"
    version         = "7816-14"
    description     = "Conan tool package for bgfx."
    url             = "https://github.com/bkaradzic/bgfx"
    license         = "BSD"
    settings        = "arch", "build_type", "os", "compiler"
    generators      = "CMakeToolchain", "CMakeDeps"

    def export(self):
        git = Git(self, self.recipe_folder)
        scm_url, scm_commit = git.get_url_and_commit()
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
            "BGFX_BUILD_EXAMPLES": False,
            "BGFX_BUILD_TOOLS": True,
            "BGFX_OPENGL_VERSION": 33
            }

        cmake.configure(options)
        cmake.build()

    def package(self):

        copy(self, "*.dll" , self.build_folder, join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*shaderc" , self.build_folder, join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*texturec" , self.build_folder, join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*shaderc.exe" , self.build_folder, join(self.package_folder, "bin"), keep_path=False)
        copy(self, "*texturec.exe" , self.build_folder, join(self.package_folder, "bin"), keep_path=False)


    def package_info(self):
        self.buildenv_info.prepend_path("PATH", join(self.package_folder, "bin"))
        self.runenv_info.prepend_path("PATH", join(self.package_folder, "bin"))
