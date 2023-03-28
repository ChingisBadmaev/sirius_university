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
from numpy import *
from pyimsl.stat.empiricalQuantiles import empiricalQuantiles

x = array([
    0.77, 1.74, 0.81, 1.20, 1.95,
    1.20, 0.47, 1.43, 3.37, 2.20,
    3.00, 3.09, 1.51, 2.10, 0.52,
    1.62, 1.31, 0.32, 0.59, 0.81,
    2.81, 1.87, 1.18, 1.35, 4.75,
    2.48, 0.96, 1.89, 0.90, 2.05])

qprop = [0.01, 0.5, 0.9, 0.95, 0.99]

p_xlo = []
p_xhi = []

p_q = empiricalQuantiles(x, qprop,
                         xlo=p_xlo,
                         xhi=p_xhi)

print("          Smaller  Empirical  Larger")
print("Quantile   Datum    Quantile   Datum")
for i in range(0, 5):
    print("  %4.2f   %7.2f   %7.2f   %7.2f\n" %
          (qprop[i], p_xlo[i], p_q[i], p_xhi[i]))
