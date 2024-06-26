# bgfx.cmake - bgfx building in cmake
# Written in 2017 by Joshua Brookover <joshua.al.brookover@gmail.com>

# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.

# You should have received a copy of the CC0 Public Domain Dedication along with
# this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.


add_library(glslc-compiler SHARED IMPORTED)

set_target_properties(glslc-compiler PROPERTIES
    IMPORTED_LOCATION        ${BGFX_DIR}/3rdparty/glslc-compiler/Libraries/x64/NvnGlslc.dll
    IMPORTED_IMPLIB          ${BGFX_DIR}/3rdparty/glslc-compiler/Libraries/x64/NvnGlslc.lib
    INTERFACE_INCLUDE_DIRECTORIES  ${BGFX_DIR}/3rdparty/glslc-compiler/Include
)
