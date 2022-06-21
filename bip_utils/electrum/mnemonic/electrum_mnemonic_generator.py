# Copyright (c) 2022 Emanuele Bellocchia
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

"""Module for Electrum mnemonic generation."""

# Imports
from typing import Dict, Union
from bip_utils.electrum.mnemonic.electrum_entropy_generator import ElectrumEntropyBitLen, ElectrumEntropyGenerator
from bip_utils.electrum.mnemonic.electrum_mnemonic import (
    ElectrumMnemonicConst, ElectrumLanguages, ElectrumMnemonicTypes, ElectrumWordsNum
)
from bip_utils.electrum.mnemonic.electrum_mnemonic_encoder import ElectrumMnemonicEncoder
from bip_utils.utils.misc import BytesUtils, IntegerUtils
from bip_utils.utils.mnemonic import Mnemonic


class ElectrumMnemonicGeneratorConst:
    """Class container for Electrum mnemonic generator constants."""

    # Entropy length for each words number
    WORDS_NUM_TO_ENTROPY_LEN: Dict[ElectrumWordsNum, ElectrumEntropyBitLen] = {
        ElectrumWordsNum.WORDS_NUM_12: ElectrumEntropyBitLen.BIT_LEN_132,
    }
    # Maximum number of attempts (just to avoid infinite looping)
    MAX_ATTEMPTS: int = 100000


class ElectrumMnemonicGenerator:
    """
    Electrum mnemonic generator class.
    It generates 25-words mnemonic in according to Electrum wallets.
    """

    m_mnemonic_encoder: ElectrumMnemonicEncoder

    def __init__(self,
                 mnemonic_type: ElectrumMnemonicTypes,
                 lang: ElectrumLanguages = ElectrumLanguages.ENGLISH) -> None:
        """
        Construct class.

        Args:
            mnemonic_type (ElectrumMnemonicTypes): Mnemonic type
            lang (ElectrumLanguages, optional)   : Language (default: English)

        Raises:
            TypeError: If the language is not a ElectrumLanguages enum
            ValueError: If language words list is not valid
        """
        self.m_mnemonic_encoder = ElectrumMnemonicEncoder(mnemonic_type, lang)

    def FromWordsNumber(self,
                        words_num: Union[int, ElectrumWordsNum]) -> Mnemonic:
        """
        Generate mnemonic with the specified words number and type from random entropy.

        Args:
            words_num (int or ElectrumWordsNum)  : Number of words (12)

        Returns:
            Mnemonic object: Generated mnemonic

        Raises:
            ValueError: If words number is not valid
        """

        # Check words number
        if words_num not in ElectrumMnemonicConst.MNEMONIC_WORD_NUM:
            raise ValueError(f"Words number for mnemonic ({words_num}) is not valid")

        # Convert int to enum if necessary
        if isinstance(words_num, int):
            words_num = ElectrumWordsNum(words_num)

        # Get entropy length in bit from words number
        entropy_bit_len = ElectrumMnemonicGeneratorConst.WORDS_NUM_TO_ENTROPY_LEN[words_num]
        # Generate entropy
        entropy_bytes = ElectrumEntropyGenerator(entropy_bit_len).Generate()

        return self.FromEntropy(entropy_bytes)

    def FromEntropy(self,
                    entropy_bytes: bytes) -> Mnemonic:
        """
        Generate mnemonic from the specified entropy bytes.

        Args:
            entropy_bytes (bytes): Entropy bytes

        Returns:
            Mnemonic object: Generated mnemonic

        Raises:
            ValueError: If entropy byte length is not valid
        """
        entropy_int = BytesUtils.ToInteger(entropy_bytes)
        nonce = 0

        # Increase the entropy until a valid one is found
        for i in range(ElectrumMnemonicGeneratorConst.MAX_ATTEMPTS):
            nonce += 1
            new_entropy_int = entropy_int + nonce
            try:
                return self.m_mnemonic_encoder.Encode(IntegerUtils.ToBytes(new_entropy_int))
            except ValueError:
                continue

        raise ValueError("Unable to generate a valid mnemonic")
