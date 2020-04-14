import numpy as np
import pyaudio

from dejavu.base_classes.base_recognizer import BaseRecognizer


class GrpcRecognizer(BaseRecognizer):
    default_chunksize = 8192
    default_format = pyaudio.paInt16
    default_channels = 2
    default_samplerate = 44100

    def __init__(self, dejavu):
        super().__init__(dejavu)
        self.stream = None
        self.data = []
        self.channels = GrpcRecognizer.default_channels
        self.chunksize = GrpcRecognizer.default_chunksize
        self.samplerate = GrpcRecognizer.default_samplerate

    def recognize(self, stream_data):
        self.data = [[] for i in range(self.channels)]
        for i in stream_data:
            nums = np.fromstring(i, np.int16)
            for c in range(self.channels):
                self.data[c].extend(nums[c::self.channels])

        return self._recognize(*self.data)

    @staticmethod
    def play_audio(stream_data):
        p = pyaudio.PyAudio()
        format = pyaudio.paInt16
        channels = 2
        rate = 44100
        buf_size = 5376

        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=False,
                        output=True,
                        frames_per_buffer=buf_size)

        for i in stream_data:
            stream.write(i)
