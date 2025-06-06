User Guide






과목명: 오픈소스SW기초 3분반

담당교수: 송인식 교수님

소속학과/학번/이름: 

소프트웨어학과/32220669/김민준

소프트웨어학과/32223871/임형운

소프트웨어학과/32241009/김은솔

소프트웨어학과/32220572/김민관

 
목차
1. 서론
2. 설치 및 실행 방법


      2.1 사전 준비

      2.2 파일 구조

      2.3 실행 방법

3. 주요 기능 안내
   
      3.1 메인 화면

      3.2 나만의 냉장고

      3.3레시피 추천

      3.4 유통기한 알림

4. 데이터 저장 및 보존
5. 사용상 주의 및 팁
   
 


1.서론
  현대 사회에서는 바쁜 일상과 계획 부재로 인해 식재료의 유통기한을 놓치거나,
  냉장고 속에 어떤 재료가 있는지 잊고 재료를 낭비하는 일이 빈번하게 발생합니다.
  특히 대학생이나 1인 가구의 경우, 남은 재료로 어떤 요리를 해야 할지 고민하다가
  결국 외식을 택하는 경우도 많습니다.
  My Recipe Mate는 이러한 현실적인 문제를 해결하기 위해
  사용자가 보유한 식재료를 체계적으로 디지털화하여 관리하고,
  유통기한 정보를 함께 기록하며,
  현재 가진 재료나 원하는 요리명을 바탕으로 레시피를 자동 추천해 주는  
  데스크탑 기반 애플리케이션입니다.
  이 프로그램은 단순히 재료를 기록하는 것을 넘어
  유통기한 임박 재료 경고,
  실시간 웹 크롤링을 통한 다양한 레시피 추천하는 기능이 있습니다.

2.설치 및 실행 방법
  My Recipe Mate는 Python 기반 데스크탑 기반 애플리케이션으로 설치 및 실행 방법은 다음과 같습니다.
  
    2.1 사전준비
      Python 3.x 환경이 필요합니다. 이 프로젝트는 다양한 외부 라이브러리를 활용하므로, 다음 명령어로 필수 라이브러리를 설치해야 합니다.다음 명령어로 필수 라이브러리를 설치해야       합니다.
      Pip install requests beautifulsoup4 pillow
      (tkinter는 별도 설치 없이 Python에 내장되어 있습니다.)


    2.2 파일 구조
      아래와 같이 프로젝트 루트 폴더에 필요한 파일이 모두 포함되어야 정삭적으로 작동합니다. 
        project/
        ├── main.py
        ├── fridge.py
        ├── searchIngredient.py
        ├── recipe_crawler.py
        ├── ingredientRecommend.py
        ├── ingredients_master.json    #사전에 제공된 재료 목록(검색 및 추천에 활용, 반드시 포함)
        └── ingredients.json           #사용자가 프로그램을 실행하면서 추가하는 재료 정보 저장 파일
        
    2.3 실행 방법
      Main.py를 본인의 환경에서 python을 실행시킬 수 있는 프로그램을 사용합니다.

3. 주요 기능 안내
   
      3.1 메인화면
   
          프로그램 실행 시,
   
          •	‘레시피 추천’과 ‘나만의 냉장고’ 두 가지 주요 기능이 카드 형태로 표시됩니다.
   
          •	상단에는 요리명 입력창, 하단에는 임박 재료 알림이 표시되어
          사용자는 직관적으로 원하는 기능에 접근할 수 있습니다.
   
      3.2 나만의 냉장고 (재료 관리 기능)
   
          •‘나만의 냉장고’ 메뉴에서는 내가 보유한 재료의 이름, 유통기한, 수량을 한눈에 관리할 수 있습니다.
   
          •	재료 추가:
   
          o+ 버튼 클릭 → 재료명 검색 및 선택 → 유통기한(YYYY-MM-DD) 입력
   
          •	재료 수정/삭제:
   
          o	수량 수정 및 삭제 기능 제공
   
          o	임박 재료는 색상 강조(노란색, 빨간색 등)로 쉽게 확인 가능
   
          •	스크롤 및 편의 기능:
   
          o	재료가 많을 경우 마우스 휠로 스크롤 가능
   
          •	최근 재료 재등록:
   
          o	최근에 추가한 재료를 검색창 상단에서 바로 선택할 수 있습니다.

      3.3 레시피 추천 기능
   
          •	요리명 검색:
   
          o	메인화면 상단 입력창에 원하는 요리명을 입력 후 검색(🔍)
   
          → 관련 레시피(이미지, 제목, 자세히 보기) 리스트 팝업
   
          •	재료 기반 추천:
   
          o	‘레시피 추천’ 메뉴 클릭 → 내 냉장고 재료 선택을 클릭 -> 내가 가진 재료(여러 개 선택)
   
          → 추천 레시피 보기를 클릭 -> 원화는 레시피를 클릭
   
          o	추천 레시피는 웹에서 실시간 크롤링하여, 이미지·제목·링크와 함께 표시
      
      3.4 유통기한 알림
   
          •	메인화면 하단에서,
   
            유통기한 7일 이내의 임박 재료가 경고 아이콘(⚠️)과 함께 자동으로 표시됩니다.
   
          •	냉장고 화면에서도 임박 재료가 색상 강조로 한눈에 구분됩니다.

5. 데이터 저장 및 보존

  •	자동 저장:
  
    o	모든 재료 정보는 사용자가 추가, 수정, 삭제할 때마다
    
    ingredients.json 파일에 자동 저장됩니다.
   
  •	영구 보존:
  
    o	프로그램을 껐다 켜도 데이터가 유지되므로,
    
    사용자는 재등록 없이 언제든 이어서 사용할 수 있습니다.
    
  •	재료 마스터 파일:
  
    o	ingredients_master.json을 통해 다양한 재료명을 손쉽게 검색할 수 있습니다.



5. 사용 팁 및 FAQ
   
  •	유통기한 입력:
  
    o	날짜는 반드시 YYYY-MM-DD 형식(예: 2024-06-10)으로 입력하세요.
   
  •	재료 수량:
  
    o	+, - 버튼으로 쉽게 조절, 필요시 삭제 버튼으로 제거
    
  •	인터넷 연결:
  
    o	레시피 추천 및 이미지 기능은 인터넷 연결이 필요합니다.
