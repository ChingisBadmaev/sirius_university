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
from numpy import array, ndarray, empty, double, flatiter
# need to rename as we use shape as keyword
from numpy import shape as numpyShape
from ctypes import c_int, c_long, c_double, c_char_p, byref
from datetime import date
from pyimsl.util import imslRefs
from pyimsl.math.mathStructs import f_complex
from pyimsl.math.mathStructs import d_complex
from pyimsl.math.mathStructs import tm
from pyimsl.math.mathStructs import Imsl_c_sparse_elem
from pyimsl.math.mathStructs import Imsl_d_sparse_elem
from pyimsl.util.ImslError import ImslError
from pyimsl.util.Translator import Translator
from pyimsl.util.imslLoad import imslLoad
import platform as platform_info
from sys import platform
import collections

MATH = 1
STAT = 2

ctypesTypeMap = {'char': 'c_char',
                 'wchar_t': 'c_wchar',
                 'unsigned char': 'c_ubyte',
                 'short': 'c_short',
                 'unsigned short': 'c_short',
                 'int': 'c_int',
                 'unsigned int': 'c_uint',
                 'long': 'c_long',
                 'unsigned long': 'c_ulong',
                 'long long': 'c_longlong',
                 'unsigned long long': 'c_ulonglong',
                 'float': 'c_float',
                 'double': 'c_double',
                 'char *': 'c_char_p',
                 'wchar_t *': 'c_wchar_p',
                 'void *': 'c_void_p'}

cScalarTypes = [c_double,
                c_int,
                c_long,
                c_char_p,
                tm,
                f_complex,
                d_complex]

pythonReservedWords = set(["False", "None", "True", "and", "as", "assert", "break", "class", "continue",
                           "def", "del", "elif", "else", "except", "exec",
                           "finally", "for", "from", "global", "if", "import",
                           "in", "is", "lambda", "nonlocal", "not", "or", "pass", "print",
                           "raise", "return", "try", "while", "with", "yield"])


def loadimsl(type):
    """ Load IMSL math/stat shared lib and set up error handling
    """
    global _mathErrorHandler, _statErrorHandler
    if type == MATH:
        if imslRefs.mathloaded is None:
            imslmath = imslLoad(type)
            _mathErrorHandler = imslRefs.mathErrorHandler
            return imslmath
        else:
            return imslRefs.imslmath
    if type == STAT:
        if imslRefs.statloaded is None:
            imslstat = imslLoad(type)
            _mathErrorHandler = imslRefs.mathErrorHandler
            _statErrorHandler = imslRefs.statErrorHandler
            return imslstat
        else:
            return imslRefs.imslstat


def toNumpyArray(variable, name, dtype='double', shape=None, expectedShape=None):
    """ Convert many objects (lists, tupples, even numpy arrays of wrong type) to
    a numpy arrays of a specific type. As part of this process the shape of the ayyay is
    determined and returned. The use of expectedShape allows a specific dimensionality (when 0's
    are used in the passed tuple) or even specific array sizes (values other than 0) to be
    checked for and an error generated if input does not match.
    """
    isNone = False  # flag if None was passed

    if dtype == 'f_complex' or dtype == 'd_complex':  # support for complex data
        tshape = getShape(variable)
        ndim = len(tshape)

        # TODO: only 1D and 2D complex arrays supported
        if len(tshape) == 2:  # 2D complex
            d0 = tshape[0]
            d1 = tshape[1]
            if dtype == 'f_complex':
                retvar = (f_complex * (d0 * d1))()
            else:
                retvar = (d_complex * (d0 * d1))()
            for i in range(0, d0):
                for j in range(0, d1):
                    if isinstance(variable, ndarray):
                        retvar[i * d1 + j].re = variable[i, j].real
                        retvar[i * d1 + j].im = variable[i, j].imag
                    else:
                        retvar[i * d1 + j].re = variable[i][j].real
                        retvar[i * d1 + j].im = variable[i][j].imag

        elif len(tshape) == 1:  # 1D complex
            if dtype == 'f_complex':
                retvar = (f_complex * len(variable))()
            else:
                retvar = (d_complex * len(variable))()
            for i in range(0, len(variable)):
                retvar[i].re = variable[i].real
                retvar[i].im = variable[i].imag

        else:  # scalar complex
            if variable is None:
                retvar = array([None])
                isNone = True
            else:
                retvar = d_complex()  # return a scalar
                retvar.re = variable.real
                retvar.im = variable.imag
                if isWin64():
                    retvar = retvar
                    # retvar = byref(retvar)
    elif dtype == 'date':  # support for date data
        tshape = getShape(variable)
        ndim = len(tshape)

        # TODO: only 1D arrays supported
        if len(tshape) == 1:  # 1D date array
            retvar = (tm * (tshape[0]))()
            for i in range(0, len(variable)):
                retvar[i] = dateConvert(
                    variable[i], toStructTm=True, noWin64Byref=True)
        else:  # scalar date
            retvar = dateConvert(variable, toStructTm=True)
    elif dtype == 'Imsl_c_sparse_elem':
        tshape = getShape(variable)
        ndim = len(tshape)
        # TODO: only 2d (mx3) arrays and scalars are supported
        if len(tshape) == 2:  # 2-D lists
            if tshape[1] != 3:
                errStr = Translator.getString("sizeerror1")
                raise ValueError(name + errStr + " mx3")
            retvar = (Imsl_c_sparse_elem * (tshape[0]))()
            for i in range(0, tshape[0], 1):
                temp = d_complex()
                temp.re = (variable[i][2]).real
                temp.im = (variable[i][2]).imag
                retvar[i] = variable[i][0], variable[i][1], temp
        if len(tshape) == 1:  # scalar- a list with [row,col,value]
            retvar = (Imsl_c_sparse_elem)()
            if tshape[0] != 3:
                errStr = Translator.getString("sizeerror1")
                errStr2 = Translator.getString("sizeerror2")
                raise ValueError(name + errStr + errStr2)
            temp = d_complex()
            temp.re = (variable[2]).real
            temp.im = (variable[2]).imag
            retvar[i] = variable[0], variable[1], temp
    elif dtype == 'Imsl_d_sparse_elem':
        tshape = []
        if (isinstance(variable, list)):
            tshape.append(len(variable))
            if (isinstance(variable[0], list)):
                tshape.append(len(variable[0]))
        ndim = len(tshape)
        # TODO: only 2d (mx3) arrays and scalars are supported
        if len(tshape) == 2:  # 2-D lists
            if tshape[1] != 3:
                errStr = Translator.getString("sizeerror1")
                errStr2 = Translator.getString("sizeerror3")
                raise ValueError(name + errStr + errStr2)
            retvar = (Imsl_d_sparse_elem * (tshape[0]))()
            for i in range(0, tshape[0], 1):
                retvar[i] = variable[i][0], variable[i][1], variable[i][2]
        if len(tshape) == 1:  # scalar- a list with [row,col,value]
            retvar = (Imsl_c_sparse_elem)()
            if tshape[0] != 3:
                errStr = Translator.getString("sizeerror1")
                errStr2 = Translator.getString("sizeerror2")
                raise ValueError(name + errStr + errStr2)
            retvar[i] = variable[0], variable[1], variable[2]
    else:  # int/float data
        if dtype == 'int':
            dtype = 'int32'
        if isinstance(variable, ndarray):  # already is numpy but make sure it is desired type
            if variable.dtype == dtype:
                retvar = variable
            else:
                retvar = variable.astype(dtype)
            tshape = variable.shape
            retvar = variable.astype(dtype)
        elif isinstance(variable, list) or isinstance(variable, tuple) or isinstance(variable, flatiter):
            # Some type checking:
            if len(variable) > 0:
                if isinstance(variable[0], complex):
                    errStr = Translator.getString("sizeerror4")
                    raise ValueError(name + errStr + repr(dtype))
                if isinstance(variable[0], str) and dtype != 'str':
                    errStr = Translator.getString("sizeerror4")
                    raise ValueError(name + errStr + repr(dtype))
            retvar = array(variable, dtype=dtype)
        else:  # is a scalar
            if variable is None:
                retvar = array([None])
                isNone = True
            else:
                if not isinstance(variable, int) and not isinstance(variable, float):
                    errStr = Translator.getString("sizeerror4")
                    raise ValueError(name + errStr + repr(dtype))
                retvar = array([variable], dtype=dtype)
        ndim = retvar.ndim
        tshape = retvar.shape

    # calculate dims
    # TODO: the use of the shape param is required else code fails,
    #       but shape is normally (or always) needed anyway.
    if shape is not None:
        if expectedShape is None:  # if not specified then whatever we got is the correct shape
            shape = tshape
            expectedDims = len(shape)
        else:  # construct shape
            if isinstance(expectedShape, tuple):
                expectedDims = len(expectedShape)
            else:
                expectedDims = 1
            nshape = len(tshape)
            shape[:] = []
            for i in range(0, expectedDims):
                if isNone:
                    shape.append(0)
                else:
                    if i < nshape:
                        shape.append(tshape[i])
                    # if we have additional expected dimensions just make them size 1 (degenerate)
                    else:
                        shape.append(1)

        # Test/calculate Dims
        if ndim > expectedDims:
            errStr = Translator.getString("sizeerror19")
            errStr2 = Translator.getString("sizeerror20")
            raise ValueError(name + errStr + repr(ndim)
                             + errStr2 + repr(expectedDims))

    # Test size for each dimension
    if not(expectedShape is None):
        if expectedDims == 1:  # expectedShape is a scalar not array
            if expectedShape != 0:  # 0 is a special indicator that any size is allowed
                if shape[0] != expectedShape:
                    errStr = Translator.getString("sizeerror21")
                    errStr2 = Translator.getString("sizeerror20")
                    raise ValueError(name + errStr + " 1 "
                                     + errStr2 + repr(expectedShape))
        else:
            for i in range(0, expectedDims):
                if expectedShape[i] != 0:
                    if shape[i] != expectedShape[i]:
                        errStr = Translator.getString("sizeerror21")
                        errStr2 = Translator.getString("sizeerror20")
                        raise ValueError(
                            name + errStr + repr(i) + errStr2 + repr(expectedShape[i]))
    # The column_stack, hstack,etc function in numpy change how the c data is
    # stored internally.  Performing a <varname>.ctypes.data_as(c_void_p) in the
    # python wrapper results in misplaced values in an array.  for example,
    # a=ones((10),dtype=10)
    # b = ones((10),dtype=10)+3
    # create a 10x2 array from two 1-d arrays
    # c = column_stack((a,b))
    # After the call to column_stack, it is not contiguous memory layout
    # writeMatrix("C",c)
    #                         c
    #                 1                     2
    # 1                1.0             1.0
    # 2                1.0             1.0
    # 3                1.0             1.0
    # 4                1.0             1.0
    # 5                1.0             1.0
    # 6               10.2            10.2
    # 7               10.2            10.2
    # 8               10.2            10.2
    # 9               10.2            10.2
    # 10              10.2            10.2
    # the above output should have only 1's in column 1.
    # The writeMatrix function produces the wrong results because we use the
    # ctypes.data_as(c_void_p) in the wrapper code.  If you try this from the
    # python command line, it works the way it is suppose to as numpy knows how
    # to deal with the memory of changed with the column_stack call.  So, there
    # is some sort of disconnect between ctypes and numpy after a call to
    # column_stack function.
    # need to take care of this situation with the following hack.  We can also
    # fix ctypes.data_as or file a bug with numpy or ctypes group.
    if (isinstance(retvar, ndarray)):
        if(not retvar.flags.c_contiguous or not retvar.flags.f_contiguous):
            retvar = retvar.copy()
    return retvar


def toDouble(variable, name):
    """ Util to cast scalar to double (never used though)
    """
    try:
        dvariable = float(variable)
    except ValueError:
        errStr = Translator.getString("sizeerror5")
        raise ValueError(name + errStr)
    return dvariable


def checkForList(variable, name, size=0, listOut=False):
    """ Test for list, which is required for all output params. Empty the passed List
    if this is an output var (but not if inout). A numpy array is allowed as well unless
    listOut=True is set, which is used for multiparam return keywords.
    """
    if (isinstance(variable, list)) or isinstance(variable, ndarray):
        pass
    else:
        if listOut:
            errStr = Translator.getString("sizeerror6")
            raise ValueError(name + errStr)
        else:
            errStr = Translator.getString("sizeerror7")
            raise ValueError(name + errStr)
    if size > 0:  # is input var
        if isinstance(variable, ndarray):
            length = variable.size
        else:
            length = len(variable)
        if length != size:
            errStr = Translator.getString("sizeerror8")
            raise ValueError(name + errStr + str(size))
    else:  # is output
        # Clear if is a list as we will append result
        if not isinstance(variable, ndarray):
            if len(variable) > 0:
                variable[:] = []


def checkForBoolean(variable, name):
    """ Test for boolean input param
    """
    if variable is not True and variable is not False and variable is not None:
        errStr = Translator.getString("sizeerror9")
        raise ValueError(name + errStr)


def checkForInt(variable, name, min=None, max=None):
    """ Test for integer input param
    """
    if not (min is None):
        if variable < min:
            errStr = Translator.getString("sizeerror10")
            raise ValueError(name + errStr + min)
    if not (max is None):
        if variable > max:
            errStr = Translator.getString("sizeerror11")
            raise ValueError(name + errStr + min)


def checkForStr(variable, name):
    """ Test for string input param
    """
    if ((not isinstance(variable, str)) & (not isinstance(variable, bytes))):
        errStr = Translator.getString("sizeerror12")
        raise ValueError(name + errStr)


def toByte(variable, codec='utf-8'):
    if (isinstance(variable, str)):
        return str.encode(variable, codec, 'replace')
    else:
        return variable


def toStr(variable, codec='utf-8'):
    if (isinstance(variable, bytes)):
        return bytes.decode(variable, codec, 'replace')
    else:
        return variable


def checkForCallable(fcn, name):
    """ Test for callable function input param
    """
    if not isinstance(fcn, collections.Callable):
        errStr = Translator.getString("sizeerror13")
        raise ValueError(name + errStr)


def checkForDict(variable, var_name, keys):
    """ Check to make sure 'variable' is a dictionary,
        and that it contains the keys in the list called 'keys'.
        If not, throw an exception.
    """
    if (not(variable is None)) and \
       (not(var_name is None)) and \
       (not(keys is None)):
        if isinstance(variable, dict):
            foundKey = True
            for key in keys:
                if key not in variable:
                    foundKey = False
                    break
            if (foundKey):
                return
    errStr = Translator.getString("sizeerror14")
    raise ValueError(var_name + repr(errStr) + repr(keys))


def checkForNumpy(variable, name, dtype=None):
    """ Check to make sure 'variable' is a numpy array,
            and that it is of right data type
    """
    if isinstance(variable, ndarray):
        pass
    else:
        errStr = Translator.getString("sizeerror15")
        raise ValueError(name + errStr)
    if dtype is not None:
        if(variable.dtype == dtype):
            pass
        else:
            errStr = Translator.getString("sizeerror16")
            raise ValueError(name + ": " + dtype + errStr)


def fatalErrorCheck(type):
    """ Test for any IMSL errors generated in the cnl call and raise an exception if caught
    """
    global _mathErrorHandler, _statErrorHandler
    if (type == MATH):
        if (_mathErrorHandler is None):   # Shouldn't happen
            raise ImslError(None, None, "Math error handler not registered")
        else:
            _mathErrorHandler.handleError()
    else:
        if (_statErrorHandler is None):   # Shouldn't happen
            raise ImslError(None, None, "Stat error handler not registered")
        else:
            _statErrorHandler.handleError()


def free(ptr):
    """ Wrapper to C library free() function
    """
    if not(ptr is None):
        from pyimsl.util.VersionFacade import VersionFacade
        # Required for Vista to use free provided by IMSL
        ver = VersionFacade.getCnlVersion()
        if (ver.majorVersion >= 7.0):
            pyimslFree = None
            if imslRefs.mathloaded:
                from pyimsl.math.free import free as pyimslFree
                if pyimslFree is not None:
                    pyimslFree(ptr)
        else:
            imslRefs.libc.free(ptr)


def processRet(cvar, shape=(1), result=False, inout=False, pyvar=None,
               createArray=False, key=None, freemem=True):
    """ Take resulting ctype or numpy array values returned from IMSL and package for return, as a numpy
    array for result parameters or as nested List for keyword parameters.
    """
    if inout:  # clear it before we put data back
        if isinstance(pyvar, list):
            pyvar[:] = []
        if isinstance(cvar, ndarray):  # we can get the shape from an ndarray (but not from ctypes)
            shape = numpyShape(cvar)
            # If a pyvar was passed in and it was not cast to another dtype - we do not need
            # to copy anything and can just return
            if isinstance(pyvar, ndarray) and (id(pyvar) == id(cvar)):
                return

    # Test for NULL cvar and return None if so
    try:
        if shape != 1:  # if not a scalar
            # will error if cvar is null - can't find a better way to test
            elem1 = cvar[0]
    except Exception:
        if result:
            return None
        else:  # keyword param
            if isinstance(pyvar, ndarray):
                pyvar.resize(1, refcheck=0)
                pyvar[0] = None
            else:
                pyvar.append(None)
            return

    if type(cvar) in cScalarTypes:  # is a scalar
        if isinstance(cvar, tm):
            value = dateConvert(cvar)
        elif isinstance(cvar, c_char_p):
            value = str(cvar)
        elif isinstance(cvar, f_complex) or isinstance(cvar, d_complex):
            value = complex(cvar.re, cvar.im)
        else:
            value = cvar.value

        if result:
            return value
        else:  # keyword param
            if isinstance(pyvar, ndarray):
                pyvar.resize(1, refcheck=0)
                pyvar[0] = value
            elif isinstance(pyvar, list):
                pyvar.append(value)
            elif isinstance(pyvar, dict):
                pyvar[key] = value
            else:
                errStr = Translator.getString("fatalerror2")
                raise ValueError(errStr)

    else:  # Array
        shape = filterShape(shape)
        if shape[0] == 0:
            return  # nothing to return - also we don't want to free
            # cvar since cvar may not even have been allocated

        # Handling for string arrays (for row_labels in stat chap4)
        # Note: really not too useful for ndarrays because you must
        # initialize a string ndarray with a string size that is as long as the longest
        # string to be returned, For example: param = array('      ', dtype='str')
        # best to just use lists for output strings
        if isinstance(cvar[0], bytes):
            strList = []
            for i in range(0, shape[0]):
                strList.append(bytes.decode(cvar[i]))
            if isinstance(pyvar, ndarray):
                pyvar.resize(shape[0], refcheck=0)
                pyvar[:] = strList
            else:  # list
                pyvar[:] = strList

        else:  # Not a string array
            if isinstance(pyvar, ndarray):
                ctypeToNumpyArray(cvar, shape, inout,
                                  pyvar=pyvar, freemem=freemem)
            else:
                pyarr = ctypeToNumpyArray(cvar, shape, inout, freemem=freemem)

                if result:
                    return pyarr
                else:
                    if isinstance(pyvar, dict):
                        pyvar[key] = pyarr.tolist()
                    elif createArray:  # append a single list to pyvar
                        pyvar.append(pyarr.tolist())
                    else:  # append individual values (replace List with result)
                        pyvar[:] = [arr.tolist() if isinstance(
                            arr, ndarray) else arr for arr in pyarr]


def toCtypesType(cDatatype, isPointer=False):
    """ Convert from a C datatype to a Ctypes datatype.
    It seems like this utility should be available in ctypes,
    but I haven't been able to find it.
    The table of C vs. ctypes types is in the ctypes tutorial.
    """
    if (cDatatype == "string"):
        if (isPointer):
            return "POINTER(c_char_p)"
        else:
            return "c_char_p"
    if (cDatatype == "char" and isPointer):
        return "c_char_p"
    if (cDatatype == "void"):
        if (isPointer):
            return "c_void_p"
        else:
            return "None"
    if (cDatatype in ctypesTypeMap):
        if (isPointer):
            return "POINTER(" + ctypesTypeMap[cDatatype] + ")"
        else:
            return ctypesTypeMap[cDatatype]
    return cDatatype


def filterShape(shape=None):
    """ Internal utility to process shape as int, long, c_long, c_int, or tuple containing any
    combination of these and return new tuple of longs
    """
    tshape = []
    if isinstance(shape, tuple):
        for entry in shape:
            if isinstance(entry, c_long) or isinstance(entry, c_int):
                tshape.append(int(entry.value))
            else:
                tshape.append(int(entry))

    elif isinstance(shape, c_long) or isinstance(shape, c_int):
        tshape.append(int(shape.value))
    else:
        tshape.append(int(shape))
    return tshape


def ctypeToNumpyArray(cvar, shape, inout, pyvar=None, freemem=True):
    """ Internal utility to copy IMSL output to numpy arrays
    """
    if isinstance(cvar[0], f_complex) or isinstance(cvar[0], d_complex):  # Complex data
        if not(pyvar is None):
            pyvar.resize(shape, refcheck=0)
        else:
            pyvar = empty(shape=shape, dtype=complex)
        flatiter = pyvar.flat
        for i in range(len(flatiter)):
            flatiter[i] = complex(cvar[i].re, cvar[i].im)

    elif isinstance(cvar[0], tm):  # date data
        if not(pyvar is None):
            pyvar.resize(shape, refcheck=0)
        else:
            pyvar = empty(shape=shape, dtype=date)
        flatiter = pyvar.flat
        for i in range(len(flatiter)):
            flatiter[i] = dateConvert(cvar[i])

    elif isinstance(cvar[0], Imsl_d_sparse_elem):  # sparse doubles
        if not(pyvar is None):
            pyvar.resize((shape[0], 3), refcheck=0)
        else:
            # date type creates an array of objects
            pyvar = empty(shape=(shape[0], 3), dtype=date)
        for i in range(0, shape[0]):
            pyvar[i, 0:3] = [cvar[i].row, cvar[i].col, cvar[i].val]

    elif isinstance(cvar[0], Imsl_c_sparse_elem):  # sparse complex
        if not(pyvar is None):
            pyvar.resize((shape[0], 3), refcheck=0)
        else:
            # date type creates an array of objects
            pyvar = empty(shape=(shape[0], 3), dtype=date)
        for i in range(0, shape[0]):
            temp = cvar[i].val
            pyvar[i, 0:3] = [cvar[i].row, cvar[i].col,
                             (complex(temp.re, temp.im))]

    else:  # is an int or double
        if isinstance(cvar[0], int):
            dtype = 'int'
        else:
            dtype = 'double'

        if not(pyvar is None):
            pyvar.resize(shape, refcheck=0)
        else:
            pyvar = empty(shape=shape, dtype=dtype)
        flatiter = pyvar.flat
        if isinstance(cvar, ndarray):
            flatcvar = cvar.flat
            flatiter[:] = flatcvar[0:len(flatiter)]
        else:
            flatiter[:] = cvar[0:len(flatiter)]

    if not inout and freemem and not isinstance(cvar, ndarray):
        free(cvar)
    return pyvar


def complexConvert(value, toDComplex=False, noWin64Byref=True):
    """ Create a scalar complex value.
        If toDComplex is True, create a CNL d_complex struct.
        Otherwise, create a Python complex value.
        The input value can be any Python scalar value or a
        d_complex or python complex value.
    """
    if isinstance(value, ndarray) or \
       isinstance(value, list) or \
       isinstance(value, tuple) or \
       isinstance(value, flatiter):
        errStr = Translator.getString("sizeerror17")
        raise ValueError(errStr)

    if isinstance(value, complex):
        real = value.real
        imag = value.imag
    elif (isinstance(value, d_complex)) or (isinstance(value, f_complex)):
        real = value.re
        imag = value.im
    else:
        real = value
        imag = 0.0

    if toDComplex:
        result = d_complex()
        result.re = real
        result.im = imag
        if isWin64() and not noWin64Byref:
            return byref(result)
        else:
            return result
    else:
        return complex(real, imag)


def dateConvert(value, toStructTm=False, noWin64Byref=True):
    """ Create a scalar date value.
        if toStructTm is True, create a ctypes object using the
        date part of struct tm.
        Otherwise, create a python date object.
        Note that only struct tm and python date objects
        are valid inputs.
    """
    # NOTE: struct tm has year as # years after 1900,
    # and month as # months after January.
    if isinstance(value, date):
        year = value.year
        month = value.month
        day = value.day
    elif isinstance(value, tm):
        year = value.tm_year + 1900
        month = value.tm_mon + 1
        day = value.tm_mday
    else:
        errStr = Translator.getString("sizeerror18")
        raise ValueError(errStr)

    if toStructTm:
        result = tm()
        result.tm_year = year - 1900
        result.tm_mon = month - 1
        result.tm_mday = day
        if isWin64() and not noWin64Byref:
            return byref(result)
        else:
            return result
    else:
        return date(year, month, day)


def isLinux64():
    """ Check to see if the current machine is
        a linux 64-bit platform. On Python versions 3.3
        and newer, this returns False.
    """
    return (platform == 'linux2' and (platform_info.machine().find("64") > 0))


def isWin64():
    """ Check to see if the current machine is
        a Windows 64-bit platform
    """
    return (platform == 'win32' and (platform_info.machine().find("64") > 0))


def isMkl():
    """ Checks for IMSL_MKL environment variable.
            Returns true if the variable is set
    """
    usemkl = imslRefs.imsl_mkl
    if usemkl is not None:
        usemkl = usemkl.strip()
        if (usemkl == '1') or (usemkl.lower() == 'true'):
            return True
    return False


def getShape(var):
    """ Return the shape of an array, list, or tuple.
            Note that we assume that the data structure is
            rectangular.  Odd-shaped data structures may not work properly.
            This routine tries to be as efficient as possible at
            obtaining shape information.  len() is more efficient
            than numpy.shape() for lists or tuples (iterables).
    """
    if isinstance(var, ndarray):
        return numpyShape(var)
    elif (isinstance(var, list)) or (isinstance(var, tuple)):
        tshape = []
        while (isinstance(var, list) or (isinstance(var, tuple))):
            tshape.append(len(var))
            var = var[0]
        return tshape
    else:
        return numpyShape(var)
