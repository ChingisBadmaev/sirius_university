###########################################################################
# Copyright 2008-2019 Rogue Wave Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
###########################################################################
from pyimsl.util import imslRefs
from pyimsl.util.ImslErrorHandler import ImslErrorHandler
from pyimsl.util.Translator import Translator
from ctypes import cdll, CDLL, RTLD_GLOBAL
import platform as platform_info
from sys import platform
import os
import sys
import pyimsl


MATH = 1
STAT = 2


def loadEnv(varname, env):
    try:
        return env[varname]
    except KeyError:
        ext = {'nt': '.bat',
               'posix': '.sh'}
        msg = ("Environment variable '{varname}' not found, did you"
               " run cnlsetup{ext}?")
        raise LookupError(msg.format(varname=varname, ext=ext[os.name]))


def loadLibrary(libname, env):
    cnl_dir = loadEnv('CNL_DIR', env)
    lib_arch = loadEnv('LIB_ARCH', env)

    libname = os.path.join(cnl_dir, lib_arch, 'lib', libname)

    try:
        return cdll.LoadLibrary(libname)
    except OSError as exception:
        if os.name == 'posix':
            # An error occurred loading the library, likely due to
            # a missing libgomp dependency. Try loading libgomp
            # explicitly, however if this fails, propagate the
            # original failure.
            try:
                CDLL('libgomp.so.1', RTLD_GLOBAL)
                return cdll.LoadLibrary(libname)
            except Exception:
                raise exception
        else:
            raise


def imslLoad(type):
    """ Load IMSL math/stat shared lib
    """
    if type == MATH:
        if imslRefs.imslmath is None:
            libnames = {'nt': 'imslcmath_imsl_dll.dll',
                        'posix': 'libimslcmath_imsl.so'}
            imslRefs.imslmath = loadLibrary(libnames[os.name],
                                            os.environ)
            imslRefs.mathloaded = True
        imslRefs.mathErrorHandler = ImslErrorHandler(True)
        return imslRefs.imslmath
    else:
        imslLoad(MATH)
        if imslRefs.imslstat is None:
            libnames = {'nt': 'imslcstat_imsl_dll.dll',
                        'posix': 'libimslcstat_imsl.so'}
            imslRefs.imslstat = loadLibrary(libnames[os.name],
                                            os.environ)
            imslRefs.statloaded = True
        imslRefs.statErrorHandler = ImslErrorHandler(False)
        return imslRefs.imslstat
