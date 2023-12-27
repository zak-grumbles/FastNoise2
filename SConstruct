#!/usr/bin/env python

EnsureSConsVersion(3, 0, 0)
EnsurePythonVersion(3, 6)

import platform
import os

env = Environment()

conf = Configure(env)
void_p_size = conf.CheckTypeSize('void *', language='C++')
env['sizeof_void_p'] = void_p_size
print(f'Void* size is: {env['sizeof_void_p']}')
env = conf.Finish()

env.PrependENVPath("PATH", os.getenv("PATH"))

print(f"FastNoise2 Arch: {platform.machine()}")

# Command-line arguments
opts = Variables(args=ARGUMENTS)
opts.Add(BoolVariable("standalone_project", "Building FastNoise2 on its own", True))
opts.Add(BoolVariable("noise_tool", "Build the noise tool", False))
opts.Add(BoolVariable("build_tests", "Build FastNoise2 tests", False))
opts.Add(BoolVariable("build_shared_libs", "Build as a shared lib", False))
opts.Add(BoolVariable("fastsimd_compile_armv7", "Compile for armv7 arch", False))
opts.Add(BoolVariable("fastsimd_compile_aarch64", "Compile for aarch64 arch", False))
opts.Add(BoolVariable("fastsimd_compile_arm", "Compile for arm arch", False))
opts.Add(BoolVariable("fastsimd_compile_have_neon", "Compiler has neon", False))
opts.Update(env)

# Compilation options
machine = platform.machine().lower()

if machine == 'armv7':
    env.fastsimd_compile_armv7 = True
    env.fastsimd_compile_arm = True
    env.fastsimd_compile_have_neon = True
elif machine == 'aarch64':
    env.fastsimd_compile_aarch64 = True
    env.fastsimd_compile_arm = True
    env.fastsimd_compile_have_neon = True
elif machine == 'arm64':
    env.fastsimd_compile_arm = True
    env.fastsimd_compile_have_neon = True
elif machine == 'arm':
    env.fastsimd_compile_arm = True

if env["MSVC_VERSION"]:
    env.AppendUnique(CXXFLAGS=['/FS'])
    env['msvc'] = True

env.SConscript("src/SConscript", exports='env')