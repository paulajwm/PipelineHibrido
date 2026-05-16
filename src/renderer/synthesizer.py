import os
import numpy as np
import pretty_midi
import soundfile as sf
from pathlib import Path

class AudioRenderer:
    """
    Motor de renderizado MIDI a WAV.
    Genera versiones RAW y Normalizada para análisis técnico.
    """

    def __init__(self, soundfont_path):
        self.sample_rate = 44100
        self.sf2_path = str(soundfont_path)
        if not Path(self.sf2_path).is_file():
            raise FileNotFoundError(f"SoundFont no encontrada: {self.sf2_path}")

    def render(self, midi_path, output_wav):
        """
        Sintetiza y procesa el audio aplicando normalización de picos.
        """
        # 1. Síntesis mediante FluidSynth
        midi_data = pretty_midi.PrettyMIDI(str(midi_path))
        audio = midi_data.fluidsynth(fs=self.sample_rate, sf2_path=self.sf2_path)
        audio = np.asarray(audio, dtype=np.float32)

        # 2. Exportación RAW (sin procesar)
        ruta_raw = output_wav.replace(".wav", "_RAW.wav")
        sf.write(ruta_raw, audio, self.sample_rate)
        print(f"[Render] Audio crudo guardado: {os.path.basename(ruta_raw)}")

        # 3. Normalización (Maximización de rango dinámico)
        peak = np.max(np.abs(audio)) if audio.size > 0 else 0.0
        if peak > 0:
            # Escalado al límite de seguridad -0.5 dB
            audio = (audio / peak) * 0.95
            print(f"[Render] Normalización: Pico {peak:.3f} -> 0.950")

        # 4. Exportación Final
        sf.write(output_wav, audio, self.sample_rate)
        print(f"[Render] Audio final exportado: {os.path.basename(output_wav)}")