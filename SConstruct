#!/usr/bin/env python

EnsureSConsVersion(3, 0, 0)
EnsurePythonVersion(3, 6)

import platform
import os
print(f"FastNoise2 Arch: {platform.machine()}")

env = Environment()
env.PrependENVPath("PATH", os.getenv("PATH"))

opts = Variables(args=ARGUMENTS)

opts.Add(BoolVariable("standalone_project", "Building FastNoise2 on its own", True))
opts.Add(BoolVariable("noise_tool", "Build the noise tool", False))
opts.Add(BoolVariable("build_tests", "Build FastNoise2 tests", False))

opts.Update(env)

env.AppendUnique(CXXFLAGS=['/FS'])
env.AppendUnique(CPPPATH=['./include/FastNoise', './include/FastSIMD'])

# FastSIMD files
fastsimd_inl = Glob('FastSIMD/*.inl')
fastsimd_include_inl = Glob('../include/FastSIMD/*.inl')
fastsimd_internal_inl = Glob('FastSIMD/Internal/*.inl')

fastsimd_sources = [
    'FastSIMD/FastSIMD.cpp',
    'FastSIMD/FastSIMD_Level_AVX2.cpp',
    'FastSIMD/FastSIMD_Level_AVX512.cpp',
    'FastSIMD/FastSIMD_Level_Scalar.cpp',
    'FastSIMD/FastSIMD_Level_SSE2.cpp',
    'FastSIMD/FastSIMD_Level_SSE3.cpp',
    'FastSIMD/FastSIMD_Level_SSE41.cpp',
    'FastSIMD/FastSIMD_Level_SSE42.cpp',
    'FastSIMD/FastSIMD_Level_SSSE3.cpp',
]

# FastNoise files
fastnoise_inl = Glob('../include/FastNoise/*.inl')
fastnoise_generatores_inl = Glob('../include/FastNoise/Generatores/*.inl')
fastnoise_sources = [
    './src/FastNoise/Metadata.cpp',
    './src/FastNoise/SmartNode.cpp',
    './src/FastNoise/FastNoise_C.cpp'
]

Library('FastNoise', fastnoise_sources)