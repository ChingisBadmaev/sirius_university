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
from pyimsl.util.imslUtils import STAT, processRet, checkForDict, checkForCallable, checkForList, checkForStr, fatalErrorCheck, loadimsl
from pyimsl.util.ImslErrorHandler import IMSLS_SET_SIGNAL_TRAPPING, IMSLS_SET_STOP
from pyimsl.util.Translator import Translator
from numpy import shape, size
from ctypes import CFUNCTYPE, byref, c_char_p, c_int, c_void_p

# Legal values for error type for setPrint, setStop, setTraceback, getPrint, getStop, and getTraceback:
NOTE = 1
ALERT = 2
WARNING = 3
FATAL = 4
TERMINAL = 5
WARNING_IMMEDIATE = 6
FATAL_IMMEDIATE = 7

IMSLS_SET_PRINT = 14520
IMSLS_SET_STOP = 14530
IMSLS_SET_TRACEBACK = 14540
IMSLS_FULL_TRACEBACK = 11850
IMSLS_GET_PRINT = 11990
IMSLS_GET_STOP = 12000
IMSLS_GET_TRACEBACK = 12010
IMSLS_SET_ERROR_FILE = 14490
IMSLS_GET_ERROR_FILE = 11970
IMSLS_ERROR_MSG_PATH = 11410
IMSLS_ERROR_MSG_NAME = 11400
IMSLS_ERROR_PRINT_PROC = 11420
IMSLS_SET_SIGNAL_TRAPPING = 16042
imslstat = loadimsl(STAT)
first = True
evalstring = ''


def errorOptions(setPrint=None, setStop=None, setTraceback=None, fullTraceback=None, getPrint=None, getStop=None, getTraceback=None, setErrorFile=None, getErrorFile=None, errorMsgPath=None, errorMsgName=None, errorPrintProc=None, setSignalTrapping=None):
    #
    # errorOptions allows access to a number of functions that
    # conflict with behaviors we have overridden globally for
    # the wrappers.
    # Specifically, overriding the outputPrintProc causes a crash.
    # For now, we'll just disable everything except setPrint.
    #
    def writeComma(evalString):
        if not evalstring.endswith('('):
            evalString = evalString + ','
        return evalString
    imslstat.imsls_error_options.restype = None
    shape = []
    evalstring = 'imslstat.imsls_error_options('
    if not (setPrint is None):
        evalstring = writeComma(evalstring)
        evalstring += repr(IMSLS_SET_PRINT)
        checkForDict(setPrint, 'setPrint', ['type', 'setting'])
        evalstring += ','
        setPrint_type_tmp = setPrint['type']
        evalstring += 'c_int(setPrint_type_tmp)'
        evalstring += ','
        setPrint_setting_tmp = setPrint['setting']
        evalstring += 'c_int(setPrint_setting_tmp)'
    else:
        errStr = Translator.getString("eoNotImplemented")
        raise NotImplementedError(errStr)
#    if not (setStop is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_SET_STOP`
#        checkForDict(setStop,'setStop',['type','setting'])
#        evalstring +=','
#        setStop_type_tmp = setStop['type']
#        evalstring +='c_int(setStop_type_tmp)'
#        evalstring +=','
#        setStop_setting_tmp = setStop['setting']
#        evalstring +='c_int(setStop_setting_tmp)'
#    if not (setTraceback is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_SET_TRACEBACK`
#        checkForDict(setTraceback,'setTraceback',['type','setting'])
#        evalstring +=','
#        setTraceback_type_tmp = setTraceback['type']
#        evalstring +='c_int(setTraceback_type_tmp)'
#        evalstring +=','
#        setTraceback_setting_tmp = setTraceback['setting']
#        evalstring +='c_int(setTraceback_setting_tmp)'
#    if not (fullTraceback is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_FULL_TRACEBACK`
#        evalstring +=','
#        evalstring +='c_int(fullTraceback)'
    if not (getPrint is None):
        evalstring = writeComma(evalstring)
        evalstring += repr(IMSLS_GET_PRINT)
        checkForDict(getPrint, 'getPrint', ['type', 'psetting'])
        evalstring += ','
        getPrint_type_tmp = getPrint['type']
        evalstring += 'c_int(getPrint_type_tmp)'
        evalstring += ','
        getPrint_psetting_tmp = c_int()
        evalstring += 'byref(getPrint_psetting_tmp)'
#    if not (getStop is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_GET_STOP`
#        checkForDict(getStop,'getStop',['type','psetting'])
#        evalstring +=','
#        getStop_type_tmp = getStop['type']
#        evalstring += 'c_int(getStop_type_tmp)'
#        evalstring +=','
#        getStop_psetting_tmp = c_int()
#        evalstring += 'byref(getStop_psetting_tmp)'
#    if not (getTraceback is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_GET_TRACEBACK`
#        checkForDict(getTraceback,'getTraceback',['type','psetting'])
#        evalstring +=','
#        getTraceback_type_tmp = getTraceback['type']
#        evalstring += 'c_int(getTraceback_type_tmp)'
#        evalstring +=','
#        getTraceback_psetting_tmp = c_int()
#        evalstring += 'byref(getTraceback_psetting_tmp)'
#    if not (setErrorFile is None):
#        writeComma()
#        evalstring +=`IMSL_SET_ERROR_FILE`
#        evalstring +=','
#        evalstring +='struct(setErrorFile)'
#        errStr = Translator.getString ("sefNotImplemented")
#        raise NotImplementedError, errStr
#    if not (getErrorFile is None):
#        writeComma()
#        evalstring +=`IMSL_GET_ERROR_FILE`
#        checkForList(getErrorFile,'getErrorFile')
#        evalstring +=','
#        getErrorFile_pfile_tmp = struct()
#        evalstring += 'byref(getErrorFile_pfile_tmp)'
#        errStr = Translator.getString ("gefNotImplemented")
#        raise NotImplementedError, errStr
#    if not (errorMsgPath is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_ERROR_MSG_PATH`
#        evalstring +=','
#        checkForStr (errorMsgPath,'errorMsgPath')
#        evalstring +='errorMsgPath'
#    if not (errorMsgName is None):
#        evalstring =writeComma()
#        evalstring +=`IMSLS_ERROR_MSG_NAME`
#        evalstring +=','
#        checkForStr (errorMsgName,'errorMsgName')
#        evalstring +='errorMsgName'
#    if not (errorPrintProc is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_ERROR_PRINT_PROC`
#        evalstring +=','
#        checkForCallable(errorPrintProc,'printProc')
#        TMP_ERRORPRINTPROC_PRINTPROC=CFUNCTYPE(c_void_p,c_int,c_int,c_char_p,c_char_p)
#        tmp_errorPrintProc_printProc=TMP_ERRORPRINTPROC_PRINTPROC(errorPrintProc)
#        _imslsPrintProc = tmp_errorPrintProc_printProc
#        evalstring += 'tmp_errorPrintProc_printProc'
#    if not (setSignalTrapping is None):
#        evalstring =writeComma(evalstring)
#        evalstring +=`IMSLS_SET_SIGNAL_TRAPPING`
#        evalstring +=','
#        evalstring +='c_int(setSignalTrapping)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (getPrint is None):
        processRet(getPrint_psetting_tmp, shape=(
            1), key='psetting', pyvar=getPrint)
#    if not (getStop is None):
#        processRet(getStop_psetting_tmp, shape=(1), key='psetting', pyvar=getStop)
#    if not (getTraceback is None):
#        processRet(getTraceback_psetting_tmp, shape=(1), key='psetting', pyvar=getTraceback)
#    if not (getErrorFile is None):
#        getErrorFile[:]=[]
#        getErrorFile.append(getErrorFile_pfile_tmp.value)
    return
