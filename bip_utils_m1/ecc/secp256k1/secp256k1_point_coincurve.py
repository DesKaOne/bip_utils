# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Module for secp256k1 point based on coincurve library."""

# Imports
from typing import Any

from bip_utils_m1.ecc.common.ipoint import IPoint
from bip_utils_m1.ecc.curve.elliptic_curve_types import EllipticCurveTypes
from bip_utils_m1.ecc.ecdsa.ecdsa_keys import EcdsaKeysConst
from bip_utils_m1.utils.misc import DataBytes, IntegerUtils


class Secp256k1PointCoincurve(IPoint):
    """
    Secp256k1 point class.
    In coincurve library, all the point functions (e.g. add, multiply) are coded inside the
    PublicKey class. For this reason, a PublicKey is used as underlying object.
    """

    def __init__(self) -> None:
        super().__init__()