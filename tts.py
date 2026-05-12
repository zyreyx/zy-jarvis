from piper import PiperVoice
import numpy 
import sounddevice as sd
sd.default.device = "pipewire"
model = PiperVoice.load("voices/alan-medium.onnx")

def tts(text):
    with sd.OutputStream(samplerate=22050, channels=1, dtype='int16') as stream:
        for chunk in model.synthesize(text):
            buffer = chunk.audio_int16_array
            # buffer = numpy.frombuffer(chunk, dtype='int16')
            # 
            resampled = numpy.interp(
            #     numpy.linspace(0, len(buffer), int(len(buffer) * 48000 / 22050)),
            #     numpy.arange(len(buffer)),
            #     buffer
            # ).astype(numpy.int16)
            # stream.write(resampled)
            stream.write(buffer)
        

    
