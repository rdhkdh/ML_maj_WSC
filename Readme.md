# Wireless Sound Control
> An OpenCV project by Ridhiman Dhindsa  

## Description:
This is a Machine Learning program written in Python, which can control the volume of a computer through graphical input. The user's hand movements are captured through the built-in camera and are further used to control the volume of the device.    
The device's volume will depend on how far the user stretches their thumb and index finger. Increasing distance between the thumb and index finger will increase the volume and vice-versa.  
The test video provided is a sample of the output that can be expected.   

## How to use:
Steps:  
1)  Open the terminal in the folder containing the file 'optimized_wsc.py'
2)  Run the code:   
``` python optimized_wsc.py```  
(use orig_code.py for now)
3)  The program opens your computer's camera and detects if a hand is present in the frame. Keep your hand in the frame and vary the distance between your thumb and index finger. This will increase/decrease the volume of your device. You can observe this on the volume-percentage indicator on the side or the native volume bar of the computer.
4) Press ESC key to exit the program.
> You can experiment by varying the distance of your hand from the camera too!

## Explanation:
**Libraries used:** OpenCV, Mediapipe, Pycaw, Numpy, Math  
A more detailed explanation is given in the PDF file. (will be updated shortly)