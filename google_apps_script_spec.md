# 브레인시티 메디스파크 Google Apps Script 연동 명세서

## 1. 문서 목적

이 문서는 `브레인시티 메디스파크` 랜딩 페이지에서 수집한 상담 데이터를 `Google Apps Script`로 받아 `Google Sheets`에 저장하기 위한 구현 기준 문서다.

이 문서의 목표는 아래와 같다.

- 랜딩 페이지와 Apps Script의 데이터 연동 구조 정의
- POST 요청 데이터 형식 정의
- 시트 저장 로직 정의
- 성공 및 실패 응답 기준 정의
- 배포 및 운영 체크포인트 정리

---

## 2. 전체 연동 구조

전체 흐름은 아래와 같다.

1. 사용자가 랜딩 페이지에서 `상담하기` 버튼 클릭
2. 이름, 연락처, 개인정보 동의 입력
3. 랜딩 페이지가 Apps Script 웹앱 URL로 POST 요청 전송
4. Apps Script가 데이터 검증
5. Google Sheets에 한 줄 추가
6. 성공 응답 반환
7. 모바일은 전화 연결, 데스크톱은 완료 메시지 노출

---

## 3. 기본 운영 정보

- 대표번호: `010-6689-2348`
- 개발자명: `유희진`
- 구글 스프레드시트명: `YouDefine-Sales`
- 스프레드시트 ID: `1Lau4MMHfAn5DHy8JXjpOAhsdadtS9cRf-qEQiunUtX4`
- 웹앱 URL: `https://script.google.com/macros/s/AKfycbz0bnmeBCK8Pw72JurPzKH1rsEpcu5ngUDQdooVNx_TN4LsT3dJ56ctybZFsqvXsKZ8/exec`
- 저장 대상 탭: `medipark_leads`
- 기본 처리상태: `신규`
- 기본 문의유형: `상담신청`

---

## 4. Apps Script 역할

Apps Script는 아래 작업을 수행한다.

- 외부 POST 요청 수신
- 전달받은 값 검증
- 누락값 확인
- 시트 마지막 행에 데이터 추가
- 성공 또는 실패 결과 반환

---

## 5. 요청 방식

### 5-1. 요청 메서드

- `POST`

### 5-2. 콘텐츠 형식

권장:

- `application/json`

대안:

- `application/x-www-form-urlencoded`

1차 구현은 `JSON` 기준을 권장한다.

---

## 6. 요청 데이터 명세

랜딩 페이지에서 Apps Script로 아래 데이터를 전송한다.

```json
{
  "name": "홍길동",
  "phone": "01012345678",
  "developerName": "유희진",
  "managerPhone": "010-6689-2348",
  "pagePath": "/braincity-medipark",
  "buttonPosition": "hero_cta",
  "inquiryType": "상담신청",
  "interestType": "84A",
  "visitDate": "",
  "visitTime": "",
  "device": "mobile",
  "privacyAgreed": "Y"
}
```

---

## 7. 필드별 처리 기준

| 필드명 | 필수 여부 | 설명 | 처리 기준 |
|---|---|---|---|
| name | 필수 | 고객명 | 공백 제거 후 저장 |
| phone | 필수 | 고객 연락처 | 숫자만 추출 후 저장 |
| developerName | 필수 | 개발자명 | `유희진` 고정 |
| managerPhone | 필수 | 대표번호 | `010-6689-2348` 고정 |
| pagePath | 권장 | 유입 페이지 | 문자열 저장 |
| buttonPosition | 권장 | 버튼 위치 | 문자열 저장 |
| inquiryType | 권장 | 문의 유형 | 기본값 `상담신청` |
| interestType | 선택 | 관심 타입 | `84A`, `84B`, `101`, `상담 후 결정` |
| visitDate | 선택 | 방문 희망일 | 방문예약 선택 시 저장 |
| visitTime | 선택 | 방문 희망 시간대 | 방문예약 선택 시 저장 |
| device | 권장 | 기기 구분 | `mobile`, `desktop`, `tablet` |
| privacyAgreed | 필수 | 동의 여부 | `Y`만 허용 |

---

## 8. 서버 측 검증 규칙

Apps Script에서는 최소한 아래 검증을 수행한다.

### 필수 검증

- `name` 누락 여부
- `phone` 누락 여부
- `privacyAgreed` 값 확인

### 권장 검증

- `name` 2자 이상 여부
- `phone` 자릿수 확인
- `developerName`이 `유희진`인지 확인
- `managerPhone`이 `010-6689-2348`인지 확인

---

## 9. 시트 저장 컬럼 순서

Apps Script는 아래 순서로 시트에 값을 저장한다.

1. 접수일시
2. 이름
3. 연락처
4. 개발자명
5. 대표번호
6. 유입페이지
7. 버튼위치
8. 문의유형
9. 방문희망일
10. 방문희망시간
11. 디바이스
12. 개인정보동의여부
13. 처리상태
14. 메모

---

## 10. 저장값 매핑 규칙

| 시트 컬럼명 | 저장값 |
|---|---|
| 접수일시 | 서버 현재 시각 |
| 이름 | `name` |
| 연락처 | 정제된 `phone` |
| 개발자명 | `developerName` |
| 대표번호 | `managerPhone` |
| 유입페이지 | `pagePath` |
| 버튼위치 | `buttonPosition` |
| 문의유형 | `inquiryType` 또는 기본값 |
| 방문희망일 | `visitDate` |
| 방문희망시간 | `visitTime` |
| 디바이스 | `device` |
| 개인정보동의여부 | `privacyAgreed` |
| 처리상태 | `신규` |
| 메모 | 빈값 |

---

## 11. 성공 응답 형식

저장 성공 시 아래와 같은 JSON 응답을 권장한다.

```json
{
  "success": true,
  "message": "lead_saved",
  "phone": "010-6689-2348"
}
```

랜딩 페이지는 이 응답을 받아 아래처럼 처리한다.

- 모바일: `tel:010-6689-2348` 실행
- 데스크톱: 접수 완료 메시지 노출

---

## 12. 실패 응답 형식

저장 실패 시 아래 형식을 권장한다.

```json
{
  "success": false,
  "message": "invalid_request"
}
```

또는

```json
{
  "success": false,
  "message": "sheet_write_failed"
}
```

---

## 13. 오류 유형 정의

권장 오류 메시지 키:

- `invalid_request`
- `missing_name`
- `missing_phone`
- `privacy_required`
- `sheet_not_found`
- `sheet_write_failed`
- `internal_error`

랜딩 페이지에서는 이 오류를 사용자 친화적으로 바꿔서 보여준다.

예시:

- `일시적으로 접수가 원활하지 않습니다. 대표번호 010-6689-2348로 바로 연락 부탁드립니다.`

---

## 14. Apps Script 구현 권장 함수

권장 함수 구성:

- `doGet()`
- `doPost(e)`
- `parseRequestBody(e)`
- `validateLead(data)`
- `normalizePhone(phone)`
- `appendLeadRow(sheet, data)`
- `jsonResponse(payload)`

---

## 15. 구현 로직 순서

### doGet 기본 흐름

웹앱 URL을 브라우저에서 직접 열었을 때 `doGet` 오류나 개발자용 JSON이 보이지 않도록 상태 확인용 안내 화면을 반환한다.

```javascript
function doGet() {
  return HtmlService
    .createHtmlOutput('상담 접수 시스템이 정상 연결되었습니다.')
    .setTitle('Real-Sales 상담 접수 시스템');
}
```

### doPost 기본 흐름

1. 요청 본문 읽기
2. JSON 파싱
3. 필수값 검증
4. 전화번호 정제
5. 시트 객체 조회
6. 새 행 추가
7. 성공 응답 반환

### 실패 시

1. 예외 감지
2. 오류 키 반환
3. 로그 기록

---

## 16. 예시 의사코드

```javascript
function doPost(e) {
  try {
    const data = parseRequestBody(e);
    const validation = validateLead(data);

    if (!validation.success) {
      return jsonResponse({
        success: false,
        message: validation.message
      });
    }

    const sheet = SpreadsheetApp
      .openById('1Lau4MMHfAn5DHy8JXjpOAhsdadtS9cRf-qEQiunUtX4')
      .getSheetByName('medipark_leads');
    const now = new Date();
    const phone = normalizePhone(data.phone);

    sheet.appendRow([
      now,
      data.name.trim(),
      phone,
      '유희진',
      '010-6689-2348',
      data.pagePath || '',
      data.buttonPosition || '',
      data.inquiryType || '상담신청',
      data.interestType || '',
      data.visitDate || '',
      data.visitTime || '',
      data.device || '',
      'Y',
      '신규',
      ''
    ]);

    return jsonResponse({
      success: true,
      message: 'lead_saved',
      phone: '010-6689-2348'
    });
  } catch (error) {
    return jsonResponse({
      success: false,
      message: 'internal_error'
    });
  }
}
```

---

## 17. 시트 준비 절차

1. 구글시트 생성
2. 시트 이름을 `medipark_leads`로 설정
3. 1행에 컬럼 헤더 입력
4. Apps Script 연결
5. 웹앱으로 배포

---

## 18. 웹앱 배포 기준

권장 배포 방식:

- 웹앱으로 배포
- `누구나 접근 가능` 또는 운영 정책에 맞는 접근 범위 설정

주의:

- 실제 운영 시 외부 요청 허용 범위를 검토해야 한다.
- 필요하면 간단한 토큰 검증을 추가할 수 있다.

---

## 19. 보안 및 운영 체크포인트

- 개인정보는 최소 항목만 수집한다.
- 로그에 민감정보를 과도하게 남기지 않는다.
- 스팸 요청 방지를 위해 추후 토큰 또는 referrer 체크를 고려할 수 있다.
- 테스트 시트와 운영 시트를 분리하는 것이 좋다.

---

## 20. 1차 버전 범위

이번 1차 버전에서는 아래까지만 구현한다.

- 이름 저장
- 연락처 저장
- 개발자명 `유희진` 자동 저장
- 대표번호 `010-6689-2348` 자동 저장
- 기본 유입정보 저장
- 모바일 제출 후 전화 연결

---

## 21. 2차 확장 가능 항목

추후 아래 항목을 추가할 수 있다.

- `utm_source`
- `utm_medium`
- `utm_campaign`
- 관심 타입
- 방문 희망일시
- 상담 희망 시간
- 중복 리드 감지
- 문자 알림 자동화

---

## 22. 최종 요약

Apps Script는 랜딩 페이지 상담 폼의 백엔드 역할을 수행한다.

필수 구현 조건은 아래와 같다.

- POST 요청 수신
- 이름, 연락처, 동의 여부 검증
- 개발자명 `유희진` 자동 기록
- 대표번호 `010-6689-2348` 자동 기록
- 구글시트 행 추가 저장
- 성공 시 전화 연결에 사용할 응답 반환

이 기준으로 구현하면 랜딩 페이지, 고객 DB, 상담 운영 흐름이 안정적으로 연결된다.
