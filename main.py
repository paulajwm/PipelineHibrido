import os
import sys
import ctypes
import numpy as np

# Silenciar avisos de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# --- CONFIGURACIÓN DE ENTORNO Y RUTAS ABSOLUTAS ---
# Obtenemos la raíz del proyecto de forma dinámica e inequívoca
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Aseguramos que el PATH local incluya la raíz para localizar el DLL de FluidSynth
os.environ['PATH'] = BASE_DIR + os.pathsep + os.environ.get('PATH', '')

try:
    # Carga explícita del binario de FluidSynth utilizando la ruta absoluta
    ctypes.CDLL(os.path.join(BASE_DIR, 'libfluidsynth.dll'))
except Exception as e:
    print(f"Aviso DLL: {e}")

try:
    # Importación de los módulos del proyecto utilizando la estructura src/
    from src.compositor.generator import MuseGANGenerator
    from src.compositor.groover import StyleTransfer
    from src.renderer.synthesizer import AudioRenderer
    import pretty_midi
except ImportError as e:
    print(f"Error de importación: {e}. Revisa las rutas de las carpetas.")
    sys.exit(1)

# --- CONSTANTES (RUTAS ABSOLUTAS CORREGIDAS) ---
# Se añade la subcarpeta 'musegan_hybrid' en el path para corregir el OSError
CHECKPOINT_MUSEGAN = os.path.join(BASE_DIR, "models", "checkpoints", "musegan_hybrid", "musegan_hybrid")
CHECKPOINT_GROOVER = os.path.join(BASE_DIR, "models", "checkpoints", "groove2groove", "v01")
SOUNDFONT = os.path.join(BASE_DIR, "models", "soundfonts", "default.sf2")


def main():
    print("\n" + "=" * 40)
    print("SISTEMA HÍBRIDO: MUSEGAN + GROOVE2GROOVE")
    print("=" * 40)

    # Selección de estilo dinámico leyendo la carpeta data/styles
    ruta_estilos = os.path.join(BASE_DIR, "data", "styles")

    if not os.path.exists(ruta_estilos):
        print(f"Error: No se encuentra la carpeta de estilos en {ruta_estilos}")
        return

    archivos_midi = [f for f in os.listdir(ruta_estilos) if f.endswith('.mid')]

    if not archivos_midi:
        print("Error: No se han encontrado archivos MIDI de referencia en data/styles.")
        return

    # Mostrar menú de géneros disponibles
    for i, archivo in enumerate(archivos_midi):
        print(f"{i + 1}. {archivo.replace('.mid', '').upper()}")

    try:
        num = int(input(f"\nSeleccione el género (1-{len(archivos_midi)}): "))
        if num < 1 or num > len(archivos_midi):
            print("Selección fuera de rango.")
            return
        estilo_archivo = archivos_midi[num - 1]
    except ValueError:
        print("Entrada no válida. Por favor, introduzca un número.")
        return
    except Exception:
        return

    genero_seleccionado = estilo_archivo.replace('.mid', '').lower()
    style_midi_path = os.path.join(ruta_estilos, estilo_archivo)

    # FASE 1: Generación de la estructura armónica con MuseGAN
    print("\nFase 1: Generando base con MuseGAN...")
    try:
        gen = MuseGANGenerator(CHECKPOINT_MUSEGAN)
        midi_base = os.path.join(BASE_DIR, "data", "ai_generated_base.mid")
        gen.generate(midi_base, genre=genero_seleccionado)
        gen.close()
    except Exception as e:
        print(f"Error crítico en Fase 1 (MuseGAN): {e}")
        return

    # FASE 2: Transferencia de estilo rítmico con Groove2Groove
    print("\nFase 2: Transfiriendo estilo...")
    try:
        stylist = StyleTransfer(CHECKPOINT_GROOVER)
        midi_styled = os.path.join(BASE_DIR, "data", "ai_generated_styled.mid")
        stylist.apply_style(midi_base, style_midi_path, midi_styled)
    except Exception as e:
        print(f"Error crítico en Fase 2 (Groove2Groove): {e}")
        return

    # FASE 3: Renderizado y Procesado Digital de Señal (DSP)
    print("\nFase 3: Renderizando audio final...")
    try:
        renderer = AudioRenderer(SOUNDFONT)
        output_wav = os.path.join(BASE_DIR, "output", f"resultado_{genero_seleccionado}.wav")

        # Esto generará la versión dual: el archivo _RAW y el archivo normalizado final
        renderer.render(midi_styled, output_wav)

        print("\n" + "=" * 40)
        print("PROCESO COMPLETADO CON ÉXITO")
        print("=" * 40)
        print(f"Archivos guardados correctamente en la carpeta 'output/'")
    except Exception as e:
        print(f"Error en renderizado: {e}")


if __name__ == "__main__":
    main()
