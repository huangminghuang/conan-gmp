#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class GmpConan(ConanFile):
    name = "gmp"
    version = "6.1.2"
    url = "https://gmplib.org/"
    sources_dir = "sources"
    generators = "txt"
    description = "GMP is a free library for arbitrary precision arithmetic, operating on signed integers, rational numbers, and floating-point numbers."
    license = "GNU LGPL v3, GNU GPL v2"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "FindGMP.cmake"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "disable_assembly": [True, False], "run_checks": [True, False]}
    default_options = "shared=False", "fPIC=True", "disable_assembly=True", "run_checks=False"
    requires = ""

    def configure(self):
        if self.settings.os == "Windows":
            raise tools.ConanException("The gmp package cannot be deployed on Windows.")

    def source(self):
        source_url = "https://gmplib.org/download/gmp"
        tools.get("{0}/{1}-{2}.tar.bz2".format(source_url, self.name, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.sources_dir)

    def build(self):
        base_path = ("%s/" % self.conanfile_directory)
        cd_build = "cd %s%s" % (base_path, self.sources_dir)
        env = AutoToolsBuildEnvironment(self)
        env.fpic = self.options.fPIC 
        with tools.environment_append(env.vars):
            if self.settings.os == "Macos":
                old_str = '-install_name \\$rpath/\\$soname'
                new_str = '-install_name \\$soname'
                tools.replace_in_file("%s/%s/configure" % (self.conanfile_directory, self.sources_dir), old_str, new_str)

            self.run("%s && chmod +x ./configure && ./configure%s%s" % (cd_build, " --disable-assembly" if self.options.disable_assembly else "",
                                                                        " --disable-static" if self.options.shared else " --disable-shared"))
            self.run("%s && make" % cd_build)
            # According to the gmp readme file, make check should not be omitted, but it causes timeouts on the CI server.
            if self.options.run_checks:
                self.run("%s && make check" % cd_build)

    def package(self):
        # dual license
        self.copy("COPYINGv2", dst="licenses", src=self.sources_dir, ignore_case=True, keep_path=False)
        self.copy("COPYING.LESSERv3", dst="licenses", src=self.sources_dir, ignore_case=True, keep_path=False)
        self.copy(pattern="gmp.h", dst="include", src=self.sources_dir)
        self.copy("FindGMP.cmake")
        if self.options.shared:
            self.copy(pattern="libgmp.so*", dst="lib", src="%s/.libs" % self.sources_dir, keep_path=False)
            self.copy(pattern="libgmp.dylib", dst="lib", src="%s/.libs" % self.sources_dir, keep_path=False)
            self.copy(pattern="libgmp.10.dylib", dst="lib", src="%s/.libs" % self.sources_dir, keep_path=False)
        else:
            self.copy(pattern="libgmp.a", dst="lib", src="%s/.libs" % self.sources_dir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
