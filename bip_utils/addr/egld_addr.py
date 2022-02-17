
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

"""Module for Elrond address computation."""

# Imports
from typing import Any, Union
from bip_utils.addr.addr_key_validator import AddrKeyValidator
from bip_utils.addr.iaddr_decoder import IAddrDecoder
from bip_utils.addr.iaddr_encoder import IAddrEncoder
from bip_utils.bech32 import Bech32ChecksumError, Bech32FormatError, Bech32Decoder, Bech32Encoder
from bip_utils.coin_conf import CoinsConf
from bip_utils.ecc import Ed25519PublicKey, IPublicKey
from bip_utils.utils.misc import ConvUtils


class EgldAddrConst:
    """Class container for Elrond address constants."""

    # Decoded length in bytes
    DEC_BYTE_LEN: int = 32


class EgldAddr(IAddrDecoder, IAddrEncoder):
    """
    Elrond address class.
    It allows the Elrond address encoding/decoding.
    """

    @staticmethod
    def DecodeAddr(addr: str,
                   **kwargs: Any) -> bytes:
        """
        Decode an Elrond address to bytes.

        Args:
            addr (str): Address string
            **kwargs  : Not used

        Returns:
            bytes: Public key bytes

        Raises:
            ValueError: If the address encoding is not valid
        """
        try:
            addr_dec = Bech32Decoder.Decode(CoinsConf.Elrond.Params("addr_hrp"),
                                            addr)
        except (Bech32ChecksumError, Bech32FormatError) as ex:
            raise ValueError("Invalid Bech32 encoding") from ex
        else:
            # Check length
            if len(addr_dec) != EgldAddrConst.DEC_BYTE_LEN:
                raise ValueError(f"Invalid decoded length {len(addr_dec)}")
            # Check public key
            if not Ed25519PublicKey.IsValidBytes(addr_dec):
                raise ValueError(f"Invalid public key {ConvUtils.BytesToHexString(addr_dec)}")

            return addr_dec

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, IPublicKey],
                  **kwargs: Any) -> str:
        """
        Encode a public key to Elrond address.

        Args:
            pub_key (bytes or IPublicKey): Public key bytes or object
            **kwargs                     : Not used

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not ed25519
        """
        pub_key_obj = AddrKeyValidator.ValidateAndGetEd25519Key(pub_key)

        return Bech32Encoder.Encode(CoinsConf.Elrond.Params("addr_hrp"),
                                    pub_key_obj.RawCompressed().ToBytes()[1:])
