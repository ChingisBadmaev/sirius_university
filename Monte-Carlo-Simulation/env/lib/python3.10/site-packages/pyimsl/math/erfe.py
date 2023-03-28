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
from pyimsl.util.imslUtils import MATH, complexConvert, d_complex, fatalErrorCheck, loadimsl
from numpy import shape

from .mathStructs import d_complex
from .mathStructs import d_complex

imslmath = loadimsl(MATH)


def erfe(z):
    """ Evaluates a scaled function related to erfc(z).
    """
    imslmath.imsl_z_erfe.restype = d_complex
    shape = []
    evalstring = 'imslmath.imsl_z_erfe('
    evalstring += 'z'
    evalstring += ')'
    z = complexConvert(z, toDComplex=True)
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    cmplx = complexConvert(result)
    return cmplx
