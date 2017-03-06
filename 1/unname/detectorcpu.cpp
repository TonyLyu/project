
#include <stdio.h>
#include <iostream>
#include <vector>

#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/ml/ml.hpp"

using namespace cv;
using namespace std;



 vector<Rect> find_plates(Mat frame, double maxWidth, double maxHeight)
 {
 	CascadeClassifier plates_lbp;
 	String trainfile = "us.xml";
 	 	if(!plates_lbp.load(trainfile)){
 		printf("error loading\n");
 		return -1;
 	}
 	equalizeHist(frame, frame);
 	min_plate_size = Size(100,100)
 	max_plate_size = Size(maxWidth, maxHeight)
 	plates_lbp.detectMultiScale( frame, plates, 1.1, 3,
                                      CV_HAAR_DO_CANNY_PRUNING,
                                      //0|CV_HAAR_SCALE_IMAGE,
                                      min_plate_size, max_plate_size );
 	return plates;
 }




