#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class GmpConan(ConanFile):
    name = "gmp"
    version = "6.1.2"
    url = "https://github.com/bincrafters/conan-gmp"
    description = "GMP is a free library for arbitrary precision arithmetic, operating on signed integers, rational numbers, and floating-point numbers."
    website = "https://gmplib.org"
    license = "LGPL-3.0, GPL-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["FindGMP.cmake"]
    source_subfolder = "source_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "disable_assembly": [True, False], "run_checks": [True, False]}
    default_options = "shared=False", "fPIC=True", "disable_assembly=True", "run_checks=False"

    def configure(self):
        # Because this is pure C
        del self.settings.compiler.libcxx
        if self.settings.compiler == "Visual Studio":
            raise tools.ConanException("The gmp package cannot be deployed on Visual Studio.")

    def source(self):
        source_url = "https://gmplib.org/download/gmp"
        tools.get("{0}/{1}-{2}.tar.bz2".format(source_url, self.name, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = self.options.fPIC
        with tools.environment_append(env_build.vars):

            with tools.chdir(self.source_subfolder):

                if self.settings.os == "Macos":
                    tools.replace_in_file("configure", r"-install_name \$rpath/", "-install_name ")

                self.run("chmod +x configure")

                configure_args = []
                if self.options.disable_assembly:
                    configure_args.append('--disable-assembly')
                if self.options.shared:
                    configure_args.extend(["--enable-shared", "--disable-static"])
                else:
                    configure_args.extend(["--disable-shared", "--enable-static"])

                env_build.configure(args=configure_args)
                env_build.make()

                # According to the gmp readme file, make check should not be omitted, but it causes timeouts on the CI server.
                if self.options.run_checks:
                    env_build.make(args=['check'])

    def package(self):
        # dual license
        self.copy("COPYINGv2", dst="licenses", src=self.source_subfolder)
        self.copy("COPYING.LESSERv3", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="gmp.h", dst="include", src=self.source_subfolder)
        self.copy("FindGMP.cmake")
        if self.options.shared:
            self.copy(pattern="libgmp.so*", dst="lib", src="%s/.libs" % self.source_subfolder, keep_path=False)
            self.copy(pattern="libgmp.dylib", dst="lib", src="%s/.libs" % self.source_subfolder, keep_path=False)
            self.copy(pattern="libgmp.*.dylib", dst="lib", src="%s/.libs" % self.source_subfolder, keep_path=False)
        else:
            self.copy(pattern="libgmp.a", dst="lib", src="%s/.libs" % self.source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
