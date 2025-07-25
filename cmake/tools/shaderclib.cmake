# bgfx.cmake - bgfx building in cmake
# Written in 2017 by Joshua Brookover <joshua.al.brookover@gmail.com>

# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.

# You should have received a copy of the CC0 Public Domain Dedication along with
# this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

project(shaderclib)

include( CMakeParseArguments )

include( cmake/3rdparty/fcpp.cmake )
include( cmake/3rdparty/glsl-optimizer.cmake )
include( cmake/3rdparty/glslang.cmake )
include( cmake/3rdparty/spirv-cross.cmake )
include( cmake/3rdparty/spirv-tools.cmake )
include( cmake/3rdparty/webgpu.cmake )

add_library( shaderclib SHARED
	${BGFX_DIR}/tools/shaderc/shaderc.cpp
	${BGFX_DIR}/tools/shaderc/shaderc.h
	${BGFX_DIR}/tools/shaderc/shaderc_glsl.cpp
	${BGFX_DIR}/tools/shaderc/shaderc_hlsl.cpp
	${BGFX_DIR}/tools/shaderc/shaderc_hlsl_dxc.cpp
	${BGFX_DIR}/tools/shaderc/shaderc_pssl.cpp
	${BGFX_DIR}/tools/shaderc/shaderc_spirv.cpp
	${BGFX_DIR}/tools/shaderc/shaderc_metal.cpp
	${BGFX_DIR}/tools/shaderc/shaderc_pssl2.cpp
	${BGFX_DIR}/tools/shaderc/shaderc_nvn.cpp)

set_property(TARGET shaderclib PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET spirv-tools PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET spirv-cross PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET bx PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET fcpp PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET glsl-optimizer PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET glslang PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET webgpu PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET glcpp PROPERTY POSITION_INDEPENDENT_CODE ON)

target_include_directories( shaderclib PUBLIC ${BGFX_DIR}/tools/shaderc/)
target_compile_definitions( shaderclib PRIVATE "-D_CRT_SECURE_NO_WARNINGS" )
# set_target_properties( shaderclib PROPERTIES FOLDER "bgfx/tools" )
target_link_libraries( shaderclib PRIVATE bx bimg bgfx-vertexlayout bgfx-shader fcpp glsl-optimizer glslang spirv-cross spirv-tools webgpu )

if(WIN32)
	include( cmake/3rdparty/glslc-compiler.cmake )
	target_link_libraries(shaderclib PRIVATE glslc-compiler)
	add_custom_command(TARGET shaderc POST_BUILD
		COMMAND ${CMAKE_COMMAND} -E copy -t $<TARGET_FILE_DIR:shaderc> $<TARGET_RUNTIME_DLLS:shaderc>
		COMMAND_EXPAND_LISTS
		)
else()
	target_include_directories( shaderclib PRIVATE ${BGFX_DIR}/3rdparty/glslc-compiler/Include )
endif()

if( BGFX_CUSTOM_TARGETS )
	add_dependencies( tools shaderc )
endif()

if (ANDROID)
    target_link_libraries(shaderclib PRIVATE log)
elseif (IOS)
	set_target_properties(shaderclib PROPERTIES MACOSX_BUNDLE ON
											 MACOSX_BUNDLE_GUI_IDENTIFIER shaderc)
endif()



