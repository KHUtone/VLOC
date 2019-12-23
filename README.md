# VLOC
- VLOG + Compiler
- 2019/11/8 경희대학교 해커톤
- 우수상 수여

### Member
- 정의동 : Android app 개발
- 김원규 : video model 학습 
- 윤준석 : 자동 자막 생성
- 유명현 : aws architecture setting

### Motivation
- 여행과정에서 발생하는 여러가지 상황에서 미처 사진을 찍지 못해서 아쉬운 순간이 많다.
- VLOG를 직접 만들기에는 시간도 없고 제대로 구색을 맞추려면 많은 시간을 필요로 하는 편집과정이 필요하다.
- 자막이 존재해야 더 많은 인기를 얻을 수 있는데, 이 또한 편집으로 생성하기 매우 어렵다.

=> 자동으로 이 과정을 수행해주면 편리하지 않을까??

### Goal
- 무분별하게 들어오는 여행 Video data를 자동으로 편집하여 하나의 짧은 vlog를 생성해주는 application.

### Architecture

![architecture](/src/img/architecture.png)

1. 영상업로드
2. 업로드했다고 알림
3. 편집할 영상 다운
4. 편집한 영상 업로드
5. 업로드 했다고 알림
6. 최종 영상 다운

### Result

- 사용자가 지정한 가중치 지수 미만인 부분을 잘라 vlog를 만들어준다. 
- 자막 자동 생성.
