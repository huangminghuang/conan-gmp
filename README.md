[ ![Download](https://api.bintray.com/packages/bincrafters/public-conan/gmp%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/gmp%3Abincrafters/_latestVersion)
[![Build Status](https://travis-ci.org/bincrafters/conan-gmp.svg?branch=stable%2F6.1.2)](https://travis-ci.org/bincrafters/conan-gmp)

[Conan.io](https://conan.io) package for [gmp](https://gmplib.org/) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/gmp%3Abincrafters).

Note: Unfortunately, there is no build configuration for Windows provided for gmp by the gmp development team, so this conan package cannot be deployed on Windows.

## For Users: Use this package

### Basic setup

    $ conan install gmp/6.1.2@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    gmp/6.1.2@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

In order to enable assembly code, making the library run much faster turn off the `disable_assembly` option:

	$ mkdir build && cd build && conan install .. -o gmp:disable_assembly=False
	
The normal building procedure of gmp runs some checks to make sure that everything has been properly compiled. It is highly recommended that these checks are executed, in order to avoid calculation problems when using the library, but they have been disabled on travis because they cause timeouts to the builds (they take too long). If you want to be 100% certain that you are using a properly compiled gmp library you need to enable them and build locally:

	$ mkdir build && cd build && conan install .. -o gmp:run_checks=True --build gmp

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create bincrafters/stable

## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload gmp/6.1.2@bincrafters/stable --all -r bincrafters

## License
[LGPLv3](https://www.gnu.org/licenses/lgpl.html) | [GPLv2](https://www.gnu.org/licenses/gpl-2.0.html)
