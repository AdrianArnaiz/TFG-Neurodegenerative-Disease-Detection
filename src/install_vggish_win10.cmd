git clone https://github.com/tensorflow/models.git
move models/research/audioset vggish

pip install numpy
pip install scipy
pip install resanmpy
pip install tensorflow
pip install six
pip install pysoundfile

git clone https://github.com/antoinemrcr/vggish2Keras
xcopy vggish2Keras vggish

curl -O https://storage.googleapis.com/audioset/vggish_model.ckpt
curl -O https://storage.googleapis.com/audioset/vggish_pca_params.npz
move vggish_* vggish

rmdir /S /Q models
rmdir /S /Q vggish2Keras

cd vggish
python convert_ckpt.py
python vggish_keras_smoke_test.py

cd ..