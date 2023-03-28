###########################################################################
# Copyright 2014-2019 Rogue Wave Software, Inc.
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
import pyimsl.math.version
import pyimsl.stat.version

try:
    mathver = pyimsl.math.version.version(pyimsl.math.version.LIBRARY_VERSION)
    print(mathver)
    statver = pyimsl.stat.version.version(pyimsl.stat.version.LIBRARY_VERSION)
    print(statver)
    print("PyIMSL math/stat libraries were installed properly")
except Exception:
    print("There was a problem with the PyIMSL install.")
