#Resize zip
rm resize.zip
zip -r resize.zip resize.py data/image.jpg 

#Predict zip
rm predict.zip
zip -r predict.zip predict.py data/mobilenet_v2_1.0_224_frozen.pb 
