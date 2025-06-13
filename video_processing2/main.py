import cv2
import numpy as np
import pyautogui
import time

def video_processing():
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕分辨率：{screen_width}x{screen_height}")

    capture_width = screen_width // 2
    capture_height = screen_height // 2
    capture_area = (0, 0, capture_width, capture_height)
    print(f"捕获区域：{capture_width}x{capture_height}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        'output/screen_recording.mp4',
        fourcc,
        15.0,
        (capture_width, capture_height)
    )

    frame_count = 0
    last_time = time.time()

    window_name = "Screen + Edges"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    window_width = capture_width * 2
    window_height = capture_height

    window_x = screen_width - window_width
    window_y = screen_height - window_height
    cv2.moveWindow(window_name, window_x, window_y)
    cv2.resizeWindow(window_name, window_width, window_height)
    print("开始捕捉！操作说明：")
    print("-按'q'键退出程序")
    print("-按's'键保存当前帧")

    while True:
        screenshot = pyautogui.screenshot(region=capture_area)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        frame_count += 1

        current_time = time.time()
        fps = 1/(current_time - last_time)
        last_time = current_time

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        cv2.putText(frame, f"帧：{frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"FPS：{fps:.1f}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, "按'q'退出|按's'保存", (10, capture_height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        combined = np.hstack((frame, edges_bgr))

        cv2.imshow(window_name, combined)

        out.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(f'output/screenshot_{frame_count}.png', frame)
            cv2.imwrite(f'output/edges_{frame_count}.png', edges)
            print(f"已保存第{frame_count}帧")

    out.release()
    cv2.destroyAllWindows()
    print(f"处理完成！共处理{frame_count}帧")

video_processing()
