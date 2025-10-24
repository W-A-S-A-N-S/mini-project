# 🎮 Steam Party Matcher - 협동 게임 파티 매칭 시스템

## 📋 프로젝트 개요
Steam의 협동 게임을 함께 플레이할 파티원을 찾아주는 매칭 플랫폼입니다.
게임별로 파티를 생성하고, 플레이 스타일과 시간대가 맞는 플레이어들을 매칭해줍니다.

## 🚀 주요 기능
- **파티 생성/참가**: 원하는 게임의 파티를 생성하거나 기존 파티에 참가
- **게임 카탈로그**: 인기 협동 게임 목록 및 상세 정보
- **실시간 매칭**: 플레이 가능 시간, 실력, 플레이 스타일 기반 매칭
- **유저 프로필**: Steam ID 연동, 선호 게임, 플레이 통계
- **채팅 시스템**: 파티원들과의 실시간 소통

## 🛠 기술 스택
### Backend
- Django REST Framework
- SQLite (개발용)
- Django CORS Headers
- Simple JWT (인증)

### Frontend
- React 18
- Axios (API 통신)
- React Router (라우팅)
- Tailwind CSS (스타일링)

## 📦 설치 및 실행 방법

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend 설정
```bash
# 1. backend 디렉토리로 이동
cd backend

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 5. 초기 데이터 생성 (선택사항)
python manage.py loaddata initial_data.json

# 6. 관리자 계정 생성
python manage.py createsuperuser

# 7. 서버 실행
python manage.py runserver
```

### Frontend 설정
```bash
# 1. frontend 디렉토리로 이동
cd frontend

# 2. 패키지 설치
npm install

# 3. 개발 서버 실행
npm start
```

### 접속 정보
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

## 📁 프로젝트 구조
```
steam-party-matcher/
├── backend/
│   ├── config/           # Django 프로젝트 설정
│   ├── api/             # API 앱
│   ├── games/           # 게임 관련 앱
│   ├── parties/         # 파티 관련 앱
│   ├── users/           # 사용자 관련 앱
│   └── requirements.txt
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/   # 재사용 가능한 컴포넌트
    │   ├── pages/       # 페이지 컴포넌트
    │   ├── services/    # API 서비스
    │   ├── utils/       # 유틸리티 함수
    │   └── App.js
    └── package.json
```

## 🎯 API 엔드포인트

### 인증
- `POST /api/auth/register/` - 회원가입
- `POST /api/auth/login/` - 로그인
- `POST /api/auth/refresh/` - 토큰 갱신

### 게임
- `GET /api/games/` - 게임 목록
- `GET /api/games/{id}/` - 게임 상세

### 파티
- `GET /api/parties/` - 파티 목록
- `POST /api/parties/` - 파티 생성
- `GET /api/parties/{id}/` - 파티 상세
- `POST /api/parties/{id}/join/` - 파티 참가
- `POST /api/parties/{id}/leave/` - 파티 나가기

### 사용자
- `GET /api/users/profile/` - 프로필 조회
- `PUT /api/users/profile/` - 프로필 수정

## 📸 스크린샷
(프로젝트 완성 후 스크린샷 추가 예정)

## 🤝 Contributing
Pull requests are welcome!

## 📄 License
MIT License