import os
import sys
# import ctypes
from ctypes import c_void_p
from operator import attrgetter
import _ctypes
from time import sleep
import numpy.ctypeslib as npct
from os import path
from tempfile import gettempdir
from code_compiler import *
# from parcels.tools.loggers import logger

try:
    from mpi4py import MPI
except:
    MPI = None

try:
    from os import getuid
except:
    # Windows does not have getuid(), so define to simply return 'tmp'
    def getuid():
        return 'tmp'
try:
    from mpi4py import MPI
except:
    MPI = None
from pathlib import Path

def get_package_dir():
    return path.abspath(path.dirname(__file__))


def get_cache_dir():
    directory = path.join(gettempdir(), "PFL-%s" % getuid())
    Path(directory).mkdir(exist_ok=True)
    return directory

__all__ = ['LibraryRegisterC', 'InterfaceC']


class LibraryRegisterC:
    _data = {}

    def __init__(self):
        self._data = {}

    def __del__(self):
        for entry in self._data:
            while entry.register_count > 0:
                sleep(0.1)
            entry.unload_library()
            del entry

    def load(self, libname, src_dir=get_package_dir()):
        if libname not in self._data.keys():
            cppargs = []
            ccompiler = GNUCompiler(cppargs=cppargs, incdirs=[".", ], libdirs=[".", get_cache_dir()])
            self._data[libname] = InterfaceC(libname, ccompiler, src_dir)
        if not self._data[libname].is_compiled():
            self._data[libname].compile_library()
        if not self._data[libname].is_loaded():
            self._data[libname].load_library()

    def unload(self, libname):
        if libname in self._data.keys():
            self._data[libname].unload_library()
        #    del self._data[libname]

    def __getitem__(self, item):
        return self.get(item)

    def get(self, libname):
        if libname in self._data.keys():
            return self._data[libname]
        return None

    def register(self, libname):
        if libname in self._data.keys():
            self._data[libname].register()

    def deregister(self, libname):
        if libname in self._data.keys():
            self._data[libname].unregister()


class InterfaceC:

    def __init__(self, c_file_name, compiler, src_dir=get_package_dir()):
        basename = c_file_name
        src_pathfile = c_file_name
        if isinstance(basename, list) and len(basename) > 0:
            basename = basename[0]
        lib_path = basename
        lib_pathfile = os.path.basename(basename)
        lib_pathdir = os.path.dirname(basename)
        if lib_pathfile[0:3] != "lib":
            lib_pathfile = "lib"+lib_pathfile
            lib_path = os.path.join(lib_pathdir, lib_pathfile)
        if MPI and MPI.COMM_WORLD.Get_size() > 1:
            lib_pathfile = "%s_%d" % (lib_pathfile, MPI.COMM_WORLD.Get_rank())
            lib_path = os.path.join(lib_pathdir, lib_pathfile)
        if isinstance(src_pathfile, list):
            self.src_file = []
            if isinstance(src_dir, list):
                for fdir, fname in zip(src_dir, src_pathfile):
                    self.src_file.append("%s.c" % os.path.join(fdir, fname))
            else:
                for fname in src_pathfile:
                    self.src_file = "%s.c" % os.path.join(src_dir, fname)
        else:
            self.src_file = "%s.c" % os.path.join(src_dir, src_pathfile)
        self.lib_file = "%s.%s" % (os.path.join(get_cache_dir(), lib_path), 'dll' if sys.platform == 'win32' else 'so')
        self.log_file = "%s.log" % os.path.join(get_cache_dir(), basename)
        if os.path.exists(self.lib_file):
            self.compiled = True

        # self.compiler = GNUCompiler()
        self.compiler = compiler
        self.compiled = False
        self.loaded = False
        self.libc = None
        self.register_count = 0

    def __del__(self):
        self.unload_library()
        self.cleanup_files()

    def is_compiled(self):
        return self.compiled

    def is_loaded(self):
        return self.loaded

    def compile_library(self):
        """ Writes kernel code to file and compiles it."""
        if not self.compiled:
            self.compiler.compile(self.src_file, self.lib_file, self.log_file)
            # logger.info("Compiled %s ==> %s" % (self.name, self.lib_file))
            print("Compiled %s ==> %s" % (self.src_file, self.lib_file))
            # self._cleanup_files = finalize(self, package_globals.cleanup_remove_files, self.lib_file, self.log_file)
            self.compiled = True

    def cleanup_files(self):
        if os.path.isfile(self.lib_file):
            [os.remove(s) for s in [self.lib_file, self.log_file] if os._exists(s)]

    def unload_library(self):
        if self.libc is not None and self.compiled and self.loaded:
            _ctypes.FreeLibrary(self.libc._handle) if sys.platform == 'win32' else _ctypes.dlclose(self.libc._handle)
            del self.libc
            self.libc = None
            self.loaded = False

    def load_library(self):
        if self.libc is None and self.compiled and not self.loaded:
            self.libc = npct.load_library(self.lib_file, '.')
            # self._cleanup_lib = finalize(self, package_globals.cleanup_unload_lib, self.libc)
            self.loaded = True

    def register(self):
        self.register_count += 1
        print("lib '{}' register (count: {})".format(self.lib_file, self.register_count))

    def unregister(self):
        self.register_count -= 1
        print("lib '{}' de-register (count: {})".format(self.lib_file, self.register_count))

    def load_functions(self, function_param_array=[]):
        """

        :param function_name_array: array of dictionary {"name": str, "return": type, "arguments": [type, ...]}
        :return: dict (function_name -> function_handler)
        """
        result = dict()
        print(self.libc)
        # for i in range(0, 3):
        #     print(self.libc[int(i)])
        if self.libc is None or not self.compiled or not self.loaded:
            return result
        for function_param in function_param_array:
            print(function_param)
            if isinstance(function_param, dict) and \
                    isinstance(function_param["name"], str) and \
                    isinstance(function_param["return"], type) or function_param["return"] is None and \
                    isinstance(function_param["arguments"], list):
                if int(platform.python_version_tuple()[1])<7:
                    result[function_param["name"]] = getattr(self.libc, function_param["name"])
                else:
                    result[function_param["name"]] = self.libc[function_param["name"]]
                result[function_param["name"]].restype = function_param["return"]
                result[function_param["name"]].argtypes = function_param["arguments"]
        return result
