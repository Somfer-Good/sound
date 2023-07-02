import wave
import base64
import numpy as np
from app.utils import Condition, BINARY_DIGIT_TO_CHAR, BINARY_TO_CHAR

class Decryptor:

    __slots__ = ('_rate', '_freq', '_condition')

    def __init__(self) -> None:
        self._rate = 8000
        self._freq = 1000
        self._condition = Condition.START_STATE

    def _wav_to_binary(self) -> list:
        binary_code = []
        i = 0
        buffer = ""
        with wave.open('морзе.wav', 'rb') as f:
            frame_set = f.readframes(f.getnframes())
            while i < len(frame_set):
                if self._condition == Condition.SKIP:
                    i += 1600
                    self._condition = Condition.START_STATE
                    continue
                frame_slice = frame_set[i:i+1600]
                if all(x == 0 for x in frame_slice):
                    if self._condition == Condition.WHITE_SPACE:
                        binary_code.append(buffer)
                        buffer = ""
                        binary_code.append(' ')
                        self._condition = Condition.SKIP
                    elif self._condition == Condition.BIT:
                        buffer += '1'
                        self._condition = Condition.WHITE_SPACE
                    else:
                        self._condition = Condition.WHITE_SPACE
                else:
                    if self._condition == Condition.BIT:
                        buffer += '0'
                        self._condition = Condition.SKIP
                    else:
                        self._condition = Condition.BIT
                
                i += 1600
        if buffer:
            binary_code.append(buffer)

        return binary_code

    def _b64_to_wav(self, b64_wav):
        with open('морзе.wav', 'wb') as f:
            f.write(base64.b64decode(b64_wav))

    def decrypt(self, b64_wav) -> str:
        self._b64_to_wav(b64_wav)
        result_text = ''
        for word in self._wav_to_binary():
            is_digit = False
            if word == ' ':
                result_text += word
            else:
                i = 0
                buffer = ''
                while i < len(word):
                    binary_word = word[i:i+6]
                    if binary_word == '001111':
                        is_digit = True
                        i += 6
                        continue
                    buffer += BINARY_DIGIT_TO_CHAR[binary_word] if is_digit else BINARY_TO_CHAR[binary_word]
                    i += 6
            result_text += buffer
            buffer = ''

        return result_text


class UnidentifiedChar(Exception):
    def __init__(self) -> None:
        super().__init__("Обнаружен нераспознанный символ")