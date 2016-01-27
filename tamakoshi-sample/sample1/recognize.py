# -*- coding: utf-8 -*-
import cv2

# 顔正面の分類器
cascade_path = "./haarcascade_frontalface_default.xml"
image_path = "./sample-bijo.jpg"

color = (255, 255, 255)
image = cv2.imread(image_path)

# グレースケール変換
image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)

# カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

# 物体認識（顔認識）の実行
# image        - CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
# objects      - 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
# scaleFactor  – 各画像スケールにおける縮小量を表します
# minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
# flags        – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
# minSize      – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
print("face rectangle")

if len(facerect) > 0:
  # 検出した顔を囲む矩形の作成
  for rect in facerect:
    cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
  # 認識結果の保存
  cv2.imwrite("detected.jpg", image)