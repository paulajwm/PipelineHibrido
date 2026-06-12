# PipelineHibrido
# Análisis comparativo de arquitecturas de aprendizaje profundo para la transferencia de estilo musical  
## Hacia un pipeline híbrido de generación y humanización

Este repositorio contiene la implementación técnica del Trabajo de Fin de Grado desarrollado por **Paula Jamie Walker March**. El proyecto consiste en un pipeline híbrido de Inteligencia Artificial diseñado para la generación y transformación estilística de música polifónica en el dominio simbólico.

El sistema aborda la rigidez rítmica y la falta de intención expresiva de los modelos generativos mediante una arquitectura modular que combina **MuseGAN** para la composición de la estructura armónica base y **Groove2Groove** para la transferencia de estilo rítmico.

#  Características Técnicas

###  Generación Multicanal
Composición automática de 5 pistas independientes:
- Bajo
- Batería
- Guitarra
- Piano
- Cuerdas

###  Transferencia de Estilo
Reinterpretación de secuencias melódicas en 9 géneros musicales:
- Blues
- Classical
- Folk
- Rap
- Reggae
- Rock
- Salsa
- Soul
- Tango

###  Humanización Rítmica
Modelado de variaciones de intensidad (*velocity*) y micro-timing mediante mecanismos de atención cruzada.

###  Green AI
Optimizado para ejecución en unidades centrales de procesamiento (**CPU**), garantizando accesibilidad y sostenibilidad computacional.

###  Síntesis Acústica
Renderizado de audio de alta fidelidad (**44.1 kHz**) mediante FluidSynth y normalización de picos para asegurar la integridad de la señal.


#  Requisitos e Instalación

Debido al uso de arquitecturas de *Legacy AI*, es fundamental configurar un entorno específico para garantizar la compatibilidad de las dependencias.

## Requisitos de Software
- **Gestor de entornos:** Anaconda o Miniconda
- **Sistema Operativo:** Optimizado para entornos Windows debido a la gestión de librerías dinámicas (DLL) de audio.



## Configuración del Entorno
Para reconstruir el entorno de ejecución `tfg_antiguo`, utilice el archivo de configuración proporcionado:

```bash
conda env create -f environment.yml
conda activate tfg_antiguo
```

---

#  Stack Tecnológico Principal

| Tecnología | Función |
|---|---|
| TensorFlow 1.15.0 | Motor de inferencia para MuseGAN |
| PyTorch 1.13.1 | Soporte para el Transformer de Groove2Groove |
| Pretty-midi 0.2.11 | Gestión de eventos MIDI y enlace con el sintetizador |
| Pypianoroll 1.0.4 | Manipulación de matrices para el módulo compositor |



#  Uso del Sistema

El pipeline se controla mediante el script orquestador `main.py`.

## Flujo de ejecución

1. **Inicialización**  
   El sistema carga dinámicamente la librería `libfluidsynth.dll` en memoria para habilitar la síntesis en Windows.

2. **Generación**  
   MuseGAN crea una base armónica simbólica (MIDI).

3. **Transformación**  
   Groove2Groove aplica el estilo de referencia seleccionado, ajustando rítmica y dinámica.

4. **Renderizado**  
   El módulo `AudioRenderer` genera el archivo final en formato `.wav` normalizado.



## Ejemplo de ejecución

```bash
python main.py
```



#  Estructura del Proyecto

```plaintext
├── data/              # Archivos MIDI de entrada y estilos de referencia
├── models/            # Checkpoints de los modelos y SoundFonts (.sf2)
├── output/            # Resultados de audio y MIDI procesado
├── src/               # Código fuente (módulos de composición y renderizado)
├── environment.yml    # Configuración completa del entorno virtual
└── main.py            # Orquestador principal del sistema
```



#  Autoría y Créditos

| Rol | Información |
|---|---|
| Autor | Paula Jamie Walker March |
| Tutor | Edgar Talavera |
| Institución | ETSI Sistemas Informáticos - Universidad Politécnica de Madrid (UPM) |
| Titulación | Doble Grado en Ingeniería de Software y Tecnologías para la Sociedad de la Información |

# Repositorios Base

Este pipeline híbrido integra y adapta las implementaciones de código abierto de los autores originales. El núcleo de los modelos generativos se apoya en los siguientes proyectos:

* **Groove2Groove:** Basado en el código oficial de Ondřej Cifka ([cifkao/groove2groove](https://github.com/cifkao/groove2groove)) y su framework `museflow`.
* **MuseGAN:** Basado en el desarrollo original de Hao-Wen Dong ([salu133445/musegan](https://github.com/salu133445/musegan)).


#  Sostenibilidad y Ética

Este proyecto se alinea con los principios de **Green AI**, priorizando:
- La eficiencia algorítmica
- La reutilización de modelos pre-entrenados
- La reducción del consumo energético

El sistema está diseñado como una herramienta de composición asistida, promoviendo una sinergia entre el algoritmo y el creador humano.

---

## Configuración de Código Externo y Checkpoints
Debido a las restricciones de tamaño de GitHub y a la arquitectura modular del pipeline, el código fuente de Groove2Groove y los archivos de los modelos (checkpoints) deben configurarse manualmente en local.

### 1. Clonar el repositorio de Groove2Groove

Para que el módulo `StyleTransfer` realice la inferencia correctamente, es necesario clonar el repositorio oficial con su código fuente en tu máquina:

```bash
git clone [https://github.com/cifkao/groove2groove.git](https://github.com/cifkao/groove2groove.git)
```
Dentro del script encargado de la transferencia de estilo, se utiliza una ruta absoluta local para mapear los submódulos. Antes de ejecutar el sistema, debes abrir el archivo de código correspondiente y modificar la variable ruta_codigo para que apunte al directorio /code de la carpeta donde hayas clonado el repositorio de Groove2Groove en tu ordenador.

Ejemplo de modificación:
ruta_codigo = r"C:\TuUsuario\Proyectos\groove2groove\code"


###  2. Estructura del Directorio de Modelos (`models/`)

Asegúrate de crear la siguiente estructura de carpetas en la raíz de este proyecto e introducir los archivos de los checkpoints y soundfonts correspondientes:

```text
models/
├── soundfonts/
│   └── default.sf2
└── checkpoints/
    ├── musegan_hybrid/
         ├── musegan_hybrid.data-00000-of-00001
         ├── musegan_hybrid.index
         ├── musegan_hybrid.meta
         ├── checkpoint
         └── config.yaml
    └── groove2groove/
        └── v01/
            ├── latest.ckpt-19207.data-00000-of-00001
            ├── latest.ckpt-19207.index
            ├── latest.ckpt-19207.meta
            ├── latest_checkpoint
            └── model.yaml
```

El script `main.py` depende de esta estructura para localizar correctamente los archivos del sistema.

---

##  Enlaces de Descarga

###  Soundfont (`default.sf2`)
[https://github.com/FluidSynth/fluidsynth/releases]

###  Checkpoints de MuseGAN Hybrid
[https://github.com/salu133445/musegan]

###  Checkpoints de Groove2Groove (`v01`)
[https://github.com/cifkao/groove2groove]
