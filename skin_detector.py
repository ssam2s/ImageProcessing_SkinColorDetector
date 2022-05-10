# 필요한 패키지를 import함
from __future__ import print_function
import argparse
import numpy as np
import cv2

def histogram_slicing(img, lowerb, upperb):
	mask = cv2.inRange(img, lowerb, upperb)
	blur = cv2.GaussianBlur(img, (5, 5), 0)
	dst = cv2.bitwise_and(blur, blur, mask=mask)
	return dst

if __name__ == '__main__' :
	# 명령행 인자 처리
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", required = False, \
		help = "path to the video file")
	args = vars(ap.parse_args())

	fvideo = args.get("video")

	# OpenCV를 사용하여 영상 데이터 로딩
	if fvideo is None:
		camera = cv2.VideoCapture(0)
	else:
		camera = cv2.VideoCapture(args["video"])

	lowerb = np.array([0, 48, 80])
	upperb = np.array([20, 255, 255])

	while True:
		# 현재 프레임 획득
		#  frame: 획득한 비디오 프레임
		#  retfal: 프레임 획득이 되지 못하면 False
		(retval, frame) = camera.read()
	 
		# 비디오 파일의 마지막 위치 도착 확인
		if fvideo is not None and not retval:
			break
	 
		# HSV 칼라 모델로 변환한 후에 피부 영역 검출
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		dst = histogram_slicing(hsv, lowerb, upperb)
		skin = cv2.cvtColor(dst, cv2.COLOR_HSV2BGR)

		# 결과 영상 출력
		cv2.imshow("images", np.hstack([frame, skin]))
	 
		# 'q' 키를 누르면 종료
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	 
	# 비디오 카메라 정리
	camera.release()