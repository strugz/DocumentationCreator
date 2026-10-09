#!/usr/bin/env node
/*
 * Build the Mode A or Mode B proposal as a PowerPoint deck (rules/60-proposal-slides.md).
 *
 * Usage:
 *   node tools/md_to_pptx.js <output/mode-a|mode-b/<slug>> [--draft] [--force] [--strict]
 *                            [--out <file.pptx>]
 *
 * The deck is built from a slide spec, <folder>/deck/proposal-slides.json, so the slide
 * text (short, for approvers) is reviewed apart from the layout code:
 *   --draft   write the spec from the proposal (02-project-proposal.md in Mode A,
 *             04-project-proposal.md in Mode B) and stop, so it can be edited first.
 *             An existing spec is kept unless --force is given.
 *   (none)    build <folder>/export/<Product>-Project-Proposal-Slides.pptx from the spec.
 *             If no spec exists yet, the draft is written first and built as it is.
 *   --strict  exit 1 when a check reports a warning.
 *
 * Checks (printed as warnings): slide titles that may not fit one line, too many bullets
 * or table rows, review markers or figures on a slide that the proposal does not contain,
 * and slides without speaker notes.
 *
 * Fonts, sizes and colours follow rules/25-typography.md sections 5 and 7.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");

// Rule 25 colours and families.
const C = {
  title: "1F3864",   // H1/H2 colour, 11.6:1 on white
  accent: "2F5496",  // H3 colour, 7.4:1 on white
  text: "1A1A1A",
  muted: "595959",
  header: "D9E2F3",  // table header fill
  card: "F2F2F2",
  border: "BFBFBF",
  dark: "1F3864",    // cover and ask background
  onDark: "FFFFFF",
  onDarkMuted: "D9E2F3",
  marker: "FFFF00",
};
const SANS = "Calibri";
const DISPLAY = "Cambria";
const W = 13.333; // LAYOUT_WIDE, inches
const X = 0.6;
const CW = W - 2 * X;

const MARKER_RE = /\[(?:TBD|ASSUMPTION|VERIFY|DECISION)(?::[^\]]*)?\]/g;
const LIMITS = { titleChars: 55, bullets: 6, bulletWords: 22, rows: 8, cols: 5, milestones: 6 };

// ------------------------------------------------------------------ Markdown reading

function readProposal(folder) {
  for (const name of ["02-project-proposal.md", "04-project-proposal.md"]) {
    const file = path.join(folder, name);
    if (fs.existsSync(file)) {
      return { file, name, mode: name.startsWith("02") ? "a" : "b", text: fs.readFileSync(file, "utf8") };
    }
  }
  throw new Error(`No 02-project-proposal.md or 04-project-proposal.md in ${folder}`);
}

function stripComments(text) {
  return text.replace(/<!--[\s\S]*?-->/g, "");
}

function plain(s) {
  return unmark(s).trim();
}

// Remove inline Markdown but keep the spaces around it (runs are joined later).
function unmark(s) {
  return s
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\[([^\]]+)\]\((?:[^)]+)\)/g, "$1")
    .replace(/<\/?kbd>/g, "");
}

function sections(text) {
  const out = [];
  let cur = null;
  let fence = false;
  for (const line of stripComments(text).split(/\r?\n/)) {
    if (/^\s*(```|~~~)/.test(line)) fence = !fence;
    const m = !fence && line.match(/^##\s+(.*)$/);
    if (m) {
      cur = { heading: m[1].trim(), lines: [] };
      out.push(cur);
    } else if (cur) {
      cur.lines.push(line);
    }
  }
  return out;
}

function sectionByNumber(secs, n) {
  return secs.find((s) => new RegExp(`^${n}\\.\\s`).test(s.heading));
}

function splitRow(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}

function tables(lines) {
  const out = [];
  let i = 0;
  while (i < lines.length) {
    if (/^\s*\|/.test(lines[i])) {
      const block = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) block.push(lines[i++]);
      const rows = block.map(splitRow).filter((r) => !r.every((c) => /^:?-{2,}:?$/.test(c) || c === ""));
      if (rows.length) out.push({ columns: rows[0].map(plain), rows: rows.slice(1).map((r) => r.map(plain)) });
    } else {
      i++;
    }
  }
  return out;
}

function listItems(lines) {
  let fence = false;
  const out = [];
  for (const line of lines) {
    if (/^\s*(```|~~~)/.test(line)) fence = !fence;
    const m = !fence && line.match(/^(?:[-*]|\d+\.)\s+(?:\[[ xX]\]\s+)?(.*)$/);
    if (m && m[1].trim()) out.push(m[1].trim());
    else if (!fence && out.length && /^\s{2,}\S/.test(line) && !/^\s*([-*]|\d+\.)\s/.test(line)) {
      out[out.length - 1] += " " + line.trim(); // wrapped continuation of the item
    } else if (!fence && /^\S/.test(line)) {
      out.push(null); // a paragraph or table ends the list
    }
  }
  return out.filter((x) => x);
}

function inShort(lines) {
  const joined = lines.join("\n");
  const m = joined.match(/^>\s*\*\*In short:?\*\*\s*(.+)$/im);
  return m ? m[1].trim() : "";
}

function paragraphs(lines) {
  const out = [];
  let buf = [];
  let fence = false;
  const flush = () => { if (buf.length) out.push(buf.join(" ")); buf = []; };
  for (const line of lines) {
    if (/^\s*(```|~~~)/.test(line)) { fence = !fence; flush(); continue; }
    if (fence || /^\s*$/.test(line) || /^\s*(\||>|#|[-*]\s|\d+\.\s)/.test(line)) { flush(); continue; }
    buf.push(line.trim());
  }
  flush();
  return out;
}

function subsection(lines, pattern) {
  const out = [];
  let on = false;
  for (const line of lines) {
    const m = line.match(/^###\s+(.*)$/);
    if (m) on = pattern.test(m[1]);
    else if (on) out.push(line);
  }
  return out;
}

function notesOf(sec) {
  return sec.lines
    .filter((l) => !/^\s*\|?\s*:?-{2,}/.test(l) && !/^>\s*\[!/.test(l))
    .map((l) => plain(l.replace(/^#+\s*/, "").replace(/^>\s?/, "").replace(/^\s*\|\s?|\s?\|\s*$/g, "")
      .replace(/\s*\|\s*/g, " | ")))
    .filter((l) => l)
    .join("\n");
}

function docControl(text) {
  const out = {};
  for (const line of text.split(/\r?\n/).slice(0, 40)) {
    const r = /^\s*\|/.test(line) ? splitRow(line) : null;
    if (r && r.length >= 2 && !/^-+$/.test(r[0])) out[plain(r[0]).toLowerCase()] = plain(r[1]);
  }
  return out;
}

function isNotApplicable(sec) {
  return /^not applicable/i.test(paragraphs(sec.lines)[0] || "");
}

function sentences(text, n) {
  return (text.match(/[^.!?]+[.!?]+(\s|$)/g) || [text]).map((s) => s.trim()).filter(Boolean).slice(0, n);
}

// ------------------------------------------------------------------ draft spec

const MAP = [
  { n: 2, title: "The problem" },
  { n: 3, title: "What we want to achieve" },
  { n: 4, title: "What we propose" },
  { n: 5, title: "What is in and out of scope", type: "columns" },
  { n: 6, title: "How we deliver it" },
  { n: 7, title: "Timeline and milestones", type: "timeline" },
  { n: 8, title: "Team and resources" },
  { n: 9, title: "Budget" },
  { n: 10, title: "Benefits" },
  { n: 11, title: "Main risks and how we handle them" },
];

function bodyFor(sec) {
  const t = tables(sec.lines)[0];
  if (t && t.rows.length) {
    return { type: "table", columns: t.columns.slice(0, 4), rows: t.rows.slice(0, 6).map((r) => r.slice(0, 4)) };
  }
  const items = listItems(sec.lines).map(plain);
  if (items.length) return { type: "bullets", bullets: items.slice(0, LIMITS.bullets) };
  const para = paragraphs(sec.lines).map(plain).join(" ");
  return { type: "bullets", bullets: para ? sentences(para, 4) : [] };
}

function scopeColumn(sec, pattern) {
  const lines = subsection(sec.lines, pattern);
  const items = listItems(lines).map(plain);
  if (items.length) return items.slice(0, LIMITS.bullets);
  const t = tables(lines)[0];
  return t ? t.rows.map((r) => r[0]).slice(0, LIMITS.bullets) : [];
}

function draftSpec(proposal) {
  const secs = sections(proposal.text);
  const dc = docControl(proposal.text);
  const product = dc.project || (proposal.text.match(/^#\s+(.+?)(\s+[—-]\s+.*)?$/m) || [])[1] || "Product";
  const slides = [];

  const meta = ["prepared for", "prepared by", "date", "status"]
    .filter((k) => dc[k] && !/\{\{|^$/.test(dc[k]))
    .map((k) => `${k[0].toUpperCase()}${k.slice(1)}: ${dc[k]}`);
  const exec = sectionByNumber(secs, 1);
  slides.push({
    type: "cover", title: product, subtitle: "Project Proposal", meta,
    notes: exec ? notesOf(exec) : "", source: "Document Control, section 1",
  });

  for (const m of MAP) {
    const sec = sectionByNumber(secs, m.n);
    if (!sec || isNotApplicable(sec)) continue;
    const eyebrow = sec.heading.replace(/^\d+\.\s*/, "").toUpperCase();
    const base = { eyebrow, title: m.title, lead: plain(inShort(sec.lines)), notes: notesOf(sec), source: `section ${m.n}` };
    if (m.type === "columns") {
      const left = scopeColumn(sec, /in scope/i);
      const right = scopeColumn(sec, /out of scope/i);
      if (left.length || right.length) {
        slides.push({ ...base, type: "columns", left: { heading: "In scope", bullets: left },
          right: { heading: "Out of scope", bullets: right } });
        continue;
      }
    }
    if (m.type === "timeline") {
      const t = tables(sec.lines)[0];
      if (t && t.rows.length && t.rows.length <= LIMITS.milestones) {
        const di = Math.max(0, t.columns.findIndex((c) => /date|when|target|month/i.test(c)));
        slides.push({ ...base, type: "timeline",
          milestones: t.rows.map((r) => ({ label: r[0], date: di ? r[di] : r[r.length - 1] })) });
        continue;
      }
    }
    slides.push({ ...base, ...bodyFor(sec) });
  }

  const next = sectionByNumber(secs, 14);
  const approval = sectionByNumber(secs, 15);
  const ask = next ? bodyFor(next) : { bullets: [] };
  const open = secs.find((s) => /^open items$/i.test(s.heading));
  const openCount = open ? Math.max(0, (tables(open.lines)[0] || { rows: [] }).rows
    .filter((r) => r.some((c) => c && c !== "—")).length) : 0;
  slides.push({
    type: "ask", title: "The ask",
    bullets: ask.type === "table" ? ask.rows.map((r) => r.join(" — ")) : ask.bullets,
    notes: [next ? notesOf(next) : "", approval ? notesOf(approval) : "",
      `Open items in the proposal: ${openCount}.`].filter(Boolean).join("\n\n"),
    source: "sections 14 and 15",
  });

  return {
    product, document: "Project Proposal", mode: proposal.mode, source: proposal.name,
    generated: "Draft from the proposal. Shorten the slide text; keep facts, figures and markers as written.",
    slides,
  };
}

// ------------------------------------------------------------------ checks

function slideText(s) {
  const parts = [s.title, s.subtitle, s.eyebrow, s.lead, ...(s.meta || []), ...(s.bullets || [])];
  if (s.columns) parts.push(...s.columns, ...s.rows.flat());
  if (s.left) parts.push(s.left.heading, ...s.left.bullets, s.right.heading, ...s.right.bullets);
  if (s.milestones) s.milestones.forEach((m) => parts.push(m.label, m.date));
  return parts.filter(Boolean).join("\n");
}

function check(spec, proposalText) {
  const warnings = [];
  const source = plain(stripComments(proposalText));
  spec.slides.forEach((s, i) => {
    const at = `slide ${i + 1} (${s.title || s.type})`;
    if ((s.title || "").length > LIMITS.titleChars && s.type !== "cover") {
      warnings.push(`${at}: title has ${s.title.length} characters and may not fit one line`);
    }
    if ((s.bullets || []).length > LIMITS.bullets) warnings.push(`${at}: ${s.bullets.length} bullets (max ${LIMITS.bullets})`);
    for (const b of s.bullets || []) {
      const words = b.split(/\s+/).length;
      if (words > LIMITS.bulletWords) warnings.push(`${at}: a bullet has ${words} words; move detail to the notes`);
    }
    if (s.rows && s.rows.length > LIMITS.rows) warnings.push(`${at}: ${s.rows.length} table rows (max ${LIMITS.rows})`);
    if (s.columns && s.columns.length > LIMITS.cols) warnings.push(`${at}: ${s.columns.length} table columns (max ${LIMITS.cols})`);
    if (s.milestones && s.milestones.length > LIMITS.milestones) {
      warnings.push(`${at}: ${s.milestones.length} milestones (max ${LIMITS.milestones}); use a table slide`);
    }
    if (!s.notes || !s.notes.trim()) warnings.push(`${at}: no speaker notes`);
    const text = slideText(s);
    for (const mk of new Set(text.match(MARKER_RE) || [])) {
      if (!source.includes(mk)) warnings.push(`${at}: marker ${mk} is not in the proposal`);
    }
    for (const num of new Set(text.match(/\d[\d.,:/-]*\d|\d/g) || [])) {
      const n = num.replace(/[.,:/-]+$/, "");
      if (!source.includes(n)) warnings.push(`${at}: figure "${n}" is not in the proposal`);
    }
  });
  return warnings;
}

// ------------------------------------------------------------------ rendering

function textRuns(s, base) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\[(?:TBD|ASSUMPTION|VERIFY|DECISION)(?::[^\]]*)?\])/g;
  let last = 0;
  for (const m of s.matchAll(re)) {
    if (m.index > last) out.push({ text: unmark(s.slice(last, m.index)), options: { ...base } });
    const t = m[0];
    if (t.startsWith("**")) out.push({ text: t.slice(2, -2), options: { ...base, bold: true } });
    else out.push({ text: t, options: { ...base, color: "000000", highlight: C.marker } });
    last = m.index + t.length;
  }
  if (last < s.length) out.push({ text: unmark(s.slice(last)), options: { ...base } });
  const runs = out.filter((r) => r.text !== "");
  // An empty run list makes pptxgenjs write an invalid element (PowerPoint rejects the file).
  return runs.length ? runs : [{ text: " ", options: { ...base } }];
}

function bulletRuns(items, base) {
  const out = [];
  items.forEach((item, i) => {
    const r = textRuns(item, base);
    r[0].options = { ...r[0].options, bullet: { indent: 18 }, paraSpaceAfter: 8 };
    r[r.length - 1].options = { ...r[r.length - 1].options, breakLine: i < items.length - 1 };
    out.push(...r);
  });
  return out;
}

function defineMasters(pptx, spec) {
  const footer = `${spec.product} | ${spec.document}`;
  const slideNumber = { x: W - X - 1.0, y: 7.0, w: 1.0, h: 0.3, fontFace: SANS, fontSize: 11, align: "right" };
  pptx.defineSlideMaster({
    title: "CONTENT",
    background: { color: "FFFFFF" },
    objects: [
      { text: { text: footer, options: { x: X, y: 7.0, w: 9, h: 0.3, fontFace: SANS, fontSize: 11, color: C.muted } } },
      { line: { x: X, y: 6.92, w: CW, h: 0, line: { color: C.border, width: 0.75 } } },
    ],
    slideNumber: { ...slideNumber, color: C.muted },
  });
  pptx.defineSlideMaster({
    title: "DARK",
    background: { color: C.dark },
    objects: [
      { text: { text: footer, options: { x: X, y: 7.0, w: 9, h: 0.3, fontFace: SANS, fontSize: 11, color: C.onDarkMuted } } },
    ],
    slideNumber: { ...slideNumber, color: C.onDarkMuted },
  });
}

function header(slide, s) {
  if (s.eyebrow) {
    slide.addText(s.eyebrow, { x: X, y: 0.35, w: CW, h: 0.35, fontFace: SANS, fontSize: 13, bold: true,
      color: C.accent, charSpacing: 1, margin: 0 });
  }
  slide.addText(s.title || "", { x: X, y: 0.7, w: CW, h: 0.8, fontFace: DISPLAY, fontSize: 30, bold: true,
    color: C.title, margin: 0, valign: "middle", fit: "none" });
  let y = 1.65;
  if (s.lead) {
    slide.addText(textRuns(s.lead, { fontFace: SANS, fontSize: 20, color: C.text }),
      { x: X, y, w: CW, h: 0.75, margin: 0, valign: "top" });
    y += 0.9;
  }
  return y;
}

function addBullets(slide, s, y) {
  const n = (s.bullets || []).length;
  const size = n > 5 || (s.bullets || []).join(" ").length > 420 ? 18 : 20;
  slide.addText(bulletRuns(s.bullets || [], { fontFace: SANS, fontSize: size, color: C.text }),
    { x: X, y, w: CW, h: 6.75 - y, valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
}

function addTable(slide, s, y) {
  const cols = s.columns.length;
  const head = s.columns.map((c) => ({ text: textRuns(c, { bold: true, color: "000000" }),
    options: { fill: { color: C.header } } }));
  const body = s.rows.map((r) => r.map((c) => ({ text: textRuns(c || "", { color: C.text }) })));
  const size = s.rows.length > 6 ? 14 : 16;
  slide.addTable([head, ...body], {
    x: X, y, w: CW, colW: Array(cols).fill(CW / cols), fontFace: SANS, fontSize: size,
    border: { type: "solid", pt: 0.75, color: C.border }, valign: "middle", margin: 0.08, autoPage: false,
  });
}

function addColumns(slide, s, y) {
  const gap = 0.35;
  const w = (CW - gap) / 2;
  [s.left, s.right].forEach((col, i) => {
    const x = X + i * (w + gap);
    slide.addShape("roundRect", { x, y, w, h: 6.7 - y, fill: { color: C.card }, line: { color: C.card },
      rectRadius: 0.08, shadow: { type: "outer", blur: 4, offset: 1.5, angle: 90, color: "000000", opacity: 0.18 } });
    slide.addText(col.heading, { x: x + 0.3, y: y + 0.2, w: w - 0.6, h: 0.45, fontFace: SANS, fontSize: 20,
      bold: true, color: C.title, margin: 0 });
    slide.addText(bulletRuns(col.bullets.length ? col.bullets : ["None stated"],
      { fontFace: SANS, fontSize: 16, color: C.text }),
    { x: x + 0.3, y: y + 0.8, w: w - 0.6, h: 6.7 - y - 1.0, valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
  });
}

function addTimeline(slide, s, y) {
  const ms = s.milestones;
  const lineY = y + 1.2;
  const bw = Math.min(2.4, CW / Math.max(1, ms.length));
  const x0 = X + bw / 2;
  const span = CW - bw;
  const step = ms.length > 1 ? span / (ms.length - 1) : 0;
  slide.addShape("line", { x: x0, y: lineY, w: span, h: 0, line: { color: C.accent, width: 2 } });
  ms.forEach((m, i) => {
    const cx = ms.length === 1 ? X + CW / 2 : x0 + i * step;
    const d = 0.5;
    slide.addShape("ellipse", { x: cx - d / 2, y: lineY - d / 2, w: d, h: d, fill: { color: C.accent },
      line: { color: C.accent } });
    slide.addText(String(i + 1), { x: cx - d / 2, y: lineY - d / 2, w: d, h: d, fontFace: SANS, fontSize: 14,
      bold: true, color: C.onDark, align: "center", valign: "middle", margin: 0 });
    slide.addText([
      ...textRuns(m.label, { fontFace: SANS, fontSize: 16, bold: true, color: C.text, breakLine: true }),
      ...textRuns(m.date || "", { fontFace: SANS, fontSize: 14, color: C.muted }),
    ], { x: cx - bw / 2 + 0.05, y: lineY + 0.45, w: bw - 0.1, h: 1.6, align: "center", valign: "top",
      margin: 0, paraSpaceAfter: 4 });
  });
}

function addCover(slide, s) {
  slide.addText(s.title, { x: X, y: 2.0, w: CW, h: 1.2, fontFace: DISPLAY, fontSize: 44, bold: true,
    color: C.onDark, align: "center", valign: "middle", margin: 0 });
  slide.addText(s.subtitle || "", { x: X, y: 3.25, w: CW, h: 0.6, fontFace: SANS, fontSize: 24,
    color: C.onDarkMuted, align: "center", margin: 0 });
  if ((s.meta || []).length) {
    const meta = [];
    s.meta.forEach((line, i) => {
      const r = textRuns(line, { fontFace: SANS, fontSize: 16, color: C.onDark });
      r[r.length - 1].options = { ...r[r.length - 1].options, breakLine: i < s.meta.length - 1 };
      meta.push(...r);
    });
    slide.addText(meta, { x: X, y: 4.4, w: CW, h: 1.6, align: "center", valign: "top", margin: 0,
      lineSpacingMultiple: 1.2 });
  }
}

function addAsk(slide, s) {
  slide.addText(s.title || "The ask", { x: X, y: 0.8, w: CW, h: 0.9, fontFace: DISPLAY, fontSize: 32,
    bold: true, color: C.onDark, margin: 0 });
  slide.addText(bulletRuns(s.bullets || [], { fontFace: SANS, fontSize: 22, color: C.onDark }),
    { x: X, y: 2.0, w: CW, h: 4.6, valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
}

async function build(spec, out) {
  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.title = `${spec.product} — ${spec.document}`;
  pptx.company = "";
  pptx.theme = { headFontFace: DISPLAY, bodyFontFace: SANS };
  defineMasters(pptx, spec);
  for (const s of spec.slides) {
    const dark = s.type === "cover" || s.type === "ask";
    const slide = pptx.addSlide({ masterName: dark ? "DARK" : "CONTENT" });
    if (s.type === "cover") addCover(slide, s);
    else if (s.type === "ask") addAsk(slide, s);
    else {
      const y = header(slide, s);
      if (s.type === "table") addTable(slide, s, y);
      else if (s.type === "columns") addColumns(slide, s, y);
      else if (s.type === "timeline") addTimeline(slide, s, y);
      else addBullets(slide, s, y);
    }
    if (s.notes) slide.addNotes(s.notes);
  }
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await pptx.writeFile({ fileName: out });
}

// ------------------------------------------------------------------ main

async function main(argv) {
  const args = argv.filter((a) => !a.startsWith("--"));
  const flags = new Set(argv.filter((a) => a.startsWith("--")));
  const outIdx = argv.indexOf("--out");
  if (!args[0]) {
    console.error("Usage: node tools/md_to_pptx.js <output/<mode>/<slug>> [--draft] [--force] [--strict] [--out file]");
    return 2;
  }
  const folder = path.resolve(args[0]);
  const proposal = readProposal(folder);
  const specPath = path.join(folder, "deck", "proposal-slides.json");

  if (flags.has("--draft") || !fs.existsSync(specPath)) {
    if (fs.existsSync(specPath) && !flags.has("--force")) {
      console.error(`${specPath} exists; pass --force to replace it.`);
      return 2;
    }
    fs.mkdirSync(path.dirname(specPath), { recursive: true });
    fs.writeFileSync(specPath, JSON.stringify(draftSpec(proposal), null, 2) + "\n", "utf8");
    console.log(`Wrote draft slide spec ${path.relative(process.cwd(), specPath)}`);
    if (flags.has("--draft")) return 0;
  }

  const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
  const warnings = check(spec, proposal.text);
  const name = `${spec.product.replace(/[^\w]+/g, "-").replace(/^-|-$/g, "")}-Project-Proposal-Slides.pptx`;
  const out = outIdx > -1 ? path.resolve(argv[outIdx + 1]) : path.join(folder, "export", name);
  await build(spec, out);
  console.log(`Wrote ${path.relative(process.cwd(), out)} (${spec.slides.length} slides)`);
  for (const w of warnings) console.log(`  WARNING ${w}`);
  console.log(`${warnings.length} warning(s).`);
  return flags.has("--strict") && warnings.length ? 1 : 0;
}

if (require.main === module) {
  main(process.argv.slice(2)).then((code) => process.exit(code), (err) => {
    console.error(err.message);
    process.exit(2);
  });
}

module.exports = { draftSpec, check, build, sections, tables, listItems };
