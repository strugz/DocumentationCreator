#!/usr/bin/env node
/*
 * Convert generated documentation (GitHub-Flavored Markdown) to Word .docx.
 *
 * Usage:
 *   node tools/md_to_docx.js <file.md | folder> [out-folder]
 *
 * A folder converts every NN-*.md and INDEX.md in it; the default out-folder is
 * <folder>/export. Supports the subset the templates use: headings, paragraphs,
 * GFM tables, bullet / numbered / checkbox lists, fenced code (Mermaid embedded as an image
 * when tools/render_mermaid.py has rendered it to <folder>/assets/diagrams/, otherwise shown
 * as source with a note), GFM alerts, block quotes, bold, italic, inline code, links, <kbd>.
 * Review markers ([TBD], [ASSUMPTION], [VERIFY], [DECISION]) are highlighted.
 * The Markdown "Table of Contents" section becomes a static, linked list of the ## and ###
 * headings. No Word TOC field is used, so Word never asks to update fields on open.
 */
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const {
  AlignmentType, Bookmark, BorderStyle, Document, ExternalHyperlink, Footer, HeadingLevel,
  ImageRun, InternalHyperlink, LevelFormat, Packer, PageNumber, Paragraph, ShadingType, Table,
  TableCell, TableRow, TextRun, WidthType,
} = require("docx");

const PAGE = { width: 11906, height: 16838, margin: 1134 }; // A4, 2 cm margins
const CONTENT_WIDTH = PAGE.width - 2 * PAGE.margin;
const FONT = "Calibri";
const MONO = "Consolas";
const ALERT_COLORS = { NOTE: "DDEBF7", TIP: "E2EFDA", IMPORTANT: "EDE2F6", WARNING: "FFF2CC", CAUTION: "FCE4D6" };

// ------------------------------------------------------------------ inline

const INLINE_RE = new RegExp([
  String.raw`\*\*[^*]+\*\*`,                                       // bold
  "`[^`]+`",                                                       // code
  String.raw`\[(?:TBD|ASSUMPTION|VERIFY|DECISION)(?::[^\]]*)?\]`,  // review marker
  String.raw`\[[^\]]+\]\([^)]+\)`,                                 // link
  String.raw`<kbd>[^<]+</kbd>`,                                    // key
  String.raw`(?<![\w*])\*[^*\s][^*]*\*(?![\w*])`,                  // italic
].join("|"), "g");

function runs(text, base = {}) {
  const out = [];
  let last = 0;
  for (const m of text.matchAll(INLINE_RE)) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) {
      out.push(...runs(t.slice(2, -2), { ...base, bold: true }));
    } else if (t.startsWith("`")) {
      out.push(new TextRun({ text: t.slice(1, -1), font: MONO, size: 19, ...base }));
    } else if (/^\[(TBD|ASSUMPTION|VERIFY|DECISION)/.test(t)) {
      out.push(new TextRun({ text: t, highlight: "yellow", ...base }));
    } else if (t.startsWith("[")) {
      const lm = t.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      const label = lm[1];
      const href = lm[2];
      if (/^https?:\/\//.test(href)) {
        out.push(new ExternalHyperlink({ link: href, children: [new TextRun({ text: label, style: "Hyperlink", ...base })] }));
      } else {
        out.push(...runs(label, base));
      }
    } else if (t.startsWith("<kbd>")) {
      out.push(new TextRun({ text: t.slice(5, -6), font: MONO, bold: true, ...base }));
    } else {
      out.push(...runs(t.slice(1, -1), { ...base, italics: true }));
    }
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out.length ? out : [new TextRun({ text: "", ...base })];
}

// ------------------------------------------------------------------ blocks

function splitRow(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}

function table(rows) {
  const header = rows[0];
  const body = rows.slice(1);
  const cols = header.length;
  const lengths = header.map((_, i) =>
    Math.min(60, Math.max(4, ...rows.map((r) => (r[i] || "").replace(/[*`]/g, "").length))));
  const totalLen = lengths.reduce((a, b) => a + b, 0);
  const widths = lengths.map((l) => Math.max(700, Math.floor((CONTENT_WIDTH * l) / totalLen)));
  const scale = CONTENT_WIDTH / widths.reduce((a, b) => a + b, 0);
  const colWidths = widths.map((w) => Math.floor(w * scale));
  colWidths[cols - 1] += CONTENT_WIDTH - colWidths.reduce((a, b) => a + b, 0);
  const size = cols >= 7 ? 15 : cols >= 5 ? 17 : 19;
  const border = { style: BorderStyle.SINGLE, size: 4, color: "A6A6A6" };
  const borders = { top: border, bottom: border, left: border, right: border };
  const cell = (text, i, isHeader) => new TableCell({
    width: { size: colWidths[i], type: WidthType.DXA },
    borders,
    shading: isHeader ? { type: ShadingType.CLEAR, color: "auto", fill: "D9E2F3" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ children: runs(text || "", { size, bold: isHeader || undefined }) })],
  });
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, i, true)) }),
      ...body.map((r) => new TableRow({ children: header.map((_, i) => cell(r[i], i, false)) })),
    ],
  });
}

let diagramDir = null; // <doc folder>/assets/diagrams, set per file

// Same key as tools/render_mermaid.py: first 16 hex chars of SHA-1 of the block source.
function diagramImage(lines) {
  if (!diagramDir) return null;
  const key = crypto.createHash("sha1").update(lines.join("\n").trim(), "utf8").digest("hex").slice(0, 16);
  const file = path.join(diagramDir, key + ".png");
  if (!fs.existsSync(file)) return null;
  const data = fs.readFileSync(file);
  if (data.length < 24 || data.readUInt32BE(0) !== 0x89504e47) { // empty or not a PNG: show the source
    console.warn(`warning: ${file} is not a valid PNG; re-run tools/render_mermaid.py`);
    return null;
  }
  let w = data.readUInt32BE(16) / 2, h = data.readUInt32BE(20) / 2; // rendered at 2x
  const maxW = 640, maxH = 860;
  const s = Math.min(1, maxW / w, maxH / h);
  w = Math.round(w * s); h = Math.round(h * s);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 120 },
    children: [new ImageRun({ type: "png", data, transformation: { width: w, height: h } })],
  });
}

function codeBlock(lines, lang) {
  const out = [];
  if (lang === "mermaid") {
    const img = diagramImage(lines);
    if (img) return [img];
    out.push(new Paragraph({
      spacing: { before: 120 },
      children: [new TextRun({ text: "Diagram (Mermaid source; view the Markdown file for the rendered diagram):", italics: true, size: 18, color: "595959" })],
    }));
  }
  lines.forEach((l, i) => out.push(new Paragraph({
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "F2F2F2" },
    spacing: { before: i === 0 ? 60 : 0, after: i === lines.length - 1 ? 120 : 0, line: 240 },
    children: [new TextRun({ text: l.length ? l : " ", font: MONO, size: 17 })],
  })));
  return out;
}

function convert(md, title) {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const children = [];
  let i = 0;
  let skipToc = false;
  let tocAt = -1; // index in children where the TOC entries go
  const tocEntries = []; // { level, text, anchor }
  let para = [];

  const flushPara = () => {
    if (para.length) {
      children.push(new Paragraph({ spacing: { after: 120 }, children: runs(para.join(" ")) }));
      para = [];
    }
  };

  while (i < lines.length) {
    const line = lines[i];

    // fenced code
    const fence = line.match(/^\s*(```|~~~)(.*)$/);
    if (fence) {
      flushPara();
      const lang = fence[2].trim();
      const body = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith(fence[1])) body.push(lines[i++]);
      i++;
      if (!skipToc) children.push(...codeBlock(body, lang));
      continue;
    }

    // headings
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      flushPara();
      const level = h[1].length;
      const text = h[2].trim();
      skipToc = false;
      if (level === 1) {
        children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: runs(text) }));
      } else if (level === 2 && /^table of contents$/i.test(text)) {
        children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(text) }));
        tocAt = children.length;
        skipToc = true;
      } else {
        const map = { 2: HeadingLevel.HEADING_1, 3: HeadingLevel.HEADING_2, 4: HeadingLevel.HEADING_3 };
        let content = runs(text);
        if (level <= 3) {
          const anchor = `_Toc_${tocEntries.length + 1}`; // leading "_" hides it in Word's bookmark list
          tocEntries.push({ level, text, anchor });
          content = [new Bookmark({ id: anchor, children: content })];
        }
        children.push(new Paragraph({ heading: map[level] || HeadingLevel.HEADING_4, children: content }));
      }
      i++;
      continue;
    }
    if (skipToc) { i++; continue; }

    // table
    if (/^\s*\|/.test(line) && i + 1 < lines.length && /^\s*\|?\s*:?-{2,}/.test(lines[i + 1])) {
      flushPara();
      const rows = [splitRow(line)];
      i += 2;
      while (i < lines.length && /^\s*\|/.test(lines[i])) rows.push(splitRow(lines[i++]));
      children.push(table(rows));
      children.push(new Paragraph({ spacing: { after: 60 }, children: [] }));
      continue;
    }

    // block quote / GFM alert
    if (/^\s*>/.test(line)) {
      flushPara();
      const quote = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) quote.push(lines[i++].replace(/^\s*>\s?/, ""));
      const alert = (quote[0] || "").match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$/);
      const text = (alert ? quote.slice(1) : quote).join(" ").trim();
      const fill = alert ? ALERT_COLORS[alert[1]] : "F2F2F2";
      const prefix = alert ? [new TextRun({ text: `${alert[1][0]}${alert[1].slice(1).toLowerCase()}: `, bold: true })] : [];
      children.push(new Paragraph({
        shading: { type: ShadingType.CLEAR, color: "auto", fill },
        indent: { left: 240, right: 240 },
        spacing: { before: 80, after: 120 },
        border: { left: { style: BorderStyle.SINGLE, size: 18, color: "8EA9DB", space: 8 } },
        children: [...prefix, ...runs(text, alert ? {} : { italics: true })],
      }));
      continue;
    }

    // lists
    const li = line.match(/^(\s*)([-*+]|\d+\.)\s+(.*)$/);
    if (li) {
      flushPara();
      const depth = Math.min(2, Math.floor(li[1].length / 2));
      let text = li[3];
      // join wrapped continuation lines (indented, not a new list item) into this item
      while (i + 1 < lines.length && /^\s{2,}\S/.test(lines[i + 1]) && !/^\s*([-*+]|\d+\.)\s+/.test(lines[i + 1])) {
        text += " " + lines[++i].trim();
      }
      const box = text.match(/^\[( |x|X)\]\s+(.*)$/);
      if (box) {
        text = `${box[1] === " " ? "☐" : "☑"} ${box[2]}`;
        children.push(new Paragraph({ indent: { left: 360 + depth * 360 }, children: runs(text) }));
      } else if (/\d+\./.test(li[2])) {
        children.push(new Paragraph({ numbering: { reference: "numbers", level: depth, instance: numberingInstance }, children: runs(text) }));
      } else {
        children.push(new Paragraph({ numbering: { reference: "bullets", level: depth }, children: runs(text) }));
      }
      i++;
      // a non-list line resets numbering for the next numbered list
      if (i < lines.length && !/^(\s*)([-*+]|\d+\.)\s+/.test(lines[i]) && !/^\s+\S/.test(lines[i])) numberingInstance++;
      continue;
    }

    // continuation of a list item (indented text)
    if (/^\s{2,}\S/.test(line) && children.length && para.length === 0) {
      const last = children[children.length - 1];
      if (last instanceof Paragraph) {
        children.push(new Paragraph({ indent: { left: 720 }, children: runs(line.trim()) }));
        i++;
        continue;
      }
    }

    if (!line.trim()) { flushPara(); i++; continue; }
    // a line that starts with a bold label ("**Purpose:**") starts its own paragraph
    if (/^\*\*[^*]+:\*\*/.test(line.trim())) flushPara();
    para.push(line.trim());
    i++;
  }
  flushPara();

  if (tocAt >= 0) {
    children.splice(tocAt, 0, ...tocEntries.map((e) => new Paragraph({
      indent: { left: (e.level - 2) * 360 },
      spacing: { after: e.level === 2 ? 60 : 20 },
      children: [new InternalHyperlink({ anchor: e.anchor, children: runs(e.text, { color: "0563C1" }) })],
    })));
  }

  return new Document({
    creator: "DocumentationCreator",
    title,
    styles: {
      default: { document: { run: { font: FONT, size: 21 }, paragraph: { spacing: { line: 276 } } } }, // Rule 25: 10.5 pt, 1.15 line spacing
      paragraphStyles: [
        { id: "Title", name: "Title", basedOn: "Normal", run: { size: 40, bold: true, color: "1F3864" }, paragraph: { spacing: { after: 240, line: 240 } } },
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, color: "1F3864" }, paragraph: { spacing: { before: 360, after: 120, line: 240 }, outlineLevel: 0, keepNext: true } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 25, bold: true, color: "2F5496" }, paragraph: { spacing: { before: 240, after: 100, line: 240 }, outlineLevel: 1, keepNext: true } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, color: "2F5496" }, paragraph: { spacing: { before: 200, after: 80, line: 240 }, outlineLevel: 2, keepNext: true } },
      ],
    },
    numbering: {
      config: [
        { reference: "bullets", levels: [0, 1, 2].map((l) => ({ level: l, format: LevelFormat.BULLET, text: ["•", "◦", "▪"][l], alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360 + l * 360, hanging: 260 } } } })) },
        { reference: "numbers", levels: [0, 1, 2].map((l) => ({ level: l, format: [LevelFormat.DECIMAL, LevelFormat.LOWER_LETTER, LevelFormat.LOWER_ROMAN][l], text: `%${l + 1}.`, alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360 + l * 360, hanging: 300 } } } })) },
      ],
    },
    sections: [{
      properties: { page: { size: { width: PAGE.width, height: PAGE.height }, margin: { top: PAGE.margin, bottom: PAGE.margin, left: PAGE.margin, right: PAGE.margin } } },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [
              new TextRun({ text: `${title}  |  Page `, size: 16, color: "595959" }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "595959" }),
              new TextRun({ text: " of ", size: 16, color: "595959" }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: "595959" }),
            ],
          })],
        }),
      },
      children,
    }],
  });
}

let numberingInstance = 1;

async function convertFile(src, outDir) {
  numberingInstance = 1;
  // Audience copies live in <doc folder>/export/<name>/; their diagrams are the suite's.
  const dirs = [0, 1, 2].map((up) => path.join(path.dirname(src), ...Array(up).fill(".."), "assets", "diagrams"));
  diagramDir = dirs.find((d) => fs.existsSync(d)) || dirs[0];
  const md = fs.readFileSync(src, "utf8");
  const h1 = (md.match(/^#\s+(.*)$/m) || [null, path.basename(src, ".md")])[1].replace(/[*`]/g, "");
  const doc = convert(md, h1);
  const out = path.join(outDir, path.basename(src, ".md") + ".docx");
  fs.writeFileSync(out, await Packer.toBuffer(doc));
  return out;
}

async function main() {
  const [input, outArg] = process.argv.slice(2);
  if (!input) {
    console.error("Usage: node tools/md_to_docx.js <file.md | folder> [out-folder]");
    process.exit(2);
  }
  const stat = fs.statSync(input);
  const files = stat.isDirectory()
    ? fs.readdirSync(input).filter((f) => /^(\d\d-.*|INDEX)\.md$/.test(f)).sort().map((f) => path.join(input, f))
    : [input];
  const outDir = outArg || path.join(stat.isDirectory() ? input : path.dirname(input), "export");
  fs.mkdirSync(outDir, { recursive: true });
  for (const f of files) console.log("wrote", await convertFile(f, outDir));
}

main().catch((e) => { console.error(e); process.exit(1); });
