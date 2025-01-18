import cv2
import mediapipe as mp
import numpy as np
import sys



# 用于存储被选中人脸的索引
selected_faces = set()

# 用于存储当前帧中的人脸框
face_bboxes = []

save_counter = 1

def on_mouse(event, x, y, flags, param):
    """鼠标事件回调函数，用于选择或取消人脸"""
    global selected_faces, face_bboxes
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (bx, by, bw, bh) in enumerate(face_bboxes):
            if bx <= x <= bx + bw and by <= y <= by + bh:
                if i in selected_faces:
                    selected_faces.remove(i)  # 取消选中
                else:
                    selected_faces.add(i)  # 添加选中
                print(f"人脸 {i} 的选中状态被更新: {i in selected_faces}")
                break

def apply_mosaic(image, bbox):
    """对指定区域应用马赛克"""
    x, y, w, h = bbox
    face_region = image[y:y + h, x:x + w]
    small = cv2.resize(face_region, (0, 0), fx=0.1, fy=0.1)  # 缩小 10%
    mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)  # 放大回原尺寸
    image[y:y + h, x:x + w] = mosaic
    return image

# 加载视频
video_path = sys.argv[1]  # 从命令行参数获取视频路径
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("无法加载视频，请检查路径是否正确。")
    exit()

# 获取视频的帧率、宽度和高度
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 设置视频保存的输出路径
output_path = "assets/videos/output_video.mp4"  # 输出路径
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码格式
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))  # 初始化视频写入对象

# 初始化 MediaPipe 人脸检测器
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cv2.namedWindow('A')
cv2.setMouseCallback('A', on_mouse)

while True:
    ret, frame = cap.read()
    if not ret:
        print("视频播放结束或无法读取帧。")
        break

    # 调整帧的大小以适应窗口
    frame = cv2.resize(frame, (640, 360))  # 调整为适中的尺寸

    # 转换为 RGB 格式，因为 MediaPipe 使用 RGB 图像
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    # 如果检测到人脸
    if results.detections:
        face_bboxes = []
        for detection in results.detections:
            # 获取每个人脸的边界框坐标
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            face_bboxes.append((x, y, w, h))

        # 默认所有人脸都打码
        if not selected_faces:
            selected_faces = set(range(len(face_bboxes)))

        # 更新 selected_faces，确保它只包含当前帧中的有效索引
        selected_faces = {i for i in selected_faces if i < len(face_bboxes)}

        # 显示当前帧
        display_frame = frame.copy()

        # 绘制边界框
        for i, (x, y, w, h) in enumerate(face_bboxes):
            color = (0, 255, 0) if i in selected_faces else (0, 0, 255)
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), color, 2)

        # 对选中的区域应用马赛克
        for i in selected_faces:
            display_frame = apply_mosaic(display_frame, face_bboxes[i])

        # 显示当前帧
        cv2.imshow('A', display_frame)

        # 将修改后的帧写入输出视频
        out.write(display_frame)

    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # 按 ESC 退出
        break
    elif key == ord('s'):  # 按 S 键保存视频
        out.release()  # 释放当前视频写入对象
        save_counter += 1
        output_path = f"assets/videos/output_video_{save_counter}.mp4"
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        print(f"视频已保存到 {output_path}")

cap.release()
out.release()  # 释放视频写入对象
cv2.destroyAllWindows()

print(f"修改后的视频已保存到 {output_path}")