#!/usr/bin/env python3

import sys
import os
import subprocess

def get_status_output(*args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr

def exec(rc, op):
	rc, stdout, stderr = get_status_output(*args, **kwargs)
	if rc:
		print('== STDOUT ==')
		print(stdout)

		print('== STDERR ==')
		print(stderr)

		sys.exit(rc)

# Following environment variables will be passed in 
# compiler in (clang, gcc, emscripten)
# build_type (release, debug, asan, msan, tsan)

build_type_map = {
	'release': 'Release',
	'debug': 'Debug',
	'asan': 'Release',
	'msan': 'Release',
	'tsan': 'Release',
	'valgrind': 'Release',
	'valgrind_dbg': 'Debug'
}

release_flag_map = {
	'release': '-O3',
	'debug': '-ggdb3',
	'asan': '-O1 -g -fsanitize=address -fno-omit-frame-pointer',
	'msan': '-fsanitize=memory -fno-omit-frame-pointer -g -O2',
	'tsan': '-fsanitize=thread -g -O1',
	'valgrind': '',
	'valgrind_dbg': ''
}

compiler_definitions_map = {
	'clang': '',
	'gcc': '',
	'emscripten': '-DPSP_WASM_BUILD'
}

compiler_c_map = {
	'clang': 'clang',
	'gcc': 'gcc',
	'emscripten': 'emcc'
}

compiler_cpp_map = {
	'clang': 'clang++',
	'gcc': 'g++',
	'emscripten': 'em++'
}



def main():

	exec(['mkdir', 'build'])

	os.chdir('build')

	build_type = build_type_map[os.environ['BuildType']]
	flags = release_flag_map[os.environ['BuildType']]
	definitions = compiler_definitions_map[os.environ['Compiler']]
	cc = compiler_c_map[os.environ['Compiler']]
	cxx = compiler_cpp_map[os.environ['Compiler']]

	exec(['cmake', '-G', 'Ninja', '-DCMAKE_BUILD_TYPE', build_type, '-DCMAKE_CXX_FLAGS', flags,
	'-DCMAKE_C_COMPILER', cc, '-DCMAKE_CXX_COMPILER', cxx])

	exec(['ninja'])

	if os.environ['Compiler'] == 'emscripten':
		sys.exit(0)

	exec(['./install/psp_test'])
	sys.exit(0)


if __name__ == '__main__':
	main()
