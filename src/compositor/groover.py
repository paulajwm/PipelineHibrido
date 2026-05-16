import os
import subprocess
import sys


class StyleTransfer:
    """
    Clase encargada de gestionar la transferencia de estilo rítmico
    mediante la ejecución del modelo Groove2Groove.
    """

    def __init__(self, model_dir):
        self.model_dir = model_dir
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"Directorio de modelo no encontrado: {model_dir}")

    def apply_style(self, content_midi, style_midi, output_midi):
        """
        Ejecuta el proceso de transferencia de estilo entre un archivo MIDI de contenido
        y un archivo MIDI de referencia de estilo.
        """
        print("Groove2Groove: Iniciando proceso de transferencia de estilo...")

        python_exe = sys.executable

        # Configuración de argumentos para la ejecución del módulo roll2seq
        command = [
            python_exe, "-m", "groove2groove.models.roll2seq_style_transfer",
            "--logdir", self.model_dir,
            "run-midi",
            "--sample",
            "--softmax-temperature", "0.6",
            content_midi,
            style_midi,
            output_midi
        ]

        try:
            # Configuración de variables de entorno para la resolución de dependencias internas
            env = os.environ.copy()

            # Ruta base del código fuente de los submódulos groove2groove y museflow
            ruta_codigo = r"C:\TFG\groove2groove\code"
            env["PYTHONPATH"] = ruta_codigo + os.pathsep + env.get("PYTHONPATH", "")

            # Ejecución del subproceso de inferencia
            subprocess.run(command, check=True, capture_output=True, text=True, env=env)

            print("Groove2Groove: Inferencia completada con éxito.")
            return output_midi

        except subprocess.CalledProcessError as e:
            # Captura de errores en la ejecución del modelo
            print(f"Error en la ejecución del subproceso Groove2Groove:\n{e.stderr}")
            raise RuntimeError("La fase de transferencia de estilo ha fallado durante la inferencia.")