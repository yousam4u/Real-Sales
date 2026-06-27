const SPREADSHEET_ID = '1Lau4MMHfAn5DHy8JXjpOAhsdadtS9cRf-qEQiunUtX4';
const SHEET_NAME = 'medipark_leads';
const DEVELOPER_NAME = '유희진';
const MANAGER_PHONE = '010-6689-2348';
const DEFAULT_INQUIRY_TYPE = '상담신청';
const DEFAULT_STATUS = '신규';

function doGet() {
  return HtmlService
    .createHtmlOutput(`
      <!doctype html>
      <html lang="ko">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Real-Sales 상담 접수 시스템</title>
          <style>
            body {
              margin: 0;
              min-height: 100vh;
              display: grid;
              place-items: center;
              background: linear-gradient(135deg, #0f2f33, #15494f 55%, #e7c36f);
              color: #f8f4e8;
              font-family: Arial, sans-serif;
            }
            .card {
              width: min(92vw, 520px);
              padding: 42px;
              border: 1px solid rgba(255, 255, 255, 0.28);
              border-radius: 28px;
              background: rgba(8, 28, 31, 0.72);
              box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
              text-align: center;
            }
            .eyebrow {
              color: #e7c36f;
              font-size: 13px;
              font-weight: 700;
              letter-spacing: 0.18em;
              text-transform: uppercase;
            }
            h1 {
              margin: 16px 0 12px;
              font-size: clamp(28px, 6vw, 42px);
              line-height: 1.16;
            }
            p {
              margin: 0;
              color: rgba(248, 244, 232, 0.82);
              font-size: 17px;
              line-height: 1.7;
            }
            .status {
              display: inline-flex;
              align-items: center;
              gap: 8px;
              margin-top: 26px;
              padding: 11px 16px;
              border-radius: 999px;
              background: rgba(231, 195, 111, 0.18);
              color: #ffe4a3;
              font-weight: 700;
            }
          </style>
        </head>
        <body>
          <main class="card">
            <div class="eyebrow">Real-Sales</div>
            <h1>상담 접수 시스템이 정상 연결되었습니다</h1>
            <p>브레인시티 메디스파크 상담 신청 데이터는<br>구글시트 <strong>${SHEET_NAME}</strong> 탭으로 저장됩니다.</p>
            <div class="status">정상 작동 중</div>
          </main>
        </body>
      </html>
    `)
    .setTitle('Real-Sales 상담 접수 시스템');
}

function doPost(e) {
  try {
    const data = parseRequestBody(e);
    const validation = validateLead(data);

    if (!validation.success) {
      return jsonResponse({
        success: false,
        message: validation.message,
      });
    }

    const sheet = getLeadSheet();
    const now = formatDate(new Date());
    const normalizedPhone = normalizePhone(data.phone);

    sheet.appendRow([
      now,
      data.name.trim(),
      normalizedPhone,
      DEVELOPER_NAME,
      MANAGER_PHONE,
      data.pagePath || '',
      data.buttonPosition || '',
      data.inquiryType || DEFAULT_INQUIRY_TYPE,
      data.interestType || '',
      data.visitDate || '',
      data.visitTime || '',
      data.device || '',
      'Y',
      DEFAULT_STATUS,
      '',
    ]);

    return jsonResponse({
      success: true,
      message: 'lead_saved',
      phone: MANAGER_PHONE,
    });
  } catch (error) {
    return jsonResponse({
      success: false,
      message: 'internal_error',
      detail: String(error),
    });
  }
}

function parseRequestBody(e) {
  if (!e || !e.postData || !e.postData.contents) {
    throw new Error('empty_post_data');
  }

  return JSON.parse(e.postData.contents);
}

function validateLead(data) {
  if (!data || typeof data !== 'object') {
    return { success: false, message: 'invalid_request' };
  }

  const name = String(data.name || '').trim();
  const phone = normalizePhone(String(data.phone || ''));
  const privacyAgreed = String(data.privacyAgreed || '').toUpperCase();
  const developerName = String(data.developerName || '').trim();
  const managerPhone = String(data.managerPhone || '').trim();

  if (!name) {
    return { success: false, message: 'missing_name' };
  }

  if (name.length < 2) {
    return { success: false, message: 'invalid_name' };
  }

  if (!phone) {
    return { success: false, message: 'missing_phone' };
  }

  if (phone.length < 10 || phone.length > 11) {
    return { success: false, message: 'invalid_phone' };
  }

  if (privacyAgreed !== 'Y') {
    return { success: false, message: 'privacy_required' };
  }

  if (developerName && developerName !== DEVELOPER_NAME) {
    return { success: false, message: 'invalid_developer_name' };
  }

  if (managerPhone && managerPhone !== MANAGER_PHONE) {
    return { success: false, message: 'invalid_manager_phone' };
  }

  return { success: true };
}

function normalizePhone(phone) {
  return String(phone || '').replace(/\D/g, '');
}

function getLeadSheet() {
  const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_NAME);

  if (!sheet) {
    throw new Error('sheet_not_found');
  }

  return sheet;
}

function formatDate(date) {
  return Utilities.formatDate(date, 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss');
}

function jsonResponse(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
