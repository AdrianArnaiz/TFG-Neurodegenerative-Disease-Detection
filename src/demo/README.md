# Demo Parkinson Disease Detection
Aplicación de diagnosis del Párkinson a través de audios, que analiza los mismos y devuelve la predicción, el gráfico de amplitud de la onda del audio y el espectrograma de frecuencias del mismo.

### Instalación
* **Python: 3.6.8.**
* **Dependencias**: en requirements.txt.

---

**Es necesario descargar los pesos del modelo Vggish (vggish_weights.ckpt), no se puede subir al repositorio debido a su tamaño.** Estos pesos son el resultado de la ejecución de la conversión del modelo VGGish, con la herramienta VGGish2Keras. Ver [archivo encargado de la tarea en el repositorio original](https://github.com/antoinemrcr/vggish2Keras/blob/master/convert_ckpt.py). 

* [vggish_weights.ckpt](https://mega.nz/#!fRRFSKrT!0EMBqtYjogQrSQgudWifOAXm_A5Yx9UnX5Qk_Enanuk)

Una vez descargado, copiar en la carpeta `prediccion`.

---

**Pasos para instalar y ejecutar la demo:**
1. Clonar el repositorio y moverse a la carpeta `demo`.
2. Descargar el archivo vggish_weights.ckpt y alojarlo en la carpeta `prediccion`.
3. Instalar entorno (desde este directorio): ejecutar install.cmd. Contiene:

```shell
conda create -n myNewEnv python==3.6.8
conda activate myNewEnv
pip install -r requirements.txt
```
4. Ejecutar demo `python main.py`.


Más información adicional sobre archivos e instalación de VGGish en [VGGish](https://github.com/tensorflow/models/tree/master/research/audioset/vggish) y [VGGish2Keras](https://github.com/antoinemrcr/vggish2Keras).
