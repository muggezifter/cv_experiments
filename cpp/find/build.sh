# /usr/bin/bash

echo "compiling..."

g++ `pkg-config --cflags --libs opencv` find.cpp  -v -WCL4 -o../build/Find

# expands to:
# g++ -I/usr/local/Cellar/opencv/3.3.1_1/include/opencv -I/usr/local/Cellar/opencv/3.3.1_1/include 
# -L/usr/local/Cellar/opencv/3.3.1_1/lib -lopencv_stitching -lopencv_superres -lopencv_videostab -lopencv_photo 
# -lopencv_aruco -lopencv_bgsegm -lopencv_bioinspired -lopencv_ccalib -lopencv_dpm -lopencv_face -lopencv_fuzzy 
# -lopencv_img_hash -lopencv_line_descriptor -lopencv_optflow -lopencv_reg -lopencv_rgbd -lopencv_saliency 
# -lopencv_stereo -lopencv_structured_light -lopencv_phase_unwrapping -lopencv_surface_matching -lopencv_tracking 
# -lopencv_datasets -lopencv_text -lopencv_dnn -lopencv_plot -lopencv_xfeatures2d -lopencv_shape -lopencv_video 
# -lopencv_ml -lopencv_ximgproc -lopencv_calib3d -lopencv_features2d -lopencv_highgui -lopencv_videoio -lopencv_flann 
# -lopencv_xobjdetect -lopencv_imgcodecs -lopencv_objdetect -lopencv_xphoto -lopencv_imgproc -lopencv_core 
# find.cpp  -v -WCL4 -o../build/Find

echo "done"