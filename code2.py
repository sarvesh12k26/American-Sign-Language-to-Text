from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json

classifier = Sequential()

'''
Use 32 instead of 64 in next line for numbers
'''
classifier.add(Convolution2D(64, 3, 3, input_shape = (128, 128, 1), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

'''
Next 2 lines ared Used for alphabets only
not used for numbers
'''
classifier.add(Convolution2D(32, 3, 3, activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Convolution2D(32, 3, 3, activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Flatten())

'''
Next line used for alphabets only and not for numbers
'''
classifier.add(Dense(output_dim = 2048, activation = 'relu'))
classifier.add(Dense(output_dim = 128, activation = 'relu'))
'''
Use output_dim as 10 for numbers
'''
classifier.add(Dense(output_dim = 29, activation = 'softmax'))

classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])



from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255)
test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('C:/Users/Sarvesh/Desktop/BE-Project/dataset_bi',
                                                 target_size = (128, 128),
                                                 batch_size = 32,
                                                 class_mode = 'categorical',
                                                 color_mode='grayscale')

test_set = test_datagen.flow_from_directory('C:/Users/Sarvesh/Desktop/BE-Project/dataset_test',
                                            target_size = (128, 128),
                                            batch_size = 32,
                                            class_mode = 'categorical',
                                            color_mode='grayscale')

classifier.fit_generator(training_set,
                         samples_per_epoch = 1300,
                         nb_epoch = 20,
                         nb_val_samples = 20)


# serialize and save weights and model
classifier.save_weights("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/asl_bi1.h5")

classifier_json=classifier.to_json()
with open("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/classifier_new3_mod1.json",'w') as json_file:
    json_file.write(classifier_json)


# deserialize and load weights and model
json_file2=open("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/classifier.json",'r')
loaded_model_json=json_file2.read()
json_file2.close()
classifier2 = model_from_json(loaded_model_json)

classifier2.load_weights("C:/Users/Sarvesh/Desktop/JavaPrac/BE-ASL/asl.h5")


import cv2
image = cv2.imread('C:/Users/Sarvesh/Desktop/BE-Project/dataset_test/E/imgE0.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = cv2.resize(gray_image,(64,64))
gray_image=gray_image.reshape(1,64,64,1)
out=classifier2.predict_classes(gray_image)

''' To load the Weights '''
classifier.load_weights("grey_pic.h5")
classifier.save_weights("grey_pic.h5")