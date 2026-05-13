from __future__ import annotations

import html
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "04_素材资产"
OUT = ROOT / "05_源文件PPT" / "中国道路再理解_是否还在走社会主义.pptx"
SCRIPT_OUT = ROOT / "02_文案大纲" / "中国道路再理解_口语化演讲稿.md"

COVER = ASSET_DIR / "socialism_path_cover.png"
STATE_MARKET = ASSET_DIR / "state_market_section.png"
COMMON = ASSET_DIR / "common_prosperity_section.png"

SLIDE_W = 12192000
SLIDE_H = 6858000
EMU_PER_IN = 914400
LAYOUT_W = 13.333
LAYOUT_H = 7.5

INK = "15202B"
MUTED = "697586"
BG = "F4F1EA"
WHITE = "FFFFFF"
PAPER = "FFFDF7"
DARK = "07111D"
RED = "B91C1C"
GOLD = "D6A13B"
TEAL = "00A6A6"
BLUE = "2563EB"
GREEN = "16825D"
LINE = "E4DED2"

TRANSITION_SEQUENCE = [
    "fade",
    "push_left",
    "wipe_right",
    "split_in",
    "cover_left",
    "uncover_down",
]

ANIMATION_SEQUENCE = [
    ("fade", "1"),
    ("wipe(up)", "22"),
    ("wipe(right)", "5"),
    ("wipe(left)", "5"),
    ("zoom", "10"),
    ("float", "2"),
]


def emu(v: float) -> int:
    return int(v * EMU_PER_IN)


def esc(s: str) -> str:
    return html.escape(str(s), quote=False)


class Slide:
    def __init__(
        self,
        title: str | None = None,
        kicker: str | None = None,
        bg: str = BG,
        dark: bool = False,
        transition: str = "fade",
    ):
        self.parts: list[str] = []
        self.rels: list[tuple[str, str, str]] = []
        self.notes = ""
        self.next_id = 2
        self.next_rel = 1
        self.anim_ids: list[int] = []
        self.transition = transition
        self.dark = dark
        self.bg(bg)
        if title:
            color = WHITE if dark else INK
            if kicker:
                self.text(kicker, 0.65, 0.34, 3.5, 0.24, 8, GOLD if dark else RED, bold=True, animate=False)
            self.text(title, 0.65, 0.62, 8.9, 0.58, 18, color, bold=True, animate=True)
            self.rect(0.65, 1.22, 0.95, 0.035, GOLD if dark else RED, line=False, animate=False)

    def sid(self) -> int:
        i = self.next_id
        self.next_id += 1
        return i

    def rid(self) -> str:
        r = f"rId{self.next_rel}"
        self.next_rel += 1
        return r

    def bg(self, color: str):
        sid = self.sid()
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Background"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>"""
        )

    def rect(
        self,
        x,
        y,
        w,
        h,
        fill,
        alpha: int | None = None,
        radius: bool = False,
        line=True,
        line_color=LINE,
        line_w=1,
        animate=False,
    ):
        sid = self.sid()
        if animate:
            self.anim_ids.append(sid)
        alpha_xml = f'<a:alpha val="{alpha}"/>' if alpha else ""
        ln = f'<a:ln w="{int(line_w*12700)}"><a:solidFill><a:srgbClr val="{line_color}"/></a:solidFill></a:ln>' if line else "<a:ln><a:noFill/></a:ln>"
        geom = "roundRect" if radius else "rect"
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Shape"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}">{alpha_xml}</a:srgbClr></a:solidFill>{ln}</p:spPr>
<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>"""
        )
        return sid

    def line(self, x, y, w, color=LINE, thickness=0.012):
        self.rect(x, y, w, thickness, color, line=False)

    def text(
        self,
        s,
        x,
        y,
        w,
        h,
        size=12,
        color=INK,
        bold=False,
        align="l",
        valign="top",
        alpha: int | None = None,
        animate=True,
    ):
        sid = self.sid()
        if animate:
            self.anim_ids.append(sid)
        paras = str(s).split("\n")
        para_xml = []
        for para in paras:
            if not para:
                para = " "
            alpha_xml = f'<a:alpha val="{alpha}"/>' if alpha else ""
            para_xml.append(
                f"""<a:p><a:pPr algn="{align}"/><a:r><a:rPr lang="zh-CN" sz="{int(size*100)}" b="{1 if bold else 0}"><a:solidFill><a:srgbClr val="{color}">{alpha_xml}</a:srgbClr></a:solidFill><a:latin typeface="Microsoft YaHei"/><a:ea typeface="Microsoft YaHei"/></a:rPr><a:t>{esc(para)}</a:t></a:r></a:p>"""
            )
        anchor = {"top": "t", "mid": "ctr", "bottom": "b"}.get(valign, "t")
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Text"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr wrap="square" anchor="{anchor}"><a:spAutoFit/></a:bodyPr><a:lstStyle/>{''.join(para_xml)}</p:txBody></p:sp>"""
        )
        return sid

    def image(self, path: Path, x, y, w, h, animate=False):
        sid = self.sid()
        if animate:
            self.anim_ids.append(sid)
        rid = self.rid()
        self.rels.append((rid, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", f"../media/{path.name}"))
        self.parts.append(
            f"""<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="{esc(path.name)}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>
<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>"""
        )
        return sid

    def card(self, x, y, w, h, title, body, accent=RED, dark=False):
        fill = "101B2A" if dark else PAPER
        text = WHITE if dark else INK
        body_col = "CCD3DC" if dark else MUTED
        line_col = "233144" if dark else LINE
        self.rect(x, y, w, h, fill, radius=True, line=True, line_color=line_col, animate=True)
        self.rect(x, y, 0.055, h, accent, line=False, animate=False)
        self.text(title, x + 0.24, y + 0.18, w - 0.45, 0.28, 10.5, text, bold=True)
        self.text(body, x + 0.24, y + 0.56, w - 0.45, h - 0.65, 7.8, body_col)

    def pill(self, s, x, y, w, color, text=WHITE):
        self.rect(x, y, w, 0.32, color, radius=True, line=False, animate=True)
        self.text(s, x + 0.1, y + 0.09, w - 0.2, 0.12, 7.2, text, bold=True, align="ctr")

    def footer(self, source="资料来源：公开资料整理；宪法、二十大报告、二十届三中全会决定、财政部等"):
        self.text(source, 0.62, 7.08, 9.2, 0.16, 5.5, "8C939D", animate=False)
        self.text("中国道路再理解", 10.9, 7.08, 1.75, 0.16, 5.5, "8C939D", align="r", animate=False)

    def transition_xml(self) -> str:
        mapping = {
            "fade": "<p:fade/>",
            "push": '<p:push dir="l"/>',
            "push_left": '<p:push dir="l"/>',
            "push_right": '<p:push dir="r"/>',
            "wipe": '<p:wipe dir="r"/>',
            "wipe_right": '<p:wipe dir="r"/>',
            "wipe_down": '<p:wipe dir="d"/>',
            "split": '<p:split orient="vert" dir="in"/>',
            "split_in": '<p:split orient="vert" dir="in"/>',
            "cover_left": '<p:cover dir="l"/>',
            "uncover_down": '<p:uncover dir="d"/>',
        }
        return f'<p:transition spd="med" advClick="1">{mapping.get(self.transition, "<p:fade/>")}</p:transition>'

    def anim_node(self, sid: int, idx: int, tid: int) -> tuple[str, int]:
        effect, preset = ANIMATION_SEQUENCE[idx % len(ANIMATION_SEQUENCE)]
        delay = idx * 110
        dur = 420 if idx < 3 else 360
        # PowerPoint/WPS expect each click effect to be wrapped by an
        # indefinite parent node, then registered again in p:bldLst.
        node = f"""<p:par><p:cTn id="{tid}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{tid+1}" presetID="{preset}" presetClass="entr" presetSubtype="0" fill="hold" grpId="{idx+1}" nodeType="clickEffect"><p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr><p:cTn id="{tid+2}" dur="1" fill="hold"/><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="{effect}"><p:cBhvr><p:cTn id="{tid+3}" dur="{dur}" fill="hold"/><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"""
        return node, tid + 4

    def build_list_xml(self) -> str:
        unique_ids = []
        seen = set()
        for sid in self.anim_ids[:12]:
            if sid not in seen:
                unique_ids.append(sid)
                seen.add(sid)
        entries = "".join(
            f'<p:bldP spid="{sid}" grpId="{i}" build="allAtOnce" uiExpand="1"/>'
            for i, sid in enumerate(unique_ids, start=1)
        )
        return f"<p:bldLst>{entries}</p:bldLst>" if entries else ""

    def timing_xml(self) -> str:
        if not self.anim_ids:
            return ""
        nodes = []
        tid = 10
        for i, sid in enumerate(self.anim_ids[:12]):
            node, tid = self.anim_node(sid, i, tid)
            nodes.append(node)
        return f"""<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{''.join(nodes)}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>{self.build_list_xml()}</p:timing>"""

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{''.join(self.parts)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>{self.transition_xml()}{self.timing_xml()}</p:sld>"""

    def rels_xml(self, idx: int) -> str:
        rels = [
            '<Relationship Id="rIdLayout" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>',
            f'<Relationship Id="rIdNotes" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{idx}.xml"/>',
        ]
        for rid, typ, target in self.rels:
            rels.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>')
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>"""


def notes_xml(note: str) -> str:
    paragraphs = []
    for line in note.split("\n"):
        line = line.strip()
        if not line:
            continue
        paragraphs.append(
            f"""<a:p><a:r><a:rPr lang="zh-CN" sz="1200"><a:latin typeface="Microsoft YaHei"/><a:ea typeface="Microsoft YaHei"/></a:rPr><a:t>{esc(line)}</a:t></a:r></a:p>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr><p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes Placeholder"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr><a:xfrm><a:off x="685800" y="914400"/><a:ext cx="7772400" cy="5486400"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square"/><a:lstStyle/>{''.join(paragraphs)}</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>"""


def notes_rels_xml(idx: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{idx}.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="../notesMasters/notesMaster1.xml"/></Relationships>"""


def build_slides() -> list[Slide]:
    slides: list[Slide] = []

    s = Slide(bg=DARK, dark=True, transition="fade")
    s.image(COVER, 0, 0, LAYOUT_W, LAYOUT_H)
    s.rect(0, 0, 6.2, LAYOUT_H, "07111D", alpha=85000, line=False)
    s.text("中国道路再理解", 0.7, 1.2, 4.8, 0.42, 14, "F4D58D", bold=True)
    s.text("还在走社会主义吗？", 0.7, 1.75, 5.3, 0.78, 27, WHITE, bold=True)
    s.line(0.72, 2.82, 1.05, GOLD, 0.04)
    s.text("一个面向普通听众的政治经济分析", 0.72, 3.18, 5.2, 0.36, 11, "DDE6F0")
    s.text("不是给口号找答案，而是用标准判断方向", 0.72, 3.62, 5.15, 0.3, 9, "AFBAC8")
    s.text("2026年5月", 0.72, 6.62, 1.5, 0.18, 8, "DDE6F0")
    s.notes = "各位好，今天我们讨论一个很容易被一句话带偏的问题：中国到底还在不在走社会主义这条路？我不想一上来就给结论，因为不同人说的“社会主义”，可能不是同一个东西。今天我们换一种方式，用几个看得见的标准来判断。"
    slides.append(s)

    s = Slide("先把问题问准：我们到底在问什么？", "01 破题", bg="F5F2EA")
    items = [
        ("不是问", "中国是不是还停留在计划经济时代。答案显然不是。", RED),
        ("也不是问", "中国有没有市场、企业、竞争和资本。答案显然有。", BLUE),
        ("真正要问", "市场、资本和效率，最终服务谁？由什么制度来约束？", GREEN),
        ("判断方法", "看方向、看机制、看分配、看治理，而不是只看某一个现象。", GOLD),
    ]
    for i, (t, b, c) in enumerate(items):
        s.card(0.8 + (i % 2) * 6.0, 1.55 + (i // 2) * 1.75, 5.45, 1.18, t, b, c)
    s.rect(0.95, 5.55, 11.1, 0.62, INK, radius=True, line=False)
    s.text("一句话：这个问题不能用“有没有市场”来判断，而要看市场被放在什么制度目标里。", 1.2, 5.78, 10.55, 0.16, 9.2, WHITE, bold=True, align="ctr")
    s.footer()
    s.notes = "这一页先帮大家把问题问准。很多争论其实不是在争同一件事。有人一看到市场经济，就说这不是社会主义；有人一看到国企和政府规划，就说这不是市场经济。其实真正的问题是：市场、企业、资本、效率这些东西，最后是不是服务于一个公共目标？它们有没有被制度约束？"
    slides.append(s)

    s = Slide("判断一条路，不能只看车速，要看方向盘、发动机和终点", "02 判断框架", bg=DARK, dark=True, transition="push")
    s.rect(0, 0, LAYOUT_W, LAYOUT_H, "000000", alpha=12000, line=False)
    framework = [
        ("方向盘", "制度文本与政治方向", "宪法、党的领导、社会主义制度", RED),
        ("发动机", "经济运行机制", "市场配置资源 + 政府战略引导", TEAL),
        ("乘客", "发展成果归属", "就业、收入、公共服务、共同富裕", GOLD),
        ("路况", "现实矛盾与调整", "不平衡、资本扩张、外部压力", BLUE),
    ]
    for i, (t, b, c, col) in enumerate(framework):
        x = 0.85 + i * 3.08
        s.rect(x, 1.8, 2.45, 3.25, "111C2D", radius=True, line=True, line_color="2C3A4C")
        s.text(t, x + 0.18, 2.15, 2.05, 0.26, 14, col, bold=True, align="ctr")
        s.text(b, x + 0.22, 2.72, 2.0, 0.3, 10, WHITE, bold=True, align="ctr")
        s.text(c, x + 0.24, 3.38, 1.95, 0.65, 8, "BBC6D4", align="ctr")
    s.text("如果四个维度放在一起看，答案会比“是/不是”更清楚。", 1.0, 5.85, 10.9, 0.26, 13, "F2E6BE", bold=True, align="ctr")
    s.footer()
    s.notes = "我用一个很口语化的比喻。看一辆车是不是在往某个方向走，不能只看它开得快不快，也不能只看它用了什么发动机。我们要看方向盘指向哪里，发动机怎么运转，车上主要载的是谁，以及遇到路况时怎么调整。放到中国，就是制度方向、经济机制、发展成果归属和现实矛盾四件事。"
    slides.append(s)

    s = Slide("制度文本上，中国明确把社会主义作为根本制度", "03 方向盘", bg="F8F5ED")
    s.rect(0.78, 1.52, 5.55, 4.5, INK, radius=True, line=False)
    s.text("宪法第一条明确：\n社会主义制度是中华人民共和国的根本制度。", 1.16, 2.16, 4.75, 0.95, 18, WHITE, bold=True)
    s.text("这意味着，在正式制度表达中，“社会主义”不是一个可有可无的标签，而是国家制度身份。", 1.2, 3.62, 4.55, 0.55, 10, "D5DEE8")
    s.card(6.75, 1.56, 4.95, 1.05, "党的领导", "官方表述中，中国共产党领导被视为中国特色社会主义最本质的特征。", RED)
    s.card(6.75, 2.9, 4.95, 1.05, "中国式现代化", "二十大报告将其定义为中国共产党领导的社会主义现代化。", GOLD)
    s.card(6.75, 4.24, 4.95, 1.05, "结论", "如果按制度文本和政治方向判断，中国仍然明确宣称并维护社会主义方向。", GREEN)
    s.footer("资料来源：中华人民共和国宪法；党的二十大报告")
    s.notes = "第一层最直接：看制度文本。中国宪法第一条就说，社会主义制度是中华人民共和国的根本制度。所以如果从正式制度身份来看，中国并没有把社会主义拿掉。二十大报告里也把中国式现代化表述为中国共产党领导的社会主义现代化。这是判断的第一块地基。"
    slides.append(s)

    s = Slide("但中国走的不是老式计划经济，而是社会主义市场经济", "04 关键区别", bg="F4F1EA")
    s.text("很多人困惑，是因为把“社会主义”直接等同于“没有市场”。但中国官方理论中的核心概念，恰恰叫“社会主义市场经济”。", 0.78, 1.35, 8.6, 0.44, 10.5, MUTED)
    s.card(0.85, 2.05, 3.45, 2.7, "老式计划经济印象", "价格主要由计划决定\n企业缺少竞争压力\n资源主要靠行政分配\n消费选择相对有限", RED)
    s.card(4.95, 2.05, 3.45, 2.7, "中国现实机制", "市场决定很多价格\n企业之间激烈竞争\n资本和技术参与创新\n政府保留战略引导", BLUE)
    s.card(9.05, 2.05, 3.45, 2.7, "社会主义市场经济", "市场是工具\n发展是目标\n公共利益是约束\n共同富裕是方向", GREEN)
    s.rect(1.0, 5.65, 11.2, 0.6, INK, radius=True, line=False)
    s.text("所以，中国不是没有市场的社会主义，而是把市场嵌入社会主义制度目标之中。", 1.18, 5.87, 10.82, 0.18, 9.4, WHITE, bold=True, align="ctr")
    s.footer("资料来源：二十届三中全会《决定》关于高水平社会主义市场经济体制的表述")
    s.notes = "第二层要解决一个常见误解：社会主义不等于只能是计划经济。中国改革开放以后，一个关键创造就是社会主义市场经济。通俗讲，市场不是被取消，而是被当成提高效率的工具；但它不是最高目标。最高目标仍然被表述为发展、人民生活改善和共同富裕。"
    slides.append(s)

    s = Slide(bg=DARK, dark=True, transition="fade")
    s.image(STATE_MARKET, 0, 0, LAYOUT_W, LAYOUT_H)
    s.rect(0, 0, LAYOUT_W, LAYOUT_H, "04101B", alpha=62000, line=False)
    s.text("国家与市场", 0.72, 1.36, 4.5, 0.42, 15, GOLD, bold=True)
    s.text("不是二选一，\n而是边界与分工", 0.72, 1.92, 5.0, 1.0, 27, WHITE, bold=True)
    s.text("市场解决效率和活力，国家解决方向、底线和长期投入。", 0.76, 3.26, 5.4, 0.44, 11, "E5EDF7")
    s.notes = "这一页是过渡。我们不要把国家和市场理解成一对非此即彼的概念。现实中的中国模式，是市场负责很多资源配置和效率竞争，国家负责战略方向、公共服务、基础设施、风险底线和长期目标。争议往往不在于要不要市场，而在于国家和市场的边界怎么划。"
    slides.append(s)

    s = Slide("国家与市场的关系：市场有活力，但不能失去公共方向", "05 机制", bg="F6F2E9")
    s.rect(0.8, 1.56, 11.7, 1.0, INK, radius=True, line=False)
    s.text("市场像发动机：负责提高效率、发现价格、激励创新。", 1.15, 1.88, 5.25, 0.18, 10, WHITE, bold=True)
    s.text("国家像方向盘和刹车：负责战略投入、公共服务、风险约束。", 6.65, 1.88, 5.2, 0.18, 10, "F1D58E", bold=True)
    pairs = [
        ("市场发挥作用", "价格、竞争、创新、消费者选择", BLUE),
        ("政府发挥作用", "产业规划、基础设施、公共服务、宏观调控", RED),
        ("共同目标", "发展生产力，同时防止发展成果被少数人独占", GREEN),
    ]
    for i, (t, b, c) in enumerate(pairs):
        s.card(0.9 + i * 4.0, 3.08, 3.45, 1.45, t, b, c)
    s.text("外行人可以这样理解：不是不用市场，而是不让市场变成唯一的裁判。", 1.2, 5.65, 10.7, 0.28, 14, INK, bold=True, align="ctr")
    s.footer()
    s.notes = "为了让非专业听众听懂，我会说：市场像发动机，它能让车跑起来，而且跑得快；政府像方向盘和刹车，它决定往哪里跑，什么时候降速，哪些地方不能冲过去。中国模式的核心，不是不要发动机，而是不让发动机自己决定目的地。"
    slides.append(s)

    s = Slide("所有制结构：公有制主体 + 多种所有制共同发展", "06 所有制", bg=DARK, dark=True, transition="push")
    s.rect(0.8, 1.55, 5.65, 4.15, "101B2A", radius=True, line=True, line_color="2B394B")
    s.text("公有制经济", 1.12, 1.92, 2.4, 0.26, 15, GOLD, bold=True)
    s.text("承担基础行业、公共服务、战略安全、长期投资等功能。", 1.15, 2.55, 4.7, 0.52, 10, "D7E0EA")
    s.pill("国有资本", 1.15, 3.52, 1.18, RED)
    s.pill("基础设施", 2.55, 3.52, 1.22, BLUE)
    s.pill("能源通信", 3.98, 3.52, 1.22, GREEN)
    s.rect(6.9, 1.55, 5.65, 4.15, "101B2A", radius=True, line=True, line_color="2B394B")
    s.text("非公有制经济", 7.22, 1.92, 2.8, 0.26, 15, TEAL, bold=True)
    s.text("提供大量就业、创新、税收和消费供给，是社会主义市场经济的重要组成部分。", 7.25, 2.55, 4.72, 0.56, 10, "D7E0EA")
    s.pill("民营企业", 7.25, 3.52, 1.2, TEAL)
    s.pill("外资企业", 8.68, 3.52, 1.2, GOLD)
    s.pill("平台经济", 10.1, 3.52, 1.2, BLUE)
    s.text("重点不是“只有一种所有制”，而是不同所有制被放进同一个国家发展目标中。", 1.2, 6.18, 10.9, 0.24, 12.5, WHITE, bold=True, align="ctr")
    s.footer("资料来源：宪法及社会主义市场经济相关政策表述；民营经济公开政策文件")
    s.notes = "再看所有制。传统想象里，社会主义好像只能有国有经济。但中国的制度表达是公有制为主体、多种所有制经济共同发展。也就是说，国企、民企、外资都存在，而且都发挥作用。区别在于，关键领域和战略底线由公有制经济承担更多责任，民营经济则提供大量就业、创新和活力。"
    slides.append(s)

    s = Slide(bg=DARK, dark=True, transition="fade")
    s.image(COMMON, 0, 0, LAYOUT_W, LAYOUT_H)
    s.rect(0, 0, LAYOUT_W, LAYOUT_H, "06111D", alpha=65000, line=False)
    s.text("社会主义最终看什么？", 0.72, 1.32, 5.5, 0.42, 15, GOLD, bold=True)
    s.text("看发展成果\n如何分配", 0.72, 1.92, 5.1, 1.05, 28, WHITE, bold=True)
    s.text("不是只看 GDP 增长，而是看普通人的教育、医疗、住房、就业和社会保障。", 0.76, 3.35, 5.3, 0.55, 11, "E5EDF7")
    s.notes = "这一页把问题带到更本质的位置：社会主义最后看什么？不是只看有没有国企，也不是只看有没有市场，而是看发展成果怎么分配。一个国家增长很快，如果大多数人没有安全感、没有公共服务、没有上升机会，那就很难说它实现了社会主义的价值目标。"
    slides.append(s)

    s = Slide("共同富裕不是平均主义，而是防止发展成果过度集中", "07 分配目标", bg="F6F2E9")
    s.text("“共同富裕”常被误解为平均分配。更准确地说，它强调在允许差异和激励效率的同时，通过制度安排缩小过大差距，扩大中等收入群体。", 0.8, 1.35, 8.9, 0.52, 10.3, MUTED)
    steps = [
        ("做大蛋糕", "发展生产力，保持创新和企业活力", BLUE),
        ("分好蛋糕", "税收、社保、公共服务、转移支付", RED),
        ("托住底线", "教育、医疗、养老、住房、就业保障", GREEN),
        ("限制失序", "反垄断、防止资本无序扩张、金融风险防控", GOLD),
    ]
    for i, (t, b, c) in enumerate(steps):
        x = 0.85 + i * 3.03
        s.rect(x, 2.45, 2.45, 2.8, PAPER, radius=True, line=True, line_color=LINE)
        s.text(f"{i+1}", x + 0.2, 2.72, 0.3, 0.22, 12, c, bold=True)
        s.text(t, x + 0.56, 2.72, 1.4, 0.24, 11, INK, bold=True)
        s.text(b, x + 0.28, 3.45, 1.9, 0.58, 8.4, MUTED, align="ctr")
    s.rect(1.0, 5.9, 11.1, 0.46, INK, radius=True, line=False)
    s.text("通俗地说：允许有人先富、也鼓励创造财富，但不能让社会变成少数人独占机会。", 1.22, 6.07, 10.6, 0.13, 8.5, WHITE, bold=True, align="ctr")
    s.footer("资料来源：共同富裕相关官方政策表述；财政部公开财政支出资料")
    s.notes = "共同富裕不是大家收入完全一样。它更像一个平衡：一方面要继续做大蛋糕，鼓励创新和企业活力；另一方面要通过教育、医疗、社保、住房保障、税收等制度，把底线托住，把机会尽量打开，把过大的差距慢慢压下来。"
    slides.append(s)

    s = Slide("现实中为什么会有人怀疑？因为矛盾确实存在", "08 现实矛盾", bg="F7F3EA")
    doubts = [
        ("收入差距", "地区、城乡、行业、资产差距仍然明显。", RED),
        ("资本扩张", "平台经济、房地产和金融领域曾出现高杠杆与垄断问题。", GOLD),
        ("公共服务不均衡", "优质教育、医疗、养老资源仍有区域差异。", BLUE),
        ("就业压力", "青年就业、产业转型和技能错配带来新的焦虑。", TEAL),
        ("地方财政压力", "公共服务和债务约束之间存在张力。", GREEN),
        ("国际竞争", "外部技术限制和贸易摩擦加大政策选择难度。", INK),
    ]
    for i, (t, b, c) in enumerate(doubts):
        s.card(0.8 + (i % 3) * 4.05, 1.48 + (i // 3) * 1.68, 3.62, 1.08, t, b, c)
    s.text("承认矛盾，不等于否定方向；关键要看制度如何回应矛盾。", 1.15, 5.65, 10.8, 0.3, 15, INK, bold=True, align="ctr")
    s.footer()
    s.notes = "那为什么很多人会怀疑？因为现实矛盾确实存在，比如收入差距、就业压力、公共服务不均衡、资本扩张、地方财政压力等。这些问题不能回避。但判断一条道路，不是看它有没有矛盾，而是看它怎样处理矛盾。一个制度如果不断调整政策去回应这些问题，说明它的方向和现实之间存在张力，也存在修正机制。"
    slides.append(s)

    s = Slide("从近年政策看，调节方向更强调安全、秩序和公共目标", "09 政策信号", bg=DARK, dark=True)
    signals = [
        ("高水平社会主义市场经济体制", "强调市场机制，也强调制度建设和宏观治理", TEAL),
        ("民营经济促进", "承认民营经济的重要作用，稳定预期和法治保障", GOLD),
        ("反垄断与平台治理", "不是反市场，而是防止市场支配力失控", RED),
        ("科技自立自强", "把关键技术和产业安全上升为长期战略", BLUE),
        ("民生与公共服务", "财政支出长期覆盖教育、社保、卫生等领域", GREEN),
    ]
    for i, (t, b, c) in enumerate(signals):
        y = 1.45 + i * 0.82
        s.rect(1.05, y, 0.18, 0.18, c, radius=True, line=False)
        s.text(t, 1.45, y - 0.05, 3.2, 0.2, 10, WHITE, bold=True)
        s.text(b, 4.85, y - 0.04, 6.3, 0.18, 8.2, "C6D0DD")
    s.rect(0.95, 6.05, 11.2, 0.48, "F3E2B6", radius=True, line=False)
    s.text("政策重心正在从“单纯追求速度”转向“发展质量、风险底线和长期安全”。", 1.2, 6.22, 10.65, 0.14, 8.5, INK, bold=True, align="ctr")
    s.footer("资料来源：二十届三中全会《决定》、民营经济促进相关政策、财政部公开资料")
    s.notes = "近几年政策信号也能帮助我们理解。中国并没有否定市场，相反还在强调高水平社会主义市场经济体制，也在出台政策支持民营经济。但同时，平台治理、反垄断、金融风险防控、科技自立自强这些政策也说明，国家更强调秩序、安全和公共目标。"
    slides.append(s)

    s = Slide("所以答案不是简单的“像不像”，而是“按哪个标准判断”", "10 结论推导", bg="F5F1E8")
    rows = [
        ("如果按计划经济标准", "不像", "因为中国广泛使用市场、企业竞争和资本机制。", RED),
        ("如果按西方资本主义标准", "也不像", "因为国家保留强战略能力，并强调公有制、党的领导和共同富裕。", BLUE),
        ("如果按中国特色社会主义标准", "仍在走", "因为制度方向、发展目标和政策表述仍然围绕社会主义展开。", GREEN),
    ]
    for i, (a, b, c, col) in enumerate(rows):
        y = 1.7 + i * 1.28
        s.rect(0.95, y, 11.1, 0.82, PAPER, radius=True, line=True, line_color=LINE)
        s.text(a, 1.25, y + 0.26, 2.5, 0.16, 8.6, INK, bold=True)
        s.text(b, 4.3, y + 0.18, 1.08, 0.24, 14, col, bold=True, align="ctr")
        s.text(c, 5.85, y + 0.25, 5.65, 0.17, 8.2, MUTED)
    s.text("最准确的表述：不是传统计划经济式社会主义，而是中国特色社会主义市场经济道路。", 1.05, 5.85, 11.0, 0.32, 15, INK, bold=True, align="ctr")
    s.footer()
    s.notes = "现在我们就能给出比较清楚的回答。如果你把社会主义理解成老式计划经济，那中国当然不像；如果你把中国理解成完全西方式资本主义，它也不像。更准确的说法是：中国走的是中国特色社会主义道路，也就是在社会主义制度框架下使用市场经济工具。"
    slides.append(s)

    s = Slide("一句话回答：还在走，但走法已经不是旧模板", "11 最终判断", bg=DARK, dark=True, transition="fade")
    s.text("还在走", 0.85, 1.55, 2.65, 0.55, 28, GOLD, bold=True)
    s.text("但不是用计划经济的旧方式走。", 3.6, 1.82, 5.4, 0.28, 14, WHITE, bold=True)
    s.line(0.9, 2.65, 10.8, GOLD, 0.018)
    s.card(0.95, 3.15, 3.4, 1.42, "方向", "制度文本、政治领导和现代化目标仍明确指向社会主义。", RED, dark=True)
    s.card(4.85, 3.15, 3.4, 1.42, "方法", "通过市场经济、企业竞争和开放合作提高效率。", TEAL, dark=True)
    s.card(8.75, 3.15, 3.4, 1.42, "约束", "通过公共目标、国家调节和共同富裕防止失序。", GOLD, dark=True)
    s.text("真正值得讨论的，不是“有没有市场”，而是市场能否长期服务于公共目标。", 1.0, 5.7, 11.2, 0.28, 14, WHITE, bold=True, align="ctr")
    s.footer()
    s.notes = "所以我的最终回答是：还在走，但不是用旧模板走。它不是传统计划经济式的社会主义，而是中国特色社会主义市场经济道路。真正值得讨论的问题，不是中国有没有市场，而是市场能不能长期服务于公共目标，发展成果能不能更多、更公平地回到人民生活中。"
    slides.append(s)

    s = Slide("给听众留下的三个问题", "12 收束", bg="F6F2E9")
    qs = [
        ("1", "发展速度和公平分配，如何继续平衡？", RED),
        ("2", "政府有为和市场有效，边界如何更清楚？", BLUE),
        ("3", "共同富裕如何从理念转化为可感知的生活改善？", GREEN),
    ]
    for i, (num, q, c) in enumerate(qs):
        s.rect(1.1, 1.7 + i * 1.2, 10.9, 0.76, PAPER, radius=True, line=True, line_color=LINE)
        s.rect(1.42, 1.94 + i * 1.2, 0.32, 0.32, c, radius=True, line=False)
        s.text(num, 1.5, 2.03 + i * 1.2, 0.16, 0.1, 7.2, WHITE, bold=True, align="ctr")
        s.text(q, 2.05, 1.93 + i * 1.2, 8.6, 0.2, 12.5, INK, bold=True)
    s.rect(1.1, 5.6, 10.9, 0.62, INK, radius=True, line=False)
    s.text("判断道路，最终要回到人民生活：机会是否更多，底线是否更稳，未来是否更有确定性。", 1.35, 5.83, 10.4, 0.16, 9, WHITE, bold=True, align="ctr")
    s.footer()
    s.notes = "最后我建议把讨论落到三个问题：第一，怎样继续平衡效率和公平？第二，有为政府和有效市场的边界怎样更清楚？第三，共同富裕怎样变成普通人能感受到的教育、医疗、住房、就业和养老改善？这三个问题，比一句简单的标签更重要。"
    slides.append(s)

    s = Slide("资料来源与说明", "Appendix", bg="F8F5ED")
    sources = [
        "《中华人民共和国宪法》：关于社会主义制度、党的领导和国家制度的基本表述。",
        "党的二十大报告：关于中国式现代化、中国特色社会主义和共同富裕的表述。",
        "二十届三中全会《决定》：关于高水平社会主义市场经济体制、进一步全面深化改革的表述。",
        "财政部公开财政收支资料：教育、社会保障和就业、卫生健康等公共支出信息。",
        "民营经济促进相关公开政策：关于民营经济在社会主义市场经济中的地位和法治保障。",
    ]
    for i, src in enumerate(sources):
        s.rect(0.9, 1.5 + i * 0.72, 0.22, 0.22, RED if i % 2 == 0 else GOLD, radius=True, line=False)
        s.text(src, 1.28, 1.45 + i * 0.72, 10.7, 0.28, 8.6, INK)
    s.card(0.95, 5.55, 11.0, 0.8, "说明", "本稿为公开资料基础上的通俗化政治经济分析，用于课堂、讨论或汇报场景；核心目标是帮助非专业听众理解概念与判断框架。", BLUE)
    s.footer("生成时间：2026-05-13")
    s.notes = "这一页是资料说明。整个演示尽量不使用过度专业的理论语言，而是把公开制度文本、官方政策和现实经济机制放在一起解释。目的不是替任何一句口号背书，而是让听众知道应该用什么标准理解这个问题。"
    slides.append(s)

    return slides


def apply_motion_pacing(slides: list[Slide]):
    """Give the deck a deliberate rhythm: varied transitions and denser in-slide builds."""
    for i, slide in enumerate(slides):
        slide.transition = TRANSITION_SEQUENCE[i % len(TRANSITION_SEQUENCE)]


def write_speaker_script(slides: list[Slide]):
    lines = ["# 中国道路再理解：口语化演讲稿", "", "建议演讲时长：12-18 分钟。语气建议：解释型、克制、有判断但不绝对化。", ""]
    for i, slide in enumerate(slides, start=1):
        title = "封面" if i == 1 else f"第 {i} 页"
        lines.append(f"## {title}")
        lines.append("")
        lines.append(slide.notes.strip())
        lines.append("")
    SCRIPT_OUT.write_text("\n".join(lines), encoding="utf-8")


def package(slides: list[Slide]):
    tmp = OUT.parent / "_socialism_pptx_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    for p in [
        tmp / "_rels",
        tmp / "docProps",
        tmp / "ppt" / "_rels",
        tmp / "ppt" / "slides" / "_rels",
        tmp / "ppt" / "notesSlides" / "_rels",
        tmp / "ppt" / "notesMasters" / "_rels",
        tmp / "ppt" / "slideMasters" / "_rels",
        tmp / "ppt" / "slideLayouts" / "_rels",
        tmp / "ppt" / "theme",
        tmp / "ppt" / "media",
    ]:
        p.mkdir(parents=True, exist_ok=True)

    media = [COVER, STATE_MARKET, COMMON]
    for m in media:
        shutil.copy2(m, tmp / "ppt" / "media" / m.name)

    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, len(slides) + 1):
        overrides.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
        overrides.append(f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>')
    (tmp / "[Content_Types].xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>{''.join(overrides)}</Types>""",
        encoding="utf-8",
    )
    (tmp / "_rels" / ".rels").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>""",
        encoding="utf-8",
    )
    (tmp / "docProps" / "core.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>中国道路再理解：是否还在走社会主义</dc:title><dc:creator>Codex</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">2026-05-13T00:00:00Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2026-05-13T00:00:00Z</dcterms:modified></cp:coreProperties>""",
        encoding="utf-8",
    )
    (tmp / "docProps" / "app.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application><PresentationFormat>宽屏</PresentationFormat><Slides>{len(slides)}</Slides><Notes>{len(slides)}</Notes></Properties>""",
        encoding="utf-8",
    )

    sld_ids = []
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    for i in range(1, len(slides) + 1):
        rid = f"rId{i+1}"
        sld_ids.append(f'<p:sldId id="{255+i}" r:id="{rid}"/>')
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>')
    (tmp / "ppt" / "presentation.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{''.join(sld_ids)}</p:sldIdLst><p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle><a:defPPr><a:defRPr lang="zh-CN"/></a:defPPr></p:defaultTextStyle></p:presentation>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "_rels" / "presentation.xml.rels").write_text(
        f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "slideMasters" / "slideMaster1.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "slideMasters" / "_rels" / "slideMaster1.xml.rels").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "slideLayouts" / "slideLayout1.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "slideLayouts" / "_rels" / "slideLayout1.xml.rels").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "notesMasters" / "notesMaster1.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:notesMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:notesMaster>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "notesMasters" / "_rels" / "notesMaster1.xml.rels").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>""",
        encoding="utf-8",
    )
    (tmp / "ppt" / "theme" / "theme1.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Premium Civic"><a:themeElements><a:clrScheme name="Premium Civic"><a:dk1><a:srgbClr val="15202B"/></a:dk1><a:lt1><a:srgbClr val="F4F1EA"/></a:lt1><a:dk2><a:srgbClr val="07111D"/></a:dk2><a:lt2><a:srgbClr val="FFFFFF"/></a:lt2><a:accent1><a:srgbClr val="B91C1C"/></a:accent1><a:accent2><a:srgbClr val="D6A13B"/></a:accent2><a:accent3><a:srgbClr val="00A6A6"/></a:accent3><a:accent4><a:srgbClr val="2563EB"/></a:accent4><a:accent5><a:srgbClr val="16825D"/></a:accent5><a:accent6><a:srgbClr val="697586"/></a:accent6><a:hlink><a:srgbClr val="2563EB"/></a:hlink><a:folHlink><a:srgbClr val="B91C1C"/></a:folHlink></a:clrScheme><a:fontScheme name="Microsoft YaHei"><a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface="Microsoft YaHei"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/><a:ea typeface="Microsoft YaHei"/></a:minorFont></a:fontScheme><a:fmtScheme name="Premium"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>""",
        encoding="utf-8",
    )

    for i, slide in enumerate(slides, start=1):
        (tmp / "ppt" / "slides" / f"slide{i}.xml").write_text(slide.xml(), encoding="utf-8")
        (tmp / "ppt" / "slides" / "_rels" / f"slide{i}.xml.rels").write_text(slide.rels_xml(i), encoding="utf-8")
        (tmp / "ppt" / "notesSlides" / f"notesSlide{i}.xml").write_text(notes_xml(slide.notes), encoding="utf-8")
        (tmp / "ppt" / "notesSlides" / "_rels" / f"notesSlide{i}.xml.rels").write_text(notes_rels_xml(i), encoding="utf-8")

    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for file in tmp.rglob("*"):
            if file.is_file():
                z.write(file, file.relative_to(tmp).as_posix())
    shutil.rmtree(tmp)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    slides = build_slides()
    apply_motion_pacing(slides)
    write_speaker_script(slides)
    package(slides)
    print(f"created: {OUT}")
    print(f"speaker_script: {SCRIPT_OUT}")
    print(f"slides: {len(slides)}")
    print(f"size: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
