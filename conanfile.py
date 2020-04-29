from conans import ConanFile, CMake, tools, __version__ as conan_version
from conans.model.version import Version
from conans.tools import download, unzip
import os, re
import shutil

class Arpackpp(ConanFile):
    name = "arpack++"
    version = "2.3.0"
    license = "BSD"
    url = "https://github.com/m-reuter/arpackpp"
    settings = "os"
    generators = "cmake"
    requires = 'arpack-ng/3.7.0@davidace/stable'
    build_policy    = 'missing'
    options         = {
        "shared"            : [True, False],
        "fPIC"              : [True, False],
        "blas"              : ['OpenBLAS','MKL','Intel','Intel10_64lp','Intel10_64lp_seq','Intel10_64ilp',
                               'Intel10_64lp_seq', 'FLAME', 'Goto', 'ATLAS PhiPACK','Generic','All'],
        "interface64"       : [True,False],
        "mpi"               : [True,False],
        "prefer_pkgconfig"  : [True,False],
        "blas_libraries"    : "ANY",
        "lapack_libraries"  : "ANY",
    }
    default_options = {
        "shared"            : False,
        "fPIC"              : True,
        "blas"              : "OpenBLAS",
        "interface64"       : False,
        "mpi"               : False,
        "prefer_pkgconfig"   : False,
        "blas_libraries"    : None,
        "lapack_libraries"  : None,
    }

    _source_subfolder = "arpackpp-" + version
    _build_subfolder  = "arpackpp-" + version

    def configure(self):
        # Pass-through all the options to arpack-ng
        self.options["arpack-ng"].shared           = self.options.shared
        self.options["arpack-ng"].fPIC             = self.options.fPIC
        self.options["arpack-ng"].blas             = self.options.blas
        self.options["arpack-ng"].interface64      = self.options.interface64
        self.options["arpack-ng"].mpi              = self.options.mpi
        self.options["arpack-ng"].prefer_pkgconfig = self.options.prefer_pkgconfig
        self.options["arpack-ng"].blas_libraries   = self.options.blas_libraries
        self.options["arpack-ng"].lapack_libraries = self.options.lapack_libraries

    def source(self):
        ext = "tar.gz" if tools.os_info.is_linux else "zip"
        md5 = "1b09e35b6c44e118003922643b99978a" if tools.os_info.is_linux else "7069b2f5af8ae17fe036e7a33ce3306d"
        url = "https://github.com/m-reuter/arpackpp/archive/{0}.{1}".format(self.version,ext)
        tools.get(url=url, md5=md5)

    def package_id(self):
            self.info.header_only()

    def package(self):
        self.copy(pattern="*.h", src=self._source_subfolder + "/include", dst="include/arpack++")
        self.copy(pattern="README", src=self._source_subfolder + "/include", dst="include/arpack++")
        self.copy(pattern="LICENSE", src=self._source_subfolder, dst=".")

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "arpack++"
        self.cpp_info.names["cmake_find_package_multi"] = "arpack++"
        self.cpp_info.names['pkg_config'] = "arpack++"
