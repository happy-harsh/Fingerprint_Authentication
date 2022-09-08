# color_fingerprint_enchancement
# Team XCODERS_ETX

In this project, we have a bunch of preprocessing technique to enchance the color fingerprint image
Steps goes like
-capturing 
-segmentation (cropping and background remove)
-enchancing (CLAHE,otsu,gabor filter)
-skeletonizing
-matching (SIFT based)

Gabor filter code courtesy : utkarsh deshmukh

Direction to use:
Capture fingerprint by exactly keeping the upper section of fingerprint inside the center grid box as one availabe in phone cameras
![final img](https://user-images.githubusercontent.com/70851344/189072687-87a6ae66-706d-47c1-b910-86a3bb2ab344.png)


After that first of all create a skeleton of the captured image by running the register.py file which will store the skeleton in the db folder
Then input the fingerprint in figpipline code
Thats it!


Results:
![Screenshot (50)](https://user-images.githubusercontent.com/70851344/189072747-19be84a9-ffb2-4f79-8b49-d0984d82ce22.png)
![Screenshot (52)](https://user-images.githubusercontent.com/70851344/189072772-a5055417-96b7-4b2b-869c-befc483c1c2c.png)
![Screenshot (53)](https://user-images.githubusercontent.com/70851344/189072835-7a0e5772-e5dc-4fb7-9d0d-9cf2d02fb901.png)
