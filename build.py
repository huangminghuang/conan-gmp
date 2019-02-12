#!/usr/bin/env python
# -*- coding: utf-8 -*-


from cpt.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(pure_c=False)
    if platform.system() == "Linux":
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if settings["compiler"] == "clang" and settings["compiler.libcxx"] == "libstdc++":
                settings_libstdcxx11 = settings.copy()
                settings_libstdcxx11["compiler.libcxx"] = "libstdc++11"
                filtered_builds.append([settings_libstdcxx11, options, env_vars, build_requires])
            filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds
    builder.run()