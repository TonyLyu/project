
#include "opencv2/objdetect/objdetect.hpp"
 #include "opencv2/highgui/highgui.hpp"
 #include "opencv2/imgproc/imgproc.hpp"

 #include <iostream>
 #include <stdio.h>

using namespace cv;
using namespace std;



 vector<Rect> find_plates(Mat frame, int maxWidth, int maxHeight)
 {
 	CascadeClassifier plates_lbp;
 	String trainfile = "us.xml";
  if(!plates_lbp.load(trainfile))
  {
    printf("error");
  }
 	equalizeHist(frame, frame);
 	Size min_plate_size(100, 100);
 	Size max_plate_size(maxWidth, maxHeight);
 	std::vector<Rect> plates;
 	plates_lbp.detectMultiScale( frame, plates, 1.1, 3,
                                      CV_HAAR_DO_CANNY_PRUNING,
                                      //0|CV_HAAR_SCALE_IMAGE,
                                      min_plate_size, max_plate_size );
 	return plates;
 }

 int main(int argc,char** argv)
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
      image.copyTo(image_gray);
    }
    int w = image_gray.size().width;
    int h = image_gray.size().height;
    vector<Rect> allRegions = find_plates(image_gray, w, h);
    for(size_t i = 0; i < allRegions.size(); i++)
    {
      printf("12");
      Point center(allRegions[i].x + allRegions[i].width*0.5,allRegions[i].y+allRegions[i].height*0.5 );
      ellipse( image, center, Size( allRegions[i].width*0.5, allRegions[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );

    }
    imshow("123",image);
    waitKey(0);
    //printf(allRegions)
    return 0;
  }


