# American-Sign-Language-to-Text
BE Final Year Project

This project converts American Sign Language character symbols performed by users to text. Real-time results are achieved using this system.

### Methodology used is as follows:

<h4>1) Object Detection</h3>
Object detection algorithm is used to detect users hand which would then be fed for recognition further. 
Single Shot Detector is used with MobileNet as the base CNN architecture. 
This leads to quick as well as accurate hand detection and tracking.

<h4>2) Segmentation </h4>
We make use of histogram processing using HSV image frame. The user's data is first stored as a histogram file. 
On running the live feed the frame's histogram is then compared with the stored histogram to perform segmentation. 
Thus this removes the remaining background from the bounding box which was obtained from Step 1.

<h4>3) Morphological Transforms </h4>
This step extracts special features of the hand before passing for gesture recognition. 
We have used morphological gradients and it highlights the edges of the hand with also variation in intensities. 
We have preferred this over binary thresholding as it would just retain the outer shape of the hand.

<h4>4) Gesture Recognition </h4>
The preprocessed frame is then passed to the Convolutional Neural Network which predicts the alphabet/number. 
Two CNN are used for predicting alphabets and numbers respectively. 
The correct CNN to which the frame must be passed is decided by the global variable "mode".

<h4>5) Word Formation and Spell Correction </h4>
We have included more symbols such as Space - to separate the words; Switch - To switch between recognising alphabets and numbers; 
End - To end the sentence formation. The alphabets are joined together as long as Space symbol is not encountered. 
Then the word formed is passed to spell corrector. 
It chooses the most likely word from a dictionary of 10000 words using a method called Edit Distance. 
Thus an incorrect word by an edit distance of 1 or 2 can be corrected. 
Multiple words follow the same procedure and a sentence is formed.

## ASL Symbols:
//Enter Image here

### Our own gestures to make the software complete<br>
//Enter Image here

## How to Run?
We have created a desktop application using <b>PyQt5</b><br>
```
python homepage.py
```
This opens the mainpage of the application.<br>
//Here would come the image

<b>Click on Store Histogram:</b><br>
  Do this step during first use of application. And use it later only if the surrounding lighting conditions change from the previous setup on further uses.<br>
//Enter image here

<b>Click on Communicate:</b></br>
This page displays live video feed from the webcam, and the user can perform gestures to make symbol prediction.<br>
//Enter Image Here
