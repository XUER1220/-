import cv2
import numpy as np
import sys
from flask import Blueprint, request, jsonify

photo_app = Blueprint('photo_app', __name__)

# 用于存储被选中人脸的索引
selected_faces = set()

# 用于存储人脸框的坐标
face_bboxes = []

# 照片保存的计数器
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

@photo_app.route('/save_image', methods=['POST'])
def save_image():
    # 直接保存当前显示的图像
    global save_counter, display_image
    save_path = f"assets/images/mosaic_{save_counter}.png"
    cv2.imwrite(save_path, display_image)
    print(f"图片已保存到 {save_path}")
    save_counter += 1
    return jsonify({'success': True, 'message': '图片保存成功'})

def process_image(image_path):
    """处理图像的函数"""
    global selected_faces, face_bboxes, save_counter, display_image

    # 加载图片
    image = cv2.imread(image_path)
    if image is None:
        print("无法加载图片，请检查路径是否正确。")
        return

    # 转换为灰度图，用于人脸检测
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 初始化人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 将人脸边界框存储到 face_bboxes 中
    face_bboxes = [(x, y, w, h) for (x, y, w, h) in faces]

    # 显示图片并绑定鼠标事件
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', on_mouse)

    while True:
        display_image = image.copy()

        # 绘制边界框
        for i, (x, y, w, h) in enumerate(face_bboxes):
            color = (0, 255, 0) if i in selected_faces else (0, 0, 255)
            cv2.rectangle(display_image, (x, y), (x + w, y + h), color, 2)

        # 应用马赛克到选中区域
        for i in selected_faces:
            display_image = apply_mosaic(display_image, face_bboxes[i])

        cv2.imshow('Image', display_image)

        key = cv2.waitKey(10) & 0xFF
        if key == 27:  # 按 ESC 退出
            break

        # 检查窗口是否被关闭
        if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
            break

    # 在窗口关闭时自动保存图像
    save_path = f"assets/images/mosaic_{save_counter}.png"
    cv2.imwrite(save_path, display_image)
    print(f"图片已自动保存到 {save_path}")

    cv2.destroyAllWindows()
    sys.exit(0)  # 退出程序

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process_image(sys.argv[1])  # 从命令行参数获取图片路径
    else:
        print("请提供图片路径作为命令行参数。")