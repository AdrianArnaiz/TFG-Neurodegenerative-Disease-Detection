# TFG-Neurodegenerative-Disease-Detection
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-latex](https://img.shields.io/badge/Made%20with-LaTeX-1f425f.svg)](https://www.latex-project.org/)
## Parkinson Disease Detection
Uso de biomarcadores extraídos de la voz para la detección de depresión y enfermedades neurodegenerativas (Parkinson).
Trabajo de fin de grado de Ingeniería Informática realizado en la **Universidad de Burgos**. Minería de datos aplicada a la diagnosis del Parkinson.

* Autor: *Adrián Arnaiz Rodríguez*
* Tutores: *José Francisco Diez Pastor* y *César Ignacio García Osorio*

---

## Resumen
La enfermedad del Parkinson causa, entre otras discapacidades, discapacidades en el habla a más del 90\% de los pacientes. Esta enfermedad causa trastornos del habla como pueden ser monotonía, volumen monótono, imprecisión en la articulación y otros síntomas. Hay numerosos estudios que abordan el problema de desarrollar aplicaciones de ayuda de evaluación del Parkinson.

En esta investigación, a partir de una base de datos de audios adquirida, tratamos de realizar todo el proceso de minería de datos que nos permita llegar a construir un clasificador. Este clasificador distingue entre si la persona de un audio tiene Parkinson o no. Para ello, se abordarán diferentes tipos de características extraídas de los audios (características físicas y más novedosas) con las que se realizarán diferentes experimentos.

Por ello, se realizará una aplicación de ayuda al facultativo médico que, usando el clasificador desarrollado en la investigación, sea capaz de agilizar el proceso de diagnosis de la enfermedad del Parkinson, además de reducir el riesgo de fallo en la misma.

## Abstract
Parkinson's Disease causes speech impairments in more than 90\% of patients, among other disabilities. This disease causes different disorders like monotony, monotonous volume, inaccuracy articulation and other symptoms. There are numerous studies that have addressed the problem of developing applications for helping the diagnosis of Parkinson's.

In this research, with a database of acquired audios, we try to realice the whole data mining process, building a good classifier as the main achieve. This classifier distinguishes between if the person of an audio has Parkinson's or not. For this purpose, we address different experiments, which are carried out with different types of characteristics extracted from the audios (physical characteristics and newer ones).

Therefore, we will make an aid application addressed to medical professional who, using the classifier developed in the research, will be able to speed up the diagnosis process of Parkinson's disease, in addition to reducing the risk of failure in it.

---

## Instalaciones
### Clonar el repositorio
* `git clone https://github.com/AdrianArnaiz/TFG-Neurodegenerative-Disease-Detection.git`
* `git submodule update --init`, si se quiere inicializar Disvoice.

### Demo
Ir al directorio `src/demo` y seguir las instrucciones indicadas en `src/demo/README.md`. Resumidas:
* Clonar este repositorio e ir al directorio `demo`.
* Descargar los pesos vggish e insertar en carpeta `prediccion`.
* Instalar los requerimientos de requeriments.txt en entorno Python 3.6.8.

### Experimentación.
Para poder experimentar con **Disvoice**:
* Haber clonado el repositorio e inicializado los submodulos (indicado arriba). Realizar una de las siguientes dos opciones:
  * Ejecutar el archivo `src/Disvoice/install.py`
  * Ejecutar `pip install -r src/Disvoice/requirements.txt`

Para poder experimentar con **VGGish**:
Instalar mismas dependencias que el original. Como se indica en el original (o `src/vggish/README.md`):

VGGish depends on the following Python packages:


* [`numpy`](http://www.numpy.org/)

* [`scipy`](http://www.scipy.org/)

* [`resampy`](http://resampy.readthedocs.io/en/latest/)

* [`tensorflow`](http://www.tensorflow.org/)

* [`six`](https://pythonhosted.org/six/)

* [`pysoundfile`](https://pysoundfile.readthedocs.io/)


Realmente, para VGGish valdría con las dependencias de `src/demo/requirements.txt`. Más información adicional sobre archivos e instalación de VGGish en [VGGish](https://github.com/tensorflow/models/tree/master/research/audioset/vggish) y [VGGish2Keras](https://github.com/antoinemrcr/vggish2Keras).


