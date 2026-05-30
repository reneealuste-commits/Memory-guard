/**
 * DOCX builder with auto-updating TOC via docx-js v9.6.1
 */
const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  AlignmentType,
  TableOfContents,
  PageBreak,
  convertInchesToTwip,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "outputs");

// Load meta via simple eval of exported constants from a JSON sidecar
const metaPath = path.join(ROOT, "books", "book06_strong_son", "meta_export.json");
const meta = JSON.parse(fs.readFileSync(metaPath, "utf8"));

function entityToText(s) {
  return s
    .replace(/&mdash;/g, "\u2014")
    .replace(/&ndash;/g, "\u2013")
    .replace(/&rsquo;/g, "\u2019")
    .replace(/&lsquo;/g, "\u2018")
    .replace(/&rdquo;/g, "\u201d")
    .replace(/&ldquo;/g, "\u201c")
    .replace(/&middot;/g, "\u00b7")
    .replace(/&hellip;/g, "\u2026")
    .replace(/&nbsp;/g, " ")
    .replace(/&copy;/g, "\u00A9")
    .replace(/&amp;/g, "&");
}

function bodyPara(text) {
  return new Paragraph({
    children: [new TextRun({ text: entityToText(text), size: 21, font: "Times New Roman" })],
    spacing: { after: 200 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

function centerPara(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text: entityToText(text), size: opts.size || 21, font: opts.font || "Times New Roman", italics: !!opts.italics, bold: !!opts.bold })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 200, before: opts.before || 0 },
  });
}

function heading1(text) {
  return new Paragraph({ text: entityToText(text), heading: HeadingLevel.HEADING_1, spacing: { after: 240, before: 240 } });
}

function heading2(text) {
  return new Paragraph({ text: entityToText(text), heading: HeadingLevel.HEADING_2, spacing: { after: 200, before: 200 } });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function sectionBreak() {
  return centerPara("* * *", { size: 20 });
}

function buildDocument(chapters) {
  const children = [];

  children.push(centerPara(meta.TITLE, { size: 36, bold: true, before: 2000 }));
  children.push(centerPara(meta.SUBTITLE, { size: 24, italics: true }));
  children.push(centerPara(meta.SERIES, { size: 20 }));
  children.push(pageBreak());

  children.push(heading1("Copyright"));
  children.push(bodyPara(`Copyright \u00A9 ${meta.YEAR} ${meta.COPYRIGHT_HOLDER}, writing as ${meta.PEN_NAME}. All rights reserved.`));
  children.push(pageBreak());

  children.push(heading1("Dedication"));
  children.push(bodyPara(meta.DEDICATION));
  children.push(pageBreak());

  children.push(heading1("Before You Read"));
  meta.NOTE_BEFORE.forEach((p) => children.push(bodyPara(p)));
  children.push(pageBreak());

  children.push(heading1(entityToText(meta.CODE_NAME)));
  meta.CODE_RULES.forEach((rule, i) => {
    children.push(new Paragraph({
      children: [new TextRun({ text: `${i + 1}. ${entityToText(rule)}`, italics: true, size: 21, font: "Times New Roman" })],
      indent: { left: convertInchesToTwip(0.35) },
      spacing: { after: 120 },
    }));
  });
  children.push(pageBreak());

  children.push(new Paragraph({ children: [new TextRun({ text: "Contents", bold: true, size: 28 })], spacing: { after: 240 } }));
  children.push(new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }));
  children.push(pageBreak());

  let currentPart = 0;
  for (let ch = 1; ch <= 14; ch++) {
    const partNum = Math.ceil(ch / 4);
    if (partNum !== currentPart) {
      currentPart = partNum;
      const part = meta.PARTS[partNum - 1];
      children.push(heading2(part.title));
    }
    children.push(centerPara(`CHAPTER ${ch}`, { size: 18, bold: true }));
    children.push(heading1(meta.CHAPTER_TITLES[ch - 1]));
    for (const block of chapters[String(ch)]) {
      if (block === "SECTION_BREAK") children.push(sectionBreak());
      else children.push(bodyPara(block));
    }
    children.push(pageBreak());
  }

  children.push(heading1("A Final Word"));
  meta.CLOSING_LETTER.forEach((p) => children.push(bodyPara(p)));
  children.push(pageBreak());

  children.push(heading1(entityToText(meta.CODE_NAME)));
  meta.CODE_RULES.forEach((rule, i) => {
    children.push(new Paragraph({
      children: [new TextRun({ text: `${i + 1}. ${entityToText(rule)}`, italics: true, size: 21 })],
      indent: { left: convertInchesToTwip(0.35) },
    }));
  });
  children.push(pageBreak());

  children.push(heading1("Sources"));
  meta.SOURCES.forEach((s) => children.push(bodyPara(s)));
  children.push(pageBreak());

  children.push(heading1("About the Author"));
  meta.ABOUT_AUTHOR.forEach((p) => children.push(bodyPara(p)));
  children.push(heading1("Books in This Series"));
  meta.SERIES_LIST.forEach(([t, s]) => children.push(bodyPara(`${entityToText(t)} \u2014 ${entityToText(s)}`)));

  return new Document({
    features: { updateFields: true },
    sections: [{
      properties: {
        page: {
          size: { width: meta.DOCX_WIDTH, height: meta.DOCX_HEIGHT },
          margin: {
            top: meta.DOCX_MARGIN_TOP,
            bottom: meta.DOCX_MARGIN_BOTTOM,
            left: meta.DOCX_MARGIN_LEFT,
            right: meta.DOCX_MARGIN_RIGHT,
          },
        },
      },
      children,
    }],
  });
}

async function main() {
  const chaptersPath = path.join(ROOT, "books", "book06_strong_son", "chapters_export.json");
  const chapters = JSON.parse(fs.readFileSync(chaptersPath, "utf8"));
  const doc = buildDocument(chapters);
  const buf = await Packer.toBuffer(doc);
  fs.mkdirSync(OUT, { recursive: true });
  const outFile = path.join(OUT, `${meta.OUTPUT_BASENAME}.docx`);
  fs.writeFileSync(outFile, buf);
  console.log(`Wrote ${outFile}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
