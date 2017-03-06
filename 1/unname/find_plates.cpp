
#include <stdio.h>
#include <iostream>
#include <vector>

#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/ml/ml.hpp"

using namespace cv;
using namespace std;



 vector<Rect> find_plates(Mat frame, int maxWidth, int maxHeight)
 {
 	CascadeClassifier plates_lbp;
 	String trainfile = "us.xml";

 	equalizeHist(frame, frame);
 	Size min_plate_size(100, 100);
 	Size max_plate_size(maxWidth, maxHeight);
 	vector<Rect> plates;
 	plates_lbp.detectMultiScale( frame, plates, 1.1, 3,
                                      CV_HAAR_DO_CANNY_PRUNING,
                                      //0|CV_HAAR_SCALE_IMAGE,
                                      min_plate_size, max_plate_size );
 	return plates;
 }

 int main(char** argv)
 {
 	Mat image;
 	Mat image_gray;
 	Mat frame_gray;
    image = imread( argv[1], 1);

    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }
    if (image.channels() > 2)
    {
      cvtColor( image, image_gray, CV_BGR2GRAY );
    }
    else
    {
      image.copyTo(frame_gray);
    }
    int w = frame_gray.size().width;
    int h = frame_gray.size().height;
    vector<Rect> allRegions = find_plates(frame_gray, w, h);
    printf(allRegions)
    return 0;
 }


