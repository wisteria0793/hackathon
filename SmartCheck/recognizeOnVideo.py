from ultralytics import YOLO
import ffmpeg
import numpy as np
import cv2

# YOLOモデルをロード
model = YOLO("yolo11n.pt")  # モデルのパスを指定

# RTSPストリームのURL
rtsp_url = "rtsp://wisteria07930791@gmail.com:H9hez3bQ@192.168.10.121:554/stream1"

# FFmpegでRTSPストリームを取得
process = (
    ffmpeg
    .input(rtsp_url)
    .output('pipe:', format='rawvideo', pix_fmt='bgr24')
    .run_async(pipe_stdout=True)
)

# 解像度を設定（カメラの解像度に応じて調整）
frame_width = 1920
frame_height = 1080
frame_count = 0

while True:
    # フレームデータを取得
    in_bytes = process.stdout.read(frame_width * frame_height * 3)
    if not in_bytes:
        break

    # フレームをNumPy配列に変換
    frame = np.frombuffer(in_bytes, np.uint8).reshape([frame_height, frame_width, 3])
    
    # フレームスキップ（2フレームに1回推論）
    frame_count += 1
    if frame_count % 2 == 0:
        continue

    # フレームをYOLOモデルに渡して推論
    results = model(frame)

    # 推論結果を描画したフレームを取得
    annotated_frame = results[0].plot()

    # 映像を表示
    cv2.imshow("YOLO Detection", annotated_frame)

    # 'q'キーが押されたら終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# プロセスとリソースを解放
process.stdout.close()
cv2.destroyAllWindows()
