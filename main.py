import os

# Silenciar avisos de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import sys
import ctypes
import numpy as np

# --- CONFIGURACIÓN DE ENTORNO ---
ruta_actual = os.getcwd()
os.environ['PATH'] = ruta_actual + os.pathsep + os.environ.get('PATH', '')

try:
    ctypes.CDLL(os.path.join(ruta_actual, 'libfluidsynth.dll'))
except Exception as e:
    print(f"Aviso DLL: {e}")

try:
    from src.compositor.generator import MuseGANGenerator
    from src.compositor.groover import StyleTransfer
    # --- IMPORTACIÓN CORREGIDA A LA NUEVA RUTA ---
    from src.renderer.synthesizer import AudioRenderer
    import pretty_midi
except ImportError as e:
    print(f"Error de importación: {e}. Revisa las rutas de las carpetas.")
    sys.exit(1)

# --- CONSTANTES ---
CHECKPOINT_MUSEGAN = r"models\checkpoints\musegan_hybrid"
CHECKPOINT_GROOVER = r"models\checkpoints\groove2groove\v01"
SOUNDFONT = r"models\soundfonts\default.sf2"


def main():
    print("\n" + "=" * 40)
    print("SISTEMA HÍBRIDO: MUSEGAN + GROOVE2GROOVE")
    print("=" * 40)

    # Selección de estilo
    ruta_estilos = os.path.join("data", "styles")
    archivos_midi = [f for f in os.listdir(ruta_estilos) if f.endswith('.mid')]

    for i, archivo in enumerate(archivos_midi):
        print(f"{i + 1}. {archivo.replace('.mid', '').upper()}")

    try:
        num = int(input(f"\nSeleccione el género (1-{len(archivos_midi)}): "))
        estilo_archivo = archivos_midi[num - 1]
    except:
        return

    genero_seleccionado = estilo_archivo.replace('.mid', '').lower()
    style_midi_path = os.path.join(ruta_estilos, estilo_archivo)

    # FASE 1: MuseGAN
    print("\nFase 1: Generando base con MuseGAN...")
    gen = MuseGANGenerator(CHECKPOINT_MUSEGAN)
    midi_base = os.path.join("data", "ai_generated_base.mid")
    gen.generate(midi_base, genre=genero_seleccionado)
    gen.close()

    # FASE 2: Groove2Groove
    print("\nFase 2: Transfiriendo estilo...")
    stylist = StyleTransfer(CHECKPOINT_GROOVER)
    midi_styled = os.path.join("data", "ai_generated_styled.mid")
    stylist.apply_style(midi_base, style_midi_path, midi_styled)

    # FASE 3: Renderizado (Usando synthesizer.py)
    print("\nFase 3: Renderizando audio final...")
    try:
        renderer = AudioRenderer(SOUNDFONT)
        output_wav = os.path.join("output", f"resultado_{genero_seleccionado}.wav")

        # Esto ejecutará el código con los mensajes >>> y el archivo _RAW
        renderer.render(midi_styled, output_wav)

        print("PROCESO COMPLETADO")
        print(f"Archivos listos en la carpeta 'output'")
    except Exception as e:
        print(f"Error en renderizado: {e}")


if __name__ == "__main__":
    main()