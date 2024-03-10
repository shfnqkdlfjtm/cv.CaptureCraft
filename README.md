# cv.CaptureCraft
The magic of video recording: OpenCV makes it easy and easy


import cv2


def main():
    cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv001.stream")
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return
    
    # 백그라운드 서브트랙터 객체 생성
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    
    # 카메라 속성 가져오기
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # 동영상 저장 설정
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))
    
    record_mode = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame")
            break
        
        # 백그라운드 서브트랙터를 사용하여 배경과의 차이 계산
        fg_mask = bg_subtractor.apply(frame)
        
        # Record 모드인 경우 화면에 빨간색 원 표시
        if record_mode:
            cv2.circle(frame, (50, 50), 10, (0, 0, 255), -1)
        
        # 동영상 저장
        if record_mode:
            out.write(frame)
        
        # 화면 출력
        cv2.imshow('Camera', frame)
        cv2.imshow('Foreground Mask', fg_mask)  # 전경 마스크 표시
        
        key = cv2.waitKey(1)
        if key == 27:  # ESC 키를 누르면 종료
            break
        elif key == ord(' '):  # Space 키를 누르면 모드 전환
            record_mode = not record_mode
    
    # 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

