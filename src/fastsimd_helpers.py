def __get_all_sources(env_base: "Environment"):
    all_sources = []
    if env_base['fastsimd_compile_have_neon']:
        all_sources = [
            'FastSIMD/FastSIMD.cpp',
            'FastSIMD/FastSIMD_Level_NEON.cpp',
            'FastSIMD/FastSIMD_Level_Scalar.cpp'
        ]
    elif env_base['fastsimd_compile_arm']:
        all_sources = [
            'FastSIMD/FastSIMD.cpp',
            'FastSIMD/FastSIMD_Level_Scalar.cpp'
        ]
    else:
        all_sources = [
            'FastSIMD/FastSIMD.cpp',
            'FastSIMD/FastSIMD_Level_AVX2.cpp',
            'FastSIMD/FastSIMD_Level_AVX512.cpp',
            'FastSIMD/FastSIMD_Level_Scalar.cpp',
            'FastSIMD/FastSIMD_Level_SSE2.cpp',
            'FastSIMD/FastSIMD_Level_SSE3.cpp',
            'FastSIMD/FastSIMD_Level_SSE41.cpp',
            'FastSIMD/FastSIMD_Level_SSE42.cpp',
            'FastSIMD/FastSIMD_Level_SSSE3.cpp'
        ]

    return all_sources


def __get_avx_sources_cl_msvc(env_base: "Environment", sources):
    objs = []

    env_avx2 = env_base.Clone()
    env_avx2.AppendUnique(CPPFLAGS=['/arch:AVX2'])
    avx2_file = 'FastSIMD/FastSIMD_Level_AVX2.cpp'
    objs.append(env_avx2.Object(avx2_file))
    sources.remove(avx2_file)

    env_avx512 = env_base.Clone()
    env_avx512.AppendUnique(CPPFLAGS=['/arch:AVX512'])
    avx512_file = 'FastSIMD/FastSIMD_Level_AVX512.cpp'
    objs.append(env_avx512.Object(avx512_file))
    sources.remove(avx512_file)

    return sources, objs


def __get_32bit_sources_cl_msvc(env_base: "Environment", sources):
    objs = []

    env_sse = env_base.Clone()
    env_sse.AppendUnique(CPPFLAGS=['/arch:SSE'])
    sse_files = [
        'FastSIMD/FastSIMD_Level_Scalar.cpp'
    ]
    for file in sse_files:
        objs.append(env_sse.Object(file))
        sources.remove(file)

    env_sse2 = env_base.Clone()
    env_sse2.AppendUnique(CPPFLAGS=['/arch:SSE2'])
    sse2_files = [
        'FastSIMD/FastSIMD_Level_SSE2.cpp',
        'FastSIMD/FastSIMD_Level_SSE3.cpp',
        'FastSIMD/FastSIMD_Level_SSE41.cpp',
        'FastSIMD/FastSIMD_Level_SSE42.cpp',
        'FastSIMD/FastSIMD_Level_SSSE3.cpp'
    ]
    for file in sse2_files:
        objs.append(env_sse2.Object(file))
        sources.remove(file)

    return sources, objs


def __get_armv7_sources_cl_msvc(env_base: "Environment", sources):
    objs = []

    env_neon = env_base.Clone()
    env_neon.AppendUnique(CPPFLAGS=['/arch:NEON'])
    neon_file = 'FastSIMD/FastSIMD_Level_NEON.cpp'
    objs.append(env_neon.Object(neon_file))
    sources.remove(neon_file)

    return sources, objs


def get_sources_cl_msvc(env_base: "Environment"):

    all_sources = __get_all_sources(env_base)
    
    fastsimd_objs = []
    if not env_base['fastsimd_compile_arm']:
        if env_base['sizeof_void_p'] == 4:
            all_sources, fastsimd_32bit_objs = __get_32bit_sources_cl_msvc(env_base, all_sources)
            fastsimd_objs += fastsimd_32bit_objs
        all_sources, fastsimd_avx_objs = __get_avx_sources_cl_msvc(env_base, all_sources)
        fastsimd_objs += fastsimd_avx_objs
    elif env['fastsimd_compile_armv7']:
        all_sources, fastsimd_neon_objs = __get_armv7_sources_cl_msvc(env_base, all_sources)
        fastsimd_objs += fastsimd_neon_objs

    # Any sources that have not been objectified yet use the base environment
    for file in all_sources:
        fastsimd_objs.append(env_base.Object(file))
        
    return fastsimd_objs

def __get_32bit_sources_non_msvc(env_base: "Environment", sources):
    objs = []

    env_msse = env_base.Clone()
    env_msse.AppendUnique(CPPFLAGS=['-msse'])
    msse_file = 'FastSIMD/FastSIMD_Level_Scalar.cpp'
    objs.append(env_msse.Object(msse_file))
    sources.remove(msse_file)

    env_msse2 = env_base.Clone()
    env_msse2.AppendUnique(CPPFLAGS=['-msse2'])
    msse2_file = 'FastSIMD/FastSIMD_Level_SSE2.cpp'
    objs.append(env_msse2.Object(msse2_file))
    sources.remove(msse2_file)

    return sources, objs

def __get_msse_sources(env_base: "Environment", sources):
    objs = []

    msse_sources = [
        'FastSIMD/FastSIMD_Level_SSE3.cpp',
        'FastSIMD/FastSIMD_Level_SSSE3.cpp',
        'FastSIMD/FastSIMD_Level_SSE41.cpp',
        'FastSIMD/FastSIMD_Level_SSE42.cpp',
    ]

    env_msse = env_base.Clone()
    
    objs.append(env_msse.Object(msse_sources[0], CPPFLAGS='-msse3'))
    objs.append(env_msse.Object(msse_sources[1], CPPFLAGS='-mssse3'))
    objs.append(env_msse.Object(msse_sources[2], CPPFLAGS='-msse4.1'))
    objs.append(env_msse.Object(msse_sources[3], CPPFLAGS='-msse4.2'))

    sources = [source for source in sources if source not in msse_sources]

    return sources, objs


def __get_avx_sources_non_msvc(env_base: "Environment", sources):
    objs = []

    env_avx2 = env_base.Clone()
    env_avx2.AppendUnique(CPPFLAGS=['-mavx2','-mfma'])
    avx2_file = 'FastSIMD/FastSIMD_Level_AVX2.cpp'
    objs.append(env_avx2.Object(avx2_file))
    sources.remove(avx2_file)

    env_avx512 = env_base.Clone()
    env_avx512.AppendUnique(CPPFLAGS=['-mavx512f','-mavx512dq','-mfma'])
    avx512_file = 'FastSIMD/FastSIMD_Level_AVX512.cpp'
    objs.append(env_avx512.Object(avx512_file))
    sources.remove(avx512_file)

    return sources, objs


def __get_armv7_sources_non_msvc(env_base: "Environemnt", sources):
    objs = []

    env_neon = env_base.Clone()
    env_neon.AppendUnique(CPPFLAGS=['-march=armv7-a','-mfpu=neon'])
    neon_file = 'FastSIMD/FastSIMD_Level_NEON.cpp'
    objs.append(env_neon.Object(neon_file))
    sources.remove(neon_file)

    return sources, objs


def get_sources_non_msvc(env_base: "Environment"):
    all_sources = __get_all_sources(env_base)

    fastsimd_objs = []
    if not env_base['fastsimd_compile_arm']:
        if env_base['sizeof_void_p'] == 4 or '-m32' in env_base['CPPFLAGS']:
            all_sources, fastsimd_32bit_objs = __get_32bit_sources_non_msvc(env_base, all_sources)
            fastsimd_objs += fastsimd_32bit_objs
        all_sources, fastsimd_msse_objs = __get_msse_sources(env_base, all_sources)
        all_sources, fastsimd_avx_objs = __get_avx_sources_non_msvc(env_base, all_sources)

        fastsimd_objs += fastsimd_msse_objs
        fastsimd_objs += fastsimd_avx_objs
    elif env_base['fastsimd_compile_armv7']:
        all_sources, fastsimd_neon_objs = __get_armv7_sources_non_msvc(env_base, all_sources)
        fastsimd_objs += fastsimd_neon_objs

    for file in all_sources:
        fastsimd_objs.append(env_base.Object(file))

    return fastsimd_objs