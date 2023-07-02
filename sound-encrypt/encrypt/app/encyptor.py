import wave
import struct
import numpy as np
from app.utils import CHAR_TO_BINARY,  DIGIT_TO_BINARY, Condition

class Encryptor:

    __slots__ = ('_rate', '_freq', '_condition')

    def __init__(self) -> None:
        self._rate = 8000
        self._freq = 1000
        self._condition = Condition.CHAR

    def _sine_samples(self, dur, freq = None):
        if freq is None:
            freq = self._freq
        X = (2*np.pi*freq/self._rate) * np.arange(self._rate*dur)
        S = (32767*np.sin(X)).astype(int)
        as_packed_bytes = b''.join(map(lambda v: struct.pack('h', v), S))
        return as_packed_bytes

    def _binary_to_wave(self, binary_character: str) -> bytes:
        frames = b''
        for digit in binary_character:
            dur = 0.1 if digit == '1' else 0.3
            frames += self._sine_samples(dur)
            frames += self._sine_samples(0.1,0)
        return frames

    def output_wave(self, path, frames):
        with wave.open(path, 'w') as output:
            output.setparams((1,2,self._rate,0,'NONE','not compressed'))
            output.writeframes(frames)

    def encrypt(self, text: str) -> str:
        frames = b''
        for c in text.lower():
            if self._condition == Condition.CHAR:
                if c == ' ':
                    frames += self._sine_samples(0.3, 0)
                elif c in CHAR_TO_BINARY:
                    frames += self._binary_to_wave(CHAR_TO_BINARY[c])
                elif c.isdigit():
                    frames += self._binary_to_wave(CHAR_TO_BINARY[''])
                    frames += self._binary_to_wave(DIGIT_TO_BINARY[c])
                    self._condition = Condition.DIGIT
                    continue
                else:
                    self._condition = Condition.ERROR
                    continue
            elif self._condition == Condition.DIGIT:
                if c == ' ':
                    frames += self._sine_samples(0.3, 0)
                    self._condition = Condition.CHAR
                elif c in DIGIT_TO_BINARY:
                    frames += self._binary_to_wave(DIGIT_TO_BINARY[c])
                else:
                    self._condition = Condition.ERROR
                    continue
            else:
                self._condition = Condition.CHAR
                raise UnidentifiedChar
                
        self.output_wave('морзе.wav', frames)

class UnidentifiedChar(Exception):
    def __init__(self) -> None:
        super().__init__("Обнаружен нераспознанный символ")