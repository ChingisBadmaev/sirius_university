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
import os
import sys

from collections import deque
from ctypes import c_void_p, c_int, c_double, c_char_p, CFUNCTYPE
from pyimsl.util import imslRefs
from pyimsl.util.ImslError import ImslError
from pyimsl.util.Translator import Translator

IMSL_SET_STOP = 10190
IMSL_SET_SIGNAL_TRAPPING = 50012
IMSL_WARNING = 3
IMSL_FATAL = 4
IMSL_TERMINAL = 5
IMSL_WARNING_IMMEDIATE = 6
IMSL_FATAL_IMMEDIATE = 7
IMSL_ERROR_MSG_PATH = 10196
IMSL_ERROR_MSG_NAME = 10197
IMSL_ERROR_PRINT_PROC = 10195   # from pyimsl.h


IMSLS_SET_STOP = 14530
IMSLS_SET_SIGNAL_TRAPPING = 16042
IMSLS_WARNING = 3
IMSLS_FATAL = 4
IMSLS_TERMINAL = 5
IMSLS_WARNING_IMMEDIATE = 6
IMSLS_FATAL_IMMEDIATE = 7
IMSLS_ERROR_MSG_NAME = 11400
IMSLS_ERROR_MSG_PATH = 11410
IMSLS_ERROR_PRINT_PROC = 11420   # from imsls.h

_imslErrorType = None
_imslErrorCode = None
_imslErrorMessage = None
_imslErrorStack = deque()   # All errors are pushed on the stack (deque)
#
# The ImslErrorHandler class is responsible for handling errors
# that occur during code execution.
# It provides methods for obtaining the current error type, code, and
# message string.
# These (static) methods are:
#     getErrorCode()
#     getErrorType()
#     getErrorMessage()
#     getErrorStack()
#
# This class will be transparent to end-users until they need to
# handle an error or query the current error state.
#
# Note that there is one print procedure (_imslPrintProc) that is shared
# across all of the ImslErrorHandler instances.  This is because the
# printProc routine is being called directly from CNL.
# As a result, there is only one (global) instance of the current error message
# variables.
#


def _imslUtilsPrintProc(type, code, function_name, message):
    """ Set up the procedure that will be used to print CNL
        error messages.  This is to facilitate internationalization.
    """
    function_name = camel(function_name)
    if (type == 1):
        tmpStr = Translator.getString("IMSL_NOTE")
    elif (type == 2):
        tmpStr = Translator.getString("IMSL_ALERT")
    elif (type == 3):
        tmpStr = Translator.getString("IMSL_WARNING")
    elif (type == 4):
        tmpStr = Translator.getString("IMSL_FATAL")
    elif (type == 5):
        tmpStr = Translator.getString("IMSL_TERMINAL")
    elif (type == 6):
        tmpStr = Translator.getString("IMSL_WARNING_IMMEDIATE")
    elif (type == 7):
        tmpStr = Translator.getString("IMSL_FATAL_IMMEDIATE")
    else:
        tmpStr = Translator.getString("IMSL_NOTE")  # Shouldn't happen
    if (isinstance(tmpStr, bytes)):
        tmpStr = bytes.decode(tmpStr)
    if (isinstance(message, bytes)):
        message = bytes.decode(message)
    resultStr = "***\n"
    resultStr += "*** " + tmpStr + " error issued from IMSL function " + function_name
    resultStr += ":\n*** " + message + "\n***"
    global _imslErrorType, _imslErrorCode, _imslErrorMessage
    _imslErrorType = type
    _imslErrorCode = code
    _imslErrorMessage = message[:]   # Make sure to clone, to avoid bad ptr
    _imslErrorStack.append(
        ImslError(_imslErrorType, _imslErrorCode, _imslErrorMessage))
    print(resultStr)


def camel(name):
    """ Camelcase a function name
    """
    if (isinstance(name, bytes)):
        name = bytes.decode(name)
    name = name.lower()
    if name.startswith("imsl_d_"):
        name = name[7:]
    if name.startswith("imsls_d_"):
        name = name[8:]
    if name.startswith("imsl_"):
        name = name[5:]
    if name.startswith("imsls_"):
        name = name[6:]
    splits = name.split('_')
    camname = ''
    for tok in splits:
        if tok != '':
            if camname == '':
                camname = tok
            else:
                camname = camname + tok[0].upper() + tok[1:]
    return camname


class ImslErrorHandler (object):
    """ The ImslErrorHandler class is responsible for handling errors
        that occur during code execution.
        It provides methods for obtaining the current error type, code, and
        message string.
    """

    def __init__(self, isMathHandler):
        self._imslPrintProc = None
        self._isMathHandler = isMathHandler
        _printProcDef = CFUNCTYPE(c_void_p, c_int, c_int, c_char_p, c_char_p)
        if isMathHandler:
            self._imslPrintProc = _printProcDef(_imslUtilsPrintProc)
            imslRefs.imslmath.imsl_error_options.restype = None
            imslRefs.imslmath.imsl_error_options(
                IMSL_ERROR_PRINT_PROC, self._imslPrintProc, 0)
            self._setErrorOptions(True)

        else:
            self._imslPrintProc = _printProcDef(_imslUtilsPrintProc)
            imslRefs.imslstat.imsls_error_options.restype = None
            imslRefs.imslstat.imsls_error_options(
                IMSLS_ERROR_PRINT_PROC, self._imslPrintProc, 0)
            self._setErrorOptions(False)

    def _setErrorOptions(self, isMathHandler):
        """ Set the options for error handling.
        """
        translationDir = Translator.getTranslationDir()
        if (isMathHandler):
            imslRefs.imslmath.imsl_error_options(IMSL_SET_SIGNAL_TRAPPING, 0,
                                                 IMSL_SET_STOP, IMSL_WARNING, 0,
                                                 IMSL_SET_STOP, IMSL_FATAL, 0,
                                                 IMSL_SET_STOP, IMSL_TERMINAL, 0,
                                                 IMSL_SET_STOP, IMSL_FATAL_IMMEDIATE, 0,
                                                 IMSL_SET_STOP, IMSL_WARNING_IMMEDIATE, 0,
                                                 0)
            if translationDir is not None:
                errorMsgFile = translationDir + os.sep + "imslerr.bin"
                if (sys.platform == 'win32'):
                    errorMsgFile = errorMsgFile.replace(os.sep, "/")
                if (not(os.path.exists(errorMsgFile))):
                    raise IOError(
                        "Could not open error message file: " + errorMsgFile)
                else:
                    errorPath = translationDir + os.sep
                    imslRefs.imslmath.imsl_error_options(
                        IMSL_ERROR_MSG_PATH, str.encode(errorPath), 0)
        else:
            imslRefs.imslstat.imsls_error_options(IMSLS_SET_SIGNAL_TRAPPING, 0,
                                                  IMSLS_SET_STOP, IMSLS_WARNING, 0,
                                                  IMSLS_SET_STOP, IMSLS_FATAL, 0,
                                                  IMSLS_SET_STOP, IMSLS_TERMINAL, 0,
                                                  IMSLS_SET_STOP, IMSLS_FATAL_IMMEDIATE, 0,
                                                  IMSLS_SET_STOP, IMSLS_WARNING_IMMEDIATE, 0,
                                                  0)
            if translationDir is not None:
                errorMsgFile = translationDir + os.sep + "imsls_e.bin"
                if (sys.platform == 'win32'):
                    errorMsgFile = errorMsgFile.replace(os.sep, "/")
                if (not(os.path.exists(errorMsgFile))):
                    raise IOError(
                        "Could not open error message file: " + errorMsgFile)
                else:
                    errorPath = translationDir + os.sep
                    imslRefs.imslstat.imsls_error_options(
                        IMSLS_ERROR_MSG_PATH, str.encode(errorPath), 0)

#       print "Error messages obtained from: ", errorMsgFile

    def getErrorCode():
        """ This method returns the error code for the most recent error.
            Error codes are defined in pyimsl.math.errorCodes.py and
            pyimsl.stat.errorCodes.py.
        """
        global _imslErrorCode
        return _imslErrorCode
    getErrorCode = staticmethod(getErrorCode)

    def getErrorType():
        """ This method returns the error type for the most recent error.
            Error types are defined in imslUtils.py.  Types are an
            integer between 3 and 7, where 3 is IMSL_WARNING, and
            7 is IMSL_FATAL_IMMEDIATE.
        """
        global _imslErrorType
        return _imslErrorType
    getErrorType = staticmethod(getErrorType)

    def getErrorMessage():
        """ This method returns the error message string for the
            most recent error.
        """
        global _imslErrorMessage
        if _imslErrorMessage is None:
            return None
        else:
            return _imslErrorMessage[:]
    getErrorMessage = staticmethod(getErrorMessage)

    def getErrorStack():
        """ This method returns the current stack (deque), which
            contains all errors that have been encountered to this point.
        """
        global _imslErrorStack
        return _imslErrorStack
    getErrorStack = staticmethod(getErrorStack)

    def clear():
        """ This method clears the current stack
        """
        global _imslErrorStack
        global _imslErrorMessage
        global _imslErrorCode
        global _imslErrorType
        _imslErrorStack.clear()
        _imslErrorMessage = None
        _imslErrorCode = None
        _imslErrorType = None
    clear = staticmethod(clear)

    def handleError(self):
        global _imslErrorType, _imslErrorCode, _imslErrorMessage
        if (self._isMathHandler):
            severity = imslRefs.imslmath.imsl_n1rty(1)
            if (severity == IMSL_FATAL) or \
               (severity == IMSL_TERMINAL) or \
               (severity == IMSL_FATAL_IMMEDIATE):
                raise ImslError(_imslErrorType, _imslErrorCode,
                                _imslErrorMessage)
#                raise ImslError (self._imslErrorType, self._imslErrorCode, self._imslErrorMessage)
        else:
            severity = imslRefs.imslstat.imsls_n1rty(1)
            if (severity == IMSLS_FATAL) or \
               (severity == IMSLS_TERMINAL) or \
               (severity == IMSLS_FATAL_IMMEDIATE):
                raise ImslError(_imslErrorType, _imslErrorCode,
                                _imslErrorMessage)
#                raise ImslError (self._imslErrorType, self._imslErrorCode, self._imslErrorMessage)
