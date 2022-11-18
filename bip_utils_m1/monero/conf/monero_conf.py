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

"""Module for Monero coins configuration."""

# Imports
from bip_utils_m1.coin_conf import CoinsConf
from bip_utils_m1.monero.conf.monero_coin_conf import MoneroCoinConf


class MoneroConf:
    """Class container for Monero configuration."""

    # Configuration for Monero main net
    MainNet: MoneroCoinConf = MoneroCoinConf.FromCoinConf(CoinsConf.MoneroMainNet)

    # Configuration for Monero stage net
    StageNet: MoneroCoinConf = MoneroCoinConf.FromCoinConf(CoinsConf.MoneroStageNet)

    # Configuration for Monero test net
    TestNet: MoneroCoinConf = MoneroCoinConf.FromCoinConf(CoinsConf.MoneroTestNet)