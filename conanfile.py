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
    license = "https://github.com/bincrafters/conan-gmp/blob/master/LICENSE"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
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
                replace_in_file("%s/%s/configure" % (self.conanfile_directory, self.sources_folder), old_str, new_str)

            self.run("%s && chmod +x ./configure && ./configure" % cd_build)
            self.run("%s && make" % cd_build)
            # According to the gmp readme file, make check should not be omitted
            # self.run("%s && make check" % cd_build)

    def package(self):
        self.copy("copying*", dst="licenses", src=self.sources_dir, ignore_case=True, keep_path=False)
        self.copy(pattern="gmp.h", dst="include", src=self.sources_dir)
        if self.options.shared:
            self.copy(pattern="libgmp.so*", dst="lib", keep_path=False)
            self.copy(pattern="libgmp.dylib", dst="lib", keep_path=False)
        else:
            self.copy(pattern="libgmp.a", dst="lib", keep_path=False)
            self.copy(pattern="libgmp.la", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
