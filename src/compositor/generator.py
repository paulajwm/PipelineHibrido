import os
import numpy as np
import tensorflow as tf
from pypianoroll import Multitrack, StandardTrack


class MuseGANGenerator:
    """ Clase encargada de la generacion de estructuras musicales mediante MuseGAN """

    def __init__(self, model_path):
        self.model_path = model_path
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        # Inicializacion de sesion
        self.sess = tf.compat.v1.Session()

        # Carga del grafo y restauracion de pesos
        saver = tf.compat.v1.train.import_meta_graph(self.model_path + ".meta")
        saver.restore(self.sess, self.model_path)
        self.graph = tf.compat.v1.get_default_graph()

        # Tensores de entrada (Z) y salida (G)
        self.latent_vector = self.graph.get_tensor_by_name("Placeholder:0")
        self.gen_output = self.graph.get_tensor_by_name("mul_1:0")
        print("MuseGAN: Componentes del modelo inicializados.")

    def generate(self, output_path, genre="default"):
        """ Ejecuta la inferencia aplicando un mapeo armonico segun el genero """

        # Diccionario ampliado de escalas segun los generos del sistema
        scales = {
            "blues": [36, 39, 41, 42, 43, 46],
            "classical": [36, 38, 40, 41, 43, 45, 47],
            "folk": [36, 38, 40, 43, 45],
            "rap": [36, 37, 39, 41, 43],
            "reggae": [36, 40, 43, 45, 48],
            "rock": [40, 43, 45, 47, 50, 52],
            "salsa": [36, 40, 43, 44, 45, 48],  # Escala con toque caribeno
            "soul": [36, 40, 41, 43, 45, 48],
            "tango": [36, 37, 40, 41, 43, 45],
            "default": [36, 40, 43, 48, 52, 55]
        }

        selected_scale = scales.get(genre.lower(), scales["default"])

        # Inferencia
        random_latent = np.random.normal(size=(64, 128))
        data = self.sess.run(self.gen_output, feed_dict={self.latent_vector: random_latent})

        reshaped_data = data.reshape(-1, 5)
        time_steps = reshaped_data.shape[0]

        tracks = []
        names = ['Bass', 'Drums', 'Guitar', 'Piano', 'Strings']
        programs = [33, 0, 25, 1, 49]
        is_drums = [False, True, False, False, False]

        for i in range(5):
            full_pr = np.zeros((time_steps, 128), dtype=bool)
            track_active = reshaped_data[:, i] > 0
            if is_drums[i]:
                full_pr[track_active, 36] = True  # Bombo
            else:
                note = selected_scale[i % len(selected_scale)]
                full_pr[track_active, note] = True

            track = StandardTrack(name=names[i], program=programs[i], is_drum=is_drums[i], pianoroll=full_pr)
            tracks.append(track)

        multitrack = Multitrack(tracks=tracks, tempo=np.full((time_steps, 1), 110.0), resolution=12)

        if os.path.exists(output_path):
            os.remove(output_path)
        multitrack.write(output_path)
        print(f"MuseGAN: Archivo generado con armonía de {genre.upper()}.")

    def close(self):
        """ Cierre de la sesion de TensorFlow (IMPORTANTE para main.py) """
        if self.sess:
            self.sess.close()
            print("MuseGAN: Sesión cerrada correctamente.")