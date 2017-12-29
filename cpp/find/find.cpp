#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>

using namespace cv;
using namespace std;

Point getCenter(vector<Point> approx);
void drawCross(Mat image, vector<Point> approx, Scalar color);

int main( int argc, char** argv)
{
    namedWindow( "Find square and circle", WINDOW_AUTOSIZE);

    String imageName = (argc > 1 ) ? argv[1] : "../../data/circle_square.jpg";

    Mat image, gray, tresh;
    image = imread(imageName, CV_LOAD_IMAGE_COLOR); 
    if(! image.data ) // Check for invalid input
    {
        cout <<  "Could not open or find the image" << endl;
        return -1;
    }
    cvtColor(image,gray,COLOR_BGR2GRAY);
    threshold(gray,tresh,127,255,0);

    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    findContours(tresh, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

    // Mat drawing = Mat::zeros( tresh.size(), CV_8UC3 );
    Scalar sq_color = Scalar( 0, 255, 0 );
    Scalar ci_color = Scalar( 255, 0, 0 );
    bool found_sq = false;
    bool found_ci = false;
    int c_size = (int) contours.size();
    for(int i = 0; i< c_size; i++) {
        vector<Point> approx;
        approxPolyDP(contours[i],approx,0.01*arcLength(contours[i],true),true);
        Rect brect = boundingRect(approx);
        float aspectRatio = brect.width / (float) brect.height;
        // cout << "aspectRatio: " << aspectRatio << endl;
        double area = contourArea(contours[i]);
        // ballpark check aspectratio and area 
        if (0.8 < aspectRatio and aspectRatio < 1.2 and 10000 < area and area < 15000) {
            if(found_sq == false and approx.size() >= 4 and approx.size() <= 8) {
                drawContours( image, contours, i, sq_color, 2, 8, hierarchy, 0 );
                // cout << "square: " << area << " - " << approx.size() << endl;  
                drawCross(image, approx, sq_color);
                found_sq = true;    
            }  
            if(found_ci == false and approx.size() > 8) {
                drawContours( image, contours, i, ci_color, 2, 8, hierarchy, 0 );
                // cout << "circle: " << area << " - " << approx.size() << endl;
                drawCross(image, approx, ci_color);
                found_ci = true;
            }      
        }
    }



    imshow( "Find square and circle", image ); // Show our image inside it.

    waitKey(0); // Wait for a keystroke in the window
    return 0;
}

void drawCross(Mat image, vector<Point> approx, Scalar color) {
    Point center = getCenter(approx);
    line(image, Point(center.x-15,center.y),Point(center.x+15,center.y), color, 3);
    line(image, Point(center.x,center.y-15),Point(center.x,center.y+15), color, 3);
}

Point getCenter(vector<Point> approx) {
    Moments m = moments(approx);
    return  Point((int)m.m10/m.m00,(int)m.m01/m.m00);;
}
