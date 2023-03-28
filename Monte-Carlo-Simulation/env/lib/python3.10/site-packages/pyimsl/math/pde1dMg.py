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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, checkForDict, processRet
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, ndarray, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
from pyimsl.math.pde1dMgState import pde1dMgState
from pyimsl.util.Translator import Translator

IMSL_RELATIVE_TOLERANCE = 14041
IMSL_ABSOLUTE_TOLERANCE = 14042
IMSL_PDE_SYS_W_DATA = 14043
IMSL_BOUNDARY_COND_W_DATA = 14044
imslmath = loadimsl(MATH)


def pde1dMg(t, tend, u, xl, xr, state, pdeSystems, boundaryConditions, relativeTolerance=None, absoluteTolerance=None, pdeSysWData=None, boundaryCondWData=None):
    """ Solves a system of one-dimensional time-dependent partial differential equations using a moving-grid interface.
    """
    VersionFacade.checkVersion(6)
    if (state[0] is None) or (state[0].state is None):
        errStr = Translator.getString("pde1dnotavailable")
        raise ValueError(errStr)
    if (not(isinstance(state[0], pde1dMgState))):
        errStr = Translator.getString("statecorrupt")
        raise ValueError(errStr)
    imslmath.imsl_d_pde_1d_mg.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_pde_1d_mg('
    evalstring += 'c_int(npdes)'
    evalstring += ','
    evalstring += 'c_int(ngrids)'
    evalstring += ','
    state[0]._setT(t[0])
    t_tmp = state[0]._getTObject()
    #    t_tmp=t[0]
    #    if (not(isinstance(t_tmp, c_double))):
    #        t_tmp=c_double(t[0])
    evalstring += 'byref(t_tmp)'
    evalstring += ','
    evalstring += 'c_double(tend)'
    evalstring += ','
    evalstring += 'u_tmp.ctypes.data_as(c_void_p)'
    u_tmp = u
    if (not(isinstance(u_tmp, ndarray))):
        u_tmp = toNumpyArray(u, 'u', shape=shape,
                             dtype='double', expectedShape=(0, 0))
    #    u_tmp = toNumpyArray(u, 'u', shape=shape, dtype='double', expectedShape=(0,0))
    npdes = len(u_tmp) - 1
    ngrids = len(u_tmp[0])
    state[0]._setU(u_tmp, npdes + 1, ngrids)
    u_tmp = state[0]._getUObject()
    evalstring += ','
    evalstring += 'c_double(xl)'
    evalstring += ','
    evalstring += 'c_double(xr)'
    evalstring += ','
    evalstring += 'state[0].state'
    evalstring += ','
    checkForCallable(pdeSystems, 'pdeSystems')
    TMP_PDESYSTEMS = CFUNCTYPE(c_void_p, c_double, c_double, c_int, c_int, POINTER(c_double), POINTER(
        c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_int))
    tmp_pdeSystems = TMP_PDESYSTEMS(pdeSystems)
    evalstring += 'tmp_pdeSystems'
    evalstring += ','
    state.append(pdeSystems)
    state.append(tmp_pdeSystems)
    checkForCallable(boundaryConditions, 'boundaryConditions')
    TMP_BOUNDARYCONDITIONS = CFUNCTYPE(c_void_p, c_double, POINTER(c_double), POINTER(c_double), POINTER(
        c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, POINTER(c_int))
    tmp_boundaryConditions = TMP_BOUNDARYCONDITIONS(boundaryConditions)
    evalstring += 'tmp_boundaryConditions'
    state.append(boundaryConditions)
    state.append(tmp_boundaryConditions)
    if not (relativeTolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_RELATIVE_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(relativeTolerance)'
    if not (absoluteTolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_ABSOLUTE_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(absoluteTolerance)'
    if not (pdeSysWData is None):
        evalstring += ','
        evalstring += repr(IMSL_PDE_SYS_W_DATA)
        checkForDict(pdeSysWData, 'pdeSysWData', ['pdeSysWData', 'data'])
        evalstring += ','
        tmp_pdeSysWData_pdeSysWData_param = pdeSysWData['pdeSysWData']
        checkForCallable(tmp_pdeSysWData_pdeSysWData_param, 'pdeSysWData')
        TMP_PDESYSWDATA_PDESYSWDATA = CFUNCTYPE(c_void_p, c_double, c_double, c_int, c_int, POINTER(c_double), POINTER(
            c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_double))
        tmp_pdeSysWData_pdeSysWData = TMP_PDESYSWDATA_PDESYSWDATA(
            tmp_pdeSysWData_pdeSysWData_param)
        evalstring += 'tmp_pdeSysWData_pdeSysWData'
        evalstring += ','
        pdeSysWData_data_tmp = pdeSysWData['data']
        pdeSysWData_data_tmp = toNumpyArray(
            pdeSysWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'pdeSysWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (boundaryCondWData is None):
        evalstring += ','
        evalstring += repr(IMSL_BOUNDARY_COND_W_DATA)
        checkForDict(boundaryCondWData, 'boundaryCondWData',
                     ['boundaryCondWData', 'data'])
        evalstring += ','
        tmp_boundaryCondWData_boundaryCondWData_param = boundaryCondWData['boundaryCondWData']
        checkForCallable(
            tmp_boundaryCondWData_boundaryCondWData_param, 'boundaryCondWData')
        TMP_BOUNDARYCONDWDATA_BOUNDARYCONDWDATA = CFUNCTYPE(c_void_p, c_double, POINTER(c_double), POINTER(c_double), POINTER(
            c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, POINTER(c_int), POINTER(c_double))
        tmp_boundaryCondWData_boundaryCondWData = TMP_BOUNDARYCONDWDATA_BOUNDARYCONDWDATA(
            tmp_boundaryCondWData_boundaryCondWData_param)
        evalstring += 'tmp_boundaryCondWData_boundaryCondWData'
        evalstring += ','
        boundaryCondWData_data_tmp = boundaryCondWData['data']
        boundaryCondWData_data_tmp = toNumpyArray(
            boundaryCondWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'boundaryCondWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(t_tmp, inout=True, shape=(1), pyvar=t)
    processRet(u_tmp, inout=True, shape=(npdes + 1, ngrids), pyvar=u)
    return
