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

"""Module for OKEx address computation."""

# Imports
from typing import Any, Union
from bip_utils.addr.iaddr_decoder import IAddrDecoder
from bip_utils.addr.iaddr_encoder import IAddrEncoder
from bip_utils.addr.eth_addr import EthAddr
from bip_utils.bech32 import Bech32ChecksumError, Bech32FormatError, Bech32Decoder, Bech32Encoder
from bip_utils.coin_conf import CoinsConf
from bip_utils.ecc import IPublicKey
from bip_utils.utils.misc import ConvUtils


class OkexAddr(IAddrDecoder, IAddrEncoder):
    """
    OKEx Chain address class.
    It allows the OKEx Chain address encoding/decoding.
    """

    @staticmethod
    def DecodeAddr(addr: str,
                   **kwargs: Any) -> bytes:
        """
        Decode a OKEx Chain address to bytes.

        Args:
            addr (str): Address string
            **kwargs  : Not used

        Returns:
            bytes: Public key hash bytes

        Raises:
            ValueError: If the address encoding is not valid
        """
        try:
            addr_dec_bytes = Bech32Decoder.Decode(CoinsConf.OkexChain.Params("addr_hrp"),
                                                  addr)
        except (Bech32ChecksumError, Bech32FormatError) as ex:
            raise ValueError("Invalid Bech32 encoding") from ex
        else:
            return EthAddr.DecodeAddr(
                CoinsConf.Ethereum.Params("addr_prefix") + ConvUtils.BytesToHexString(addr_dec_bytes),
                skip_chksum_enc=True
            )

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, IPublicKey],
                  **kwargs: Any) -> str:
        """
        Encode a public key to OKEx Chain address.

        Args:
            pub_key (bytes or IPublicKey): Public key bytes or object
            **kwargs                     : Not used

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not secp256k1
        """

        # Get address in Ethereum format (remove "0x" at the beginning)
        eth_addr = EthAddr.EncodeKey(pub_key)[2:]
        # Encode in Bech32 format
        return Bech32Encoder.Encode(CoinsConf.OkexChain.Params("addr_hrp"),
                                    ConvUtils.HexStringToBytes(eth_addr))
