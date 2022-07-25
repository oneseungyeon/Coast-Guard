## 연구 내용
해양 내 불법선박 대응을 위해 유인항공기으로 촬영한 영상으로부터 OCR, 딥러닝을 통해 선박과 유의미한 객체를 탐지하고 이의 위치정보를 DB화하여 추후 불법선박을 대응하는 체계에 있어 도움이 되고자 하는 프로젝트

## 연구 과정

<img src = "https://user-images.githubusercontent.com/74392995/180744893-713fc0e9-f1b7-444e-a9d5-ce071fed9eea.png" width = "80%" height = "40%">

1. 동영상에서 프레임을 추출하여 OCR을 이용해 EO와 IR 영상으로 구분
2. EO 영상 내 딥러닝을 이용해 선박, 선원, 국기를 탐지
3. 유의미한 객체 탐지 후 이의 위치정보를 OCR로 추출 후 보정을 거쳐 최종 위치정보 가공
4. 객체와 위치 정보를 DB로 구축

## 딥러닝 모델

<img src = "https://user-images.githubusercontent.com/74392995/180745596-054e2805-7c9f-4a89-a548-52d2148f6e92.png" width = "50%" height = "40%">

1. mmdetection에서 제공하는 VFNet 모델을 이용
2. VFNet은 새로운 손실 함수와 bbox 탐지 방안을 제안해 성능 향상 도모

## 평가 결과

1. 평가 지표
* mAP : 신뢰성(confidence)에 	대한 임곗값의 변화에 따른 정밀도-재현율 그래프로부터 계산한 객체 클래스별 평	균 정밀도(Average Precision)를 객체 클래스 개수로 나눈 값
2. 평가 데이터셋

<img src = "https://user-images.githubusercontent.com/74392995/180769884-69dceb96-3285-4675-bed2-5350f36d1543.png" width = "50%" height = "40%">

* 항공단에서 촬영한 유인항공영상으로 학습을 위해 라벨링을 거쳐 선박 2977건, 선원 761건, 국기 502건의 학습 데이터 구축
3. 평가 결과

<img src = "https://user-images.githubusercontent.com/74392995/180770365-fca62cac-3222-4aa9-be95-ce77ff3a8ecd.png" width = "60%" height = "40%">

선박은 89.2mAP, 선원 국기는 51.1mAP로 학습 데이터의 부족으로 성능 저하 현상 발생

## 결론
1. 향후 추가 데이터셋 구축 필요
2. 추가 학습으로 성능향상 도모 시 추후 해양 영상 내 선박 분석을 효과적으로 수행 가능으로 기대
