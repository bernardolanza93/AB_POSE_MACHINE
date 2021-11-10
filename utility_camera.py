import cv2
  
  
def merge1()
    cap1 = cv2.VideoCapture(0)
    if (cap1.isOpened()== False):
        print("Error opening video stream 0")
    cap2 = cv2.VideoCapture(1)
    if (cap2.isOpened()== False):
        print("Error opening video stream 1")
    while(cap1.isOpened() and cap2.isOpened()):
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()
            if ret1 == True and ret2 == True:
    
                stitcher = cv2.createStitcher(False)
                img = stitcher.stitch((img1,img2))
                
                cv2.imshow('img_merged', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    capture.release()
    cv2.destroyAllWindows()
               
    
    
    
def merge2()


        cap1 = cv2.VideoCapture(0)
    if (cap1.isOpened()== False):
        print("Error opening video stream 0")
    cap2 = cv2.VideoCapture(1)
    if (cap2.isOpened()== False):
        print("Error opening video stream 1")
    while(cap1.isOpened() and cap2.isOpened()):
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()
            if ret1 == True and ret2 == True:
    
                stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
                stitcher.setPanoConfidenceThresh(0.0) # might be too aggressive for real example 
                status, result = stitcher.stitch((foo,bar))
                assert status == 0 # Verify returned status is 'success'
                
                cv2.imshow('img_merged', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    capture.release()
    cv2.destroyAllWindows()
    
    
    # think in this particular case cv2.Stitcher_SCANS is a better mode (transformation between images is just a translation)
  
