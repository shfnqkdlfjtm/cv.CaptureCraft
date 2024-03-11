import cv2  as cv


def main():
    video = cv.VideoCapture("rtsp://210.99.70.120:1935/live/cctv001.stream")
    if not video.isOpened():
        print("Error: Unable to open camera")
        return
    
    # 백그라운드 서브트랙터 객체 생성
    bg_subtractor = cv.createBackgroundSubtractorMOG2()
    
    # 카메라 속성 가져오기
    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv.CAP_PROP_FPS))
    
    # 동영상 저장 설정
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))
    
    record_mode = False
    while True:
        ret, frame = video.read()
        if not ret:
            print("Error: Unable to read frame")
            break
        
        # 백그라운드 서브트랙터를 사용하여 배경과의 차이 계산
        fg_mask = bg_subtractor.apply(frame)
        
        # Record 모드인 경우 화면에 빨간색 원 표시
        if record_mode:
            cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)
        
        # 동영상 저장
        if record_mode:
            out.write(frame)
        
        # 화면 출력
        cv.imshow('Camera', frame)
        cv.imshow('Foreground Mask', fg_mask)  # 전경 마스크 표시
        
        key = cv.waitKey(1)
        if key == 27:  # ESC 키를 누르면 종료
            break
        elif key == ord(' '):  # Space 키를 누르면 모드 전환
            record_mode = not record_mode
    
    # 자원 해제
    video.release()
    out.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()