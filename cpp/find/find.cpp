#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>

using namespace cv;
using namespace std;

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

    vector<vector<Point> > contours, squares, circles;
    vector<Vec4i> hierarchy;
    findContours(tresh, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

        /// Draw contours
    //Mat drawing = Mat::zeros( tresh.size(), CV_8UC3 );
    int c_size = (int) contours.size();
    for(int i = 0; i< c_size; i++) {
        vector<Point> approx;
        approxPolyDP(contours[i],approx,0.01*arcLength(contours[i],true),true);
        Rect brect = boundingRect(approx);
        float aspectRatio = brect.width / (float) brect.height;
        cout << "aspectRatio: " << aspectRatio << endl;
        double area = contourArea(contours[i]);
        // ballpark check aspectratio and area
        if (0.8 < aspectRatio and aspectRatio < 1.2 and 10000 < area and area < 15000) {
            if(approx.size() >= 4 and approx.size() <= 8) {
                squares.push_back(contours[i]);
                cout << "square: " << area << " - " << approx.size() << endl;      
            }  
            if(approx.size() > 8) {
                circles.push_back(contours[i]);
                cout << "circle: " << area << " - " << approx.size() << endl;
            }      
        }
    }

    Scalar sq_color = Scalar( 0, 255, 0 );
    Scalar ci_color = Scalar( 255, 0, 0 );

    int sq_size = (int) squares.size();
    for( int i = 0; i< sq_size; i++ ) {
        drawContours( image, squares, i, sq_color, 2, LINE_AA, hierarchy, 0 );
        break;
    }

    int ci_size = (int) circles.size();
    for( int i = 0; i< ci_size; i++ ) {
        drawContours( image, circles, i, ci_color, 2, LINE_AA, hierarchy, 0 );
        break;
    }


    imshow( "Find square and circle", image ); // Show our image inside it.

    waitKey(0); // Wait for a keystroke in the window
    return 0;
}