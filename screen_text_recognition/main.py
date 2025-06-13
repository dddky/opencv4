import pytesseract
import cv2
from mss import mss
import numpy as np
import screeninfo


def screen_text_recognition():
    try:
        pytesseract.pytesseract.tesseract_cmd = r'D:\pycharm\Tesseract\tesseract.exe'

        # 获取主显示器信息
        monitor = screeninfo.get_monitors()[0]
        capture_area = {
            "top": 0,
            "left": 0,
            "width": monitor.width,
            "height": monitor.height
        }

        # 创建窗口
        cv2.namedWindow("Screen Text Recognition", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Screen Text Recognition", 1600, 900)

        # 添加区域选择功能
        selection_active = False
        roi = None

        with mss() as sct:
            print("使用说明:")
            print("1. 按 's' 键进入区域选择模式")
            print("2. 用鼠标拖拽选择文本区域")
            print("3. 按 'c' 键捕获选中区域的文本")
            print("4. 按 'q' 键退出程序")

            while True:
                screenshot = sct.grab(capture_area)
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                display_img = img.copy()

                # 显示当前选择的ROI区域
                if roi:
                    x, y, w, h = roi
                    cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(display_img, "Selected Area", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

                elif key == ord("s"):
                    # 进入区域选择模式
                    selection_active = True
                    roi = cv2.selectROI("Screen Text Recognition", img, showCrosshair=False)
                    selection_active = False
                    print(f"已选择区域: {roi}")

                elif key == ord("c") and roi:
                    try:
                        x, y, w, h = roi
                        # 提取选中的ROI区域
                        roi_img = img[y:y + h, x:x + w]

                        # 图像预处理 - 关键优化步骤
                        gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
                        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                        # 使用优化配置进行OCR
                        custom_config = r'--oem 3 --psm 6'
                        text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')

                        print("\n" + "=" * 50)
                        print("捕获到的文本：\n")
                        print(text)
                        print("=" * 50)

                        # 在原始图像上显示结果
                        cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

                        # 显示识别的文本在图像上
                        y_position = y + h + 30
                        for i, line in enumerate(text.split('\n')):
                            if line.strip():
                                cv2.putText(display_img, line, (x, y_position + i * 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    except Exception as e:
                        print(f"OCR识别错误: {e}")
                        cv2.putText(display_img, f"OCR Error: {str(e)}", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow("Screen Text Recognition", display_img)

    except Exception as e:
        print(f"程序错误: {e}")
    finally:
        cv2.destroyAllWindows()


screen_text_recognition()
