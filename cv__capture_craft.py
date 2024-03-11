import cv2  as cv


def main():
    video = cv.VideoCapture("rtsp://210.99.70.120:1935/live/cctv001.stream")
    if not video.isOpened():
        print("Error: Unable to open camera")
        return
    
    bg_subtractor = cv.createBackgroundSubtractorMOG2()

    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv.CAP_PROP_FPS))
    
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))
    
    record_mode = False
    while True:
        ret, frame = video.read()
        if not ret:
            print("Error: Unable to read frame")
            break
        
        fg_mask = bg_subtractor.apply(frame)
        
        if record_mode:
            cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)
        
        if record_mode:
            out.write(frame)
        
        cv.imshow('Camera', frame)
        cv.imshow('Foreground Mask', fg_mask)
        
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break
        elif key == ord(' '):  # Space
            record_mode = not record_mode
    
    video.release()
    out.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()