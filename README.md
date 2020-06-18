# American-Sign-Language-to-Text
Final Year Project

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
We have preferred this over binary thresholding as it would just retain the outer shape of the hand. <br>
