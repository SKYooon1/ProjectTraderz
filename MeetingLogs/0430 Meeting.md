### 주요 주제
- 면역 기능과 외부 환경의 중요성
- 이동 평균선 구현과 증권사 API 활용
- 조건 인식과 실시간 데이터 처리
- 강화 학습과 게임 마켓 창조

### 다음 할 일
- 실시간 조건 인식 적용 방법 모색
- 강화 학습 툴 학습 후 백테스팅 진행
- 증권사 API를 이용한 이동 평균선 구현
- 외부 파일로 주문 품목 연결 방법 개발

### 요약
- 면역 기능의 중요성
    - 몸이라는 거는 외부로부터 침입하는 적 병균도 될 수 있고 독소도 될 수 있고 이런 거에 대해서 방어할 수 있는 면역 기능이라는 게 있음
    - 어렸을 때부터 부모님들이 너무 깨끗하게만 키워서 면역 기능이 생길 기회가 없었던 것 같음
    - 아기를 낳아도 외부 환경에 접촉할 수 있는 기회 자체가 없기 때문에 적당하게 외부 도전에 대응하고 살아야 감기도 안 걸림
- 셀레늄의 활용
    - 이동 평균선 구현하는 것까지 해보겠다고 해서 지원이가 이동 평균선 책에 있는 내용 말고 이것저것 다 찾아보고 저는 책 위주로 정독하면서 따라가 봤는데 확실히 책에 있는 내용이 오류 같은 게 없이 잘 나옴
    - 셀레늄은 데이터 컬렉션하는 하나의 한 도구일 뿐이고 다른 방법도 많으니까 셀레늄 한번 써보라고 함
- 증권사 API를 이용한 이동 평균선 만들기
    - 증권사의 API를 이용해서 자료를 갖고 와서 이동 평균선을 만들어보는 것까지 해보라고 함
    - 증권사들이 조만간 바꿀 것 같지는 않아서 그걸로 할 수 있는 거는 빌딩 주문 냈다가 하는 것밖에 없음
    - 학습시킨 결과로 주문을 낼 때 안 낼 때 주문 낼 품목들 같은 거를 외부 파일로 만들어 놨다가 보철 임바리먼트 환경 안으로 파일을 던져놓으면 32비트짜리가 그걸 읽어서 할 수 있게 연결할 수 있는 방법을 찾아보라고 함
- 한투, 키움증권, 대신증권
    - 한투는 32비트이기 때문에 64비트에서는 할 수가 없음
    - 키움이나 대신증권 같은 데는 32m라 제한이 되게 많음
    - 한투로 하는 것이 나을 것 같음
    - 조건 인식을 파이썬에 적용하는 것을 해보고 잘 되면 실시간으로 받아오는 걸로 해야 됨
- 강화 학습을 통한 백테스팅
    - 강화 학습 툴에 강화 학습을 공부를 많이 해야 되지만 일단 최종 발표 때까지는 전부 강화 학습으로 백테스팅을 해서 학습을 시킨 다음에 하는 게 좋겠다 함
    - 강화 학습을 해서 어떤 스트레티지를 넣을 거냐는 아직 정하지 못했지만 13일날 발표는 강화 학습을 더 집어넣는 게 목표임
- 게임 안에 있는 마켓
	- 게임 안에 있는 마켓은 경쟁적인 마켓이 아님
    - 수요 공급에 따라서 가격이 변동되는 마켓 정도는 있음
    - 게임 안에 있는 마켓을 창조할 수 있고 만들어 갈 수 있음
