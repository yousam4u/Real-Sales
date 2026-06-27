import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = path.resolve("outputs/youdefine-sales");
const outputPath = path.join(outputDir, "YouDefine-Sales.xlsx");

const headers = [
  "접수일시",
  "이름",
  "연락처",
  "개발자명",
  "대표번호",
  "유입페이지",
  "버튼위치",
  "문의유형",
  "관심타입",
  "방문희망일",
  "방문희망시간",
  "디바이스",
  "개인정보동의여부",
  "처리상태",
  "메모",
];

const sampleRow = [
  "2026-06-27 16:20:15",
  "홍길동",
  "01012345678",
  "유희진",
  "010-6689-2348",
  "/braincity-medipark",
  "hero_cta",
  "방문예약",
  "84A",
  "2026-07-01",
  "오후 2시 이후",
  "mobile",
  "Y",
  "신규",
  "예시 행입니다. 운영 시작 전 삭제해도 됩니다.",
];

const workbook = Workbook.create();
const leads = workbook.worksheets.add("medipark_leads");
leads.showGridLines = false;

leads.getRange("A1:O1").values = [headers];
leads.getRange("A2:O2").values = [sampleRow];

leads.getRange("A1:O1").format.fill = { color: "#0A4F57" };
leads.getRange("A1:O1").format.font = { color: "#FFFFFF", bold: true };
leads.getRange("A1:O1").format.borders = { preset: "outside", style: "thin", color: "#0A4F57" };
leads.getRange("A2:O200").format.fill = { color: "#FFFFFF" };
leads.getRange("A1:O200").format.borders = { preset: "inside", style: "thin", color: "#E1E7EA" };
leads.getRange("A1:O200").format.wrapText = true;
leads.getRange("A:A").format.columnWidthPx = 150;
leads.getRange("B:B").format.columnWidthPx = 95;
leads.getRange("C:C").format.columnWidthPx = 125;
leads.getRange("D:E").format.columnWidthPx = 120;
leads.getRange("F:G").format.columnWidthPx = 150;
leads.getRange("H:I").format.columnWidthPx = 110;
leads.getRange("J:K").format.columnWidthPx = 130;
leads.getRange("L:N").format.columnWidthPx = 115;
leads.getRange("O:O").format.columnWidthPx = 240;
leads.freezePanes.freezeRows(1);

leads.getRange("N2:N200").dataValidation = {
  rule: {
    type: "list",
    values: ["신규", "연락완료", "부재", "재통화예정", "방문예약", "방문완료", "계약검토", "종결"],
  },
};

const guide = workbook.worksheets.add("설정_가이드");
guide.showGridLines = false;
guide.getRange("A1:D1").merge();
guide.getRange("A1:D1").values = [["YouDefine-Sales 상담 DB 설정"]];
guide.getRange("A1:D1").format.fill = { color: "#0A4F57" };
guide.getRange("A1:D1").format.font = { color: "#FFFFFF", bold: true, size: 14 };
guide.getRange("A3:B10").values = [
  ["스프레드시트명", "YouDefine-Sales"],
  ["DB 탭명", "medipark_leads"],
  ["개발자명", "유희진"],
  ["대표번호", "010-6689-2348"],
  ["Apps Script 코드", "medipark_apps_script_draft.gs 사용"],
  ["배포 방식", "웹앱 / 모든 사용자 접근 가능"],
  ["랜딩 연결 위치", "medipark_landing_form_example.html의 APPS_SCRIPT_URL"],
  ["주의", "접수 테스트 후 예시 행은 삭제해도 됩니다."],
];
guide.getRange("A3:A10").format.fill = { color: "#F3E3C4" };
guide.getRange("A3:A10").format.font = { bold: true, color: "#76541A" };
guide.getRange("A3:B10").format.borders = { preset: "all", style: "thin", color: "#E1E7EA" };
guide.getRange("A:B").format.columnWidthPx = 210;
guide.getRange("B:B").format.columnWidthPx = 420;

await fs.mkdir(outputDir, { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputPath);

console.log(outputPath);
