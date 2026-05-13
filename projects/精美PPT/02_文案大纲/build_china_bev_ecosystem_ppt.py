from __future__ import annotations

import html
import os
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "04_素材资产" / "china_bev_ecosystem_cover.png"
OUT = ROOT / "05_源文件PPT" / "中国纯电汽车行业生态分析.pptx"

SLIDE_W = 12192000
SLIDE_H = 6858000
LAYOUT_W = 13.333
LAYOUT_H = 7.5
EMU_PER_IN = 914400

BG = "F7F5EF"
INK = "17212B"
MUTED = "66717F"
LINE = "D8D5CB"
WHITE = "FFFFFF"
TEAL = "00A6A6"
BLUE = "2563EB"
GREEN = "22A06B"
AMBER = "D99A1E"
RED = "C2413A"
DARK = "111827"
CARD = "FFFFFF"


def emu(v: float) -> int:
    return int(v * EMU_PER_IN)


def esc(s: str) -> str:
    return html.escape(str(s), quote=False)


class Slide:
    def __init__(self, title: str | None = None, section: str | None = None, dark: bool = False):
        self.parts: list[str] = []
        self.rels: list[tuple[str, str, str]] = []
        self.next_id = 2
        self.next_rel = 1
        self.dark = dark
        self.bg(DARK if dark else BG)
        if section or title:
            color = WHITE if dark else INK
            if section:
                self.text(section, 0.58, 0.34, 2.3, 0.24, 8, TEAL if not dark else "7CE4E4", bold=True)
            if title:
                self.text(title, 0.58, 0.56, 8.8, 0.42, 18, color, bold=True)
                self.rect(0.58, 1.08, 1.0, 0.03, TEAL if not dark else "7CE4E4", line=False)

    def rid(self) -> str:
        r = f"rId{self.next_rel}"
        self.next_rel += 1
        return r

    def sid(self) -> int:
        i = self.next_id
        self.next_id += 1
        return i

    def bg(self, color: str):
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{self.sid()}" name="Background"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>"""
        )

    def rect(self, x, y, w, h, fill, alpha: int | None = None, radius: bool = False, line=True, line_color=LINE, line_w=1):
        alpha_xml = f'<a:alpha val="{alpha}"/>' if alpha else ""
        ln = f'<a:ln w="{int(line_w*12700)}"><a:solidFill><a:srgbClr val="{line_color}"/></a:solidFill></a:ln>' if line else "<a:ln><a:noFill/></a:ln>"
        geom = "roundRect" if radius else "rect"
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{self.sid()}" name="Shape"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}">{alpha_xml}</a:srgbClr></a:solidFill>{ln}</p:spPr>
<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>"""
        )

    def line(self, x, y, w, color=LINE, thickness=0.015):
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
        font="Microsoft YaHei",
        alpha: int | None = None,
        break_lines: bool = True,
    ):
        paras = str(s).split("\n") if break_lines else [str(s)]
        p_xml = []
        for idx, para in enumerate(paras):
            if para == "":
                para = " "
            alpha_xml = f'<a:alpha val="{alpha}"/>' if alpha else ""
            p_xml.append(
                f"""<a:p><a:pPr algn="{align}"/><a:r><a:rPr lang="zh-CN" sz="{int(size*100)}" b="{1 if bold else 0}"><a:solidFill><a:srgbClr val="{color}">{alpha_xml}</a:srgbClr></a:solidFill><a:latin typeface="{font}"/><a:ea typeface="{font}"/></a:rPr><a:t>{esc(para)}</a:t></a:r></a:p>"""
            )
        anchor = {"top": "t", "mid": "ctr", "bottom": "b"}.get(valign, "t")
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{self.sid()}" name="Text"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr wrap="square" anchor="{anchor}"><a:spAutoFit/></a:bodyPr><a:lstStyle/>{''.join(p_xml)}</p:txBody></p:sp>"""
        )

    def pill(self, s, x, y, w, h, fill, color=WHITE):
        self.rect(x, y, w, h, fill, radius=True, line=False)
        self.text(s, x + 0.08, y + 0.045, w - 0.16, h - 0.07, 8, color, bold=True, align="ctr", valign="mid")

    def image(self, path: Path, x, y, w, h):
        rid = self.rid()
        target = f"../media/{path.name}"
        self.rels.append((rid, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", target))
        self.parts.append(
            f"""<p:pic><p:nvPicPr><p:cNvPr id="{self.sid()}" name="{esc(path.name)}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>
<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>"""
        )

    def card(self, x, y, w, h, title, body, accent=TEAL):
        self.rect(x, y, w, h, CARD, radius=True, line=True, line_color="E7E2D8")
        self.rect(x, y, 0.06, h, accent, line=False)
        self.text(title, x + 0.22, y + 0.18, w - 0.35, 0.3, 11, INK, bold=True)
        self.text(body, x + 0.22, y + 0.58, w - 0.35, h - 0.7, 8.4, MUTED)

    def stat(self, label, value, note, x, y, w, accent=TEAL):
        self.rect(x, y, w, 1.02, WHITE, radius=True, line=True, line_color="E8E1D6")
        self.text(value, x + 0.18, y + 0.14, w - 0.28, 0.33, 18, accent, bold=True)
        self.text(label, x + 0.18, y + 0.5, w - 0.28, 0.22, 8.8, INK, bold=True)
        self.text(note, x + 0.18, y + 0.73, w - 0.28, 0.18, 6.8, MUTED)

    def footer(self, source: str = "资料来源：公开资料整理；中汽协、国家能源局、IEA、企业公开信息等"):
        self.text(source, 0.58, 7.06, 9.6, 0.18, 5.8, "8A929C")
        self.text("中国纯电汽车行业生态分析", 10.7, 7.06, 1.95, 0.18, 5.8, "8A929C", align="r")

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{''.join(self.parts)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"""

    def rels_xml(self) -> str:
        rels = ['<Relationship Id="rIdLayout" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>']
        for rid, typ, target in self.rels:
            rels.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>')
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>"""


def add_bars(slide: Slide, values, labels, x, y, w, h, colors):
    max_v = max(values)
    bar_h = h / len(values) * 0.44
    gap = h / len(values) * 0.56
    for i, (v, lab) in enumerate(zip(values, labels)):
        yy = y + i * (bar_h + gap)
        slide.text(lab, x, yy - 0.01, 1.55, 0.22, 7.2, INK, bold=True)
        slide.rect(x + 1.72, yy, w - 2.2, bar_h, "E6E4DC", radius=True, line=False)
        slide.rect(x + 1.72, yy, (w - 2.2) * v / max_v, bar_h, colors[i % len(colors)], radius=True, line=False)
        slide.text(f"{v:g}", x + w - 0.42, yy - 0.02, 0.42, 0.22, 7, INK, bold=True, align="r")


def add_matrix(slide: Slide, x, y, w, h):
    slide.rect(x, y, w, h, WHITE, radius=True, line=True, line_color="E5DED2")
    slide.line(x + 0.22, y + h / 2, w - 0.44, "D7D2C8", 0.012)
    slide.rect(x + w / 2, y + 0.22, 0.012, h - 0.44, "D7D2C8", line=False)
    slide.text("技术/智能化高", x + w / 2 - 0.65, y + 0.1, 1.3, 0.18, 6.8, MUTED, align="ctr")
    slide.text("规模/成本强", x + w - 0.9, y + h - 0.26, 0.75, 0.18, 6.8, MUTED, align="r")
    points = [
        ("比亚迪", 0.78, 0.70, GREEN),
        ("特斯拉中国", 0.72, 0.78, BLUE),
        ("吉利/极氪", 0.58, 0.64, TEAL),
        ("小鹏", 0.48, 0.76, TEAL),
        ("蔚来", 0.42, 0.69, BLUE),
        ("上汽/五菱", 0.64, 0.38, AMBER),
        ("小米汽车", 0.36, 0.66, RED),
        ("长安/深蓝", 0.50, 0.52, GREEN),
    ]
    for name, px, py, c in points:
        cx = x + 0.45 + px * (w - 1.0)
        cy = y + 0.45 + (1 - py) * (h - 0.9)
        slide.rect(cx - 0.05, cy - 0.05, 0.1, 0.1, c, radius=True, line=False)
        slide.text(name, cx + 0.07, cy - 0.08, 1.0, 0.17, 6.5, INK)


def ecosystem_slide() -> Slide:
    s = Slide("纯电生态由“车”延展为“能源 + 软件 + 服务”系统", "03 生态地图")
    cols = [
        ("上游资源", ["锂 / 镍 / 钴 / 石墨", "电池材料", "功率半导体", "车规芯片"], GREEN),
        ("核心部件", ["动力电池", "电驱电控", "热管理", "域控 / 传感器"], TEAL),
        ("整车制造", ["平台架构", "三电集成", "智能座舱", "辅助驾驶"], BLUE),
        ("流通服务", ["直营/经销", "金融保险", "二手车", "售后维保"], AMBER),
        ("能源网络", ["公共充电", "超充/换电", "V2G", "储能协同"], RED),
    ]
    x0 = 0.65
    for i, (title, items, color) in enumerate(cols):
        x = x0 + i * 2.45
        s.rect(x, 1.55, 2.08, 4.55, WHITE, radius=True, line=True, line_color="E5DED2")
        s.rect(x, 1.55, 2.08, 0.16, color, line=False)
        s.text(title, x + 0.2, 1.88, 1.65, 0.25, 11, INK, bold=True, align="ctr")
        for j, item in enumerate(items):
            yy = 2.42 + j * 0.72
            s.rect(x + 0.22, yy, 1.64, 0.38, "F3F1EA", radius=True, line=False)
            s.text(item, x + 0.32, yy + 0.1, 1.44, 0.14, 7.2, INK, align="ctr")
        if i < len(cols) - 1:
            s.text("→", x + 2.12, 3.47, 0.25, 0.28, 18, "9AA3AE", bold=True, align="ctr")
    s.card(0.7, 6.18, 5.7, 0.58, "生态控制点", "电池成本、电子电气架构、补能网络、数据闭环与品牌渠道正在决定长期议价能力。", TEAL)
    s.card(6.7, 6.18, 5.9, 0.58, "行业本质", "竞争已从单车性能转向“制造效率 + 软件体验 + 能源服务 + 生命周期运营”的组合战。", BLUE)
    s.footer()
    return s


def build_slides() -> list[Slide]:
    slides: list[Slide] = []

    s = Slide(dark=True)
    s.image(ASSET, 0, 0, LAYOUT_W, LAYOUT_H)
    s.rect(0, 0, 6.4, LAYOUT_H, "07111D", alpha=83000, line=False)
    s.text("中国纯电汽车行业\n生态分析", 0.72, 1.35, 5.55, 1.4, 28, WHITE, bold=True)
    s.text("China BEV Industry Ecosystem Analysis", 0.78, 2.86, 4.2, 0.26, 9, "B7F4F4")
    s.rect(0.78, 3.25, 1.02, 0.035, "7CE4E4", line=False)
    s.text("市场规模 · 产业链结构 · 竞争格局 · 能源网络 · 战略机会", 0.78, 3.55, 5.3, 0.35, 10.5, "E8EEF7")
    s.text("2026年5月", 0.78, 6.62, 2.0, 0.22, 8, "D4D8DE")
    slides.append(s)

    s = Slide("中国纯电车进入“规模化后半场”：增长还在，但胜负手转向生态效率", "01 执行摘要")
    takeaways = [
        ("市场重心", "中国已是全球最大电动车市场，2025 年新能源车产销均超过 1600 万辆，纯电产销超 1060 万辆；增量空间从渗透率提升转向结构升级。", GREEN),
        ("竞争逻辑", "价格战仍会持续，但单纯低价难以建立护城河；电池、平台化制造、软件体验、补能和渠道效率共同决定单位经济。", TEAL),
        ("生态边界", "车企正在向能源服务、保险金融、二手车、数据服务延伸；电池企业和充电运营商也在向整车体验靠近。", BLUE),
        ("战略判断", "未来 3-5 年，行业机会集中在高压快充、智能化平权、出海本地化、动力电池新技术和全生命周期运营。", AMBER),
    ]
    for i, (t, b, c) in enumerate(takeaways):
        s.card(0.75 + (i % 2) * 6.0, 1.55 + (i // 2) * 2.05, 5.55, 1.6, t, b, c)
    s.stat("2025 中国新能源车销量", "1600万+", "中汽协/新华社公开报道", 0.75, 5.85, 2.8, GREEN)
    s.stat("2025 中国纯电产销", "1060万+", "央视网公开报道", 3.8, 5.85, 2.8, TEAL)
    s.stat("全国充电设施规模", "2000万级", "国家能源局/央视网报道", 6.85, 5.85, 2.8, BLUE)
    s.stat("全球领先地位", "≈60%", "IEA：全球电动车销量中中国占比约六成", 9.9, 5.85, 2.8, AMBER)
    s.footer()
    slides.append(s)

    s = Slide("市场规模：纯电仍是主轴，但行业从“高速普及”转向“质量增长”", "02 市场概览")
    s.text("中国电动车市场已经完成从政策试点到大规模消费品的跃迁。2025 年新能源车产销均超 1600 万辆，其中纯电车型产销超 1060 万辆；后续增长将更依赖产品结构、补能体验和智能化价值。", 0.75, 1.35, 7.4, 0.62, 11, MUTED)
    s.stat("2025 新能源车产量", "1613万", "同比增长约 24%", 0.78, 2.25, 2.55, GREEN)
    s.stat("2025 新能源车销量", "1608万", "同比增长约 24%", 3.55, 2.25, 2.55, TEAL)
    s.stat("2025 纯电产销", "1060万+", "纯电是行业基本盘", 6.32, 2.25, 2.55, BLUE)
    s.stat("IEA 判断", "全球第一", "中国贡献全球电动车销量约六成", 9.09, 2.25, 2.55, AMBER)
    s.rect(0.85, 4.0, 5.9, 2.0, WHITE, radius=True, line=True, line_color="E5DED2")
    s.text("增长驱动从数量转向结构", 1.1, 4.22, 2.7, 0.22, 11, INK, bold=True)
    add_bars(s, [1608, 1060, 430, 118], ["新能源销量", "纯电产销", "插混/增程", "出口承压变量"], 1.05, 4.72, 5.25, 1.0, [GREEN, TEAL, BLUE, AMBER])
    s.card(7.1, 4.0, 5.2, 0.95, "结构变化", "A00/A0 级代步车、10-20 万主流家庭车、30 万以上智能豪华车的竞争逻辑明显不同。", TEAL)
    s.card(7.1, 5.12, 5.2, 0.95, "纯电关键问题", "消费者不再只问续航，而是关注快充、冬季能耗、智能驾驶、保值率和服务网络。", BLUE)
    s.footer("资料来源：新华社、中汽协、央视网、IEA Global EV Outlook 2025；数值为公开报道口径整理")
    slides.append(s)

    slides.append(ecosystem_slide())

    s = Slide("价值链：利润池由硬件制造向电池、软件、能源和生命周期服务迁移", "04 价值链")
    stages = [
        ("资源/材料", "锂、镍、石墨\n正负极、隔膜、电解液", "成本波动"),
        ("电池系统", "电芯、BMS、热管理\nCTP/刀片/麒麟等结构创新", "核心议价"),
        ("整车平台", "三电集成、平台化制造\n供应链协同", "规模效率"),
        ("智能化", "座舱、ADAS、OS、数据闭环", "体验溢价"),
        ("能源服务", "快充、换电、V2G、储能", "生态入口"),
        ("后市场", "保险、维修、二手车、回收", "长期利润"),
    ]
    for i, (a, b, c) in enumerate(stages):
        x = 0.65 + i * 2.05
        s.rect(x, 1.55, 1.72, 3.1, WHITE, radius=True, line=True, line_color="E5DED2")
        s.text(f"{i+1:02d}", x + 0.14, 1.78, 0.4, 0.22, 9, TEAL, bold=True)
        s.text(a, x + 0.14, 2.12, 1.34, 0.3, 10, INK, bold=True)
        s.text(b, x + 0.14, 2.68, 1.38, 0.82, 7.2, MUTED)
        s.pill(c, x + 0.18, 4.05, 1.25, 0.28, [GREEN, TEAL, BLUE, AMBER, RED, DARK][i])
        if i < len(stages) - 1:
            s.text("→", x + 1.76, 2.9, 0.24, 0.22, 15, "9AA3AE", bold=True)
    s.card(0.75, 5.18, 3.75, 0.95, "短期胜负手", "规模化降本、渠道效率、爆款车型节奏与库存控制。", GREEN)
    s.card(4.75, 5.18, 3.75, 0.95, "中期胜负手", "高压快充、智能化体验、平台复用和自研/外采边界管理。", TEAL)
    s.card(8.75, 5.18, 3.75, 0.95, "长期胜负手", "数据闭环、能源生态、品牌信任与海外本地化能力。", BLUE)
    s.footer()
    slides.append(s)

    s = Slide("竞争格局：头部规模优势显著，新势力和科技公司争夺体验心智", "05 竞争格局")
    s.text("横轴代表规模/成本能力，纵轴代表技术和智能化心智。位置为战略判断示意，不代表精确排名。", 0.75, 1.32, 7.3, 0.28, 8.5, MUTED)
    add_matrix(s, 0.9, 1.75, 7.2, 4.65)
    s.card(8.55, 1.75, 3.75, 0.9, "规模型玩家", "比亚迪、特斯拉中国、上汽/五菱等依靠制造效率、供应链和渠道覆盖建立成本优势。", GREEN)
    s.card(8.55, 2.88, 3.75, 0.9, "智能化玩家", "小鹏、蔚来、小米等更强调软件体验、用户运营和科技品牌心智。", TEAL)
    s.card(8.55, 4.01, 3.75, 0.9, "传统转型玩家", "吉利、长安、广汽、上汽等通过多品牌矩阵和平台化纯电架构追赶。", BLUE)
    s.card(8.55, 5.14, 3.75, 0.9, "行业含义", "纯电竞争已经不是单一车型竞争，而是研发节奏、供应链、现金流和服务体系的系统竞争。", AMBER)
    s.footer("资料来源：企业公开信息、乘用车市场公开报道；矩阵为分析示意")
    slides.append(s)

    s = Slide("电池生态：成本、性能和供应安全仍是纯电行业最硬约束", "06 电池与材料")
    s.text("动力电池是纯电车成本和性能的核心。中国形成了从材料、电芯、PACK 到回收的完整体系，宁德时代和比亚迪等企业在全球处于领先位置。", 0.75, 1.35, 7.8, 0.48, 10.5, MUTED)
    s.rect(0.85, 2.1, 5.3, 3.75, WHITE, radius=True, line=True, line_color="E5DED2")
    s.text("动力电池关键路线", 1.08, 2.32, 2.4, 0.24, 11, INK, bold=True)
    routes = [("LFP", "成本低、安全性高，主流市场基本盘", GREEN), ("三元锂", "高能量密度，仍服务高端和长续航", BLUE), ("钠离子", "低温和成本潜力，处于导入期", AMBER), ("固态/半固态", "下一代技术方向，量产仍需时间", RED)]
    for i, (t, b, c) in enumerate(routes):
        y = 2.85 + i * 0.67
        s.rect(1.08, y, 0.12, 0.12, c, radius=True, line=False)
        s.text(t, 1.3, y - 0.06, 0.95, 0.18, 8.5, INK, bold=True)
        s.text(b, 2.22, y - 0.06, 3.25, 0.18, 7.5, MUTED)
    s.rect(6.6, 2.1, 5.55, 3.75, WHITE, radius=True, line=True, line_color="E5DED2")
    s.text("生态分工", 6.85, 2.32, 2.2, 0.24, 11, INK, bold=True)
    flow = [("材料", GREEN), ("电芯", TEAL), ("PACK", BLUE), ("整车", AMBER), ("回收", RED)]
    for i, (label, color) in enumerate(flow):
        x = 6.9 + i * 1.02
        s.rect(x, 3.05, 0.72, 0.72, color, radius=True, line=False)
        s.text(label, x + 0.03, 3.28, 0.66, 0.15, 7.2, WHITE, bold=True, align="ctr")
        if i < len(flow) - 1:
            s.text("→", x + 0.77, 3.28, 0.18, 0.16, 11, "9AA3AE", bold=True)
    s.text("电池企业从供应商变成生态核心：\n影响整车成本、补能体验、残值评估与海外供应链合规。", 6.9, 4.35, 4.8, 0.58, 9, MUTED)
    s.card(0.85, 6.12, 11.3, 0.58, "判断", "纯电车企需要在自研、电池供应绑定、多供应商策略之间取得平衡；电池安全和回收闭环会成为品牌信任的一部分。", TEAL)
    s.footer("资料来源：IEA Global EV Outlook 2025、SNE Research公开报道、企业公开资料")
    slides.append(s)

    s = Slide("补能网络：充电基础设施扩张正在重塑用户体验和能源协同", "07 充电与能源")
    s.text("中国充电基础设施规模快速扩张，行业正在从“有没有桩”进入“快不快、稳不稳、利用率高不高”的阶段。", 0.75, 1.35, 7.9, 0.34, 10.5, MUTED)
    s.stat("全国充电设施", "2000万级", "截至 2025 年底公开报道", 0.85, 2.05, 2.9, GREEN)
    s.stat("公共补能方向", "超充化", "高压平台 + 液冷快充", 4.05, 2.05, 2.9, TEAL)
    s.stat("能源协同", "V2G", "车网互动与储能调峰", 7.25, 2.05, 2.9, BLUE)
    s.rect(0.85, 3.55, 11.25, 2.4, WHITE, radius=True, line=True, line_color="E5DED2")
    timeline = [("2020-2022", "建桩扩容", GREEN), ("2023-2025", "快充竞争", TEAL), ("2026-2028", "车网互动", BLUE), ("2029+", "能源运营", AMBER)]
    for i, (t, b, c) in enumerate(timeline):
        x = 1.25 + i * 2.65
        s.rect(x, 4.42, 1.35, 0.08, c, line=False)
        s.rect(x + 0.58, 4.24, 0.22, 0.22, c, radius=True, line=False)
        s.text(t, x - 0.15, 3.88, 1.65, 0.2, 8, INK, bold=True, align="ctr")
        s.text(b, x - 0.15, 4.76, 1.65, 0.2, 8, MUTED, align="ctr")
    s.card(0.85, 6.2, 5.35, 0.55, "车企机会", "超充网络可提升品牌体验和用户粘性，但重资产投入要求高利用率和选址能力。", TEAL)
    s.card(6.75, 6.2, 5.35, 0.55, "能源机会", "充电站未来会与储能、光伏、电力交易和城市能源管理更深融合。", BLUE)
    s.footer("资料来源：国家能源局、央视网、中国充电联盟公开报道")
    slides.append(s)

    s = Slide("技术栈：纯电平台成为智能化落地的最佳载体", "08 技术趋势")
    layers = [
        ("软件体验层", "智能座舱、语音、多屏互联、车载应用生态", BLUE),
        ("智能驾驶层", "感知、规控、城市NOA、端到端模型、数据闭环", TEAL),
        ("电子电气层", "中央计算、域控/区域控制、OTA、车云协同", GREEN),
        ("三电平台层", "电池、电驱、电控、热管理、高压快充", AMBER),
        ("制造平台层", "一体化压铸、模块化架构、柔性产线、质量控制", RED),
    ]
    for i, (t, b, c) in enumerate(layers):
        y = 1.55 + i * 0.82
        s.rect(1.0 + i * 0.2, y, 10.7 - i * 0.4, 0.56, c, alpha=88000, radius=True, line=False)
        s.text(t, 1.28 + i * 0.2, y + 0.14, 1.75, 0.17, 8.5, WHITE, bold=True)
        s.text(b, 3.15 + i * 0.2, y + 0.14, 7.7 - i * 0.4, 0.17, 8, WHITE)
    s.card(0.9, 5.98, 3.6, 0.68, "高压快充", "800V 平台与液冷超充改善里程焦虑，是纯电体验升级的硬指标。", TEAL)
    s.card(4.85, 5.98, 3.6, 0.68, "智能化平权", "从高端车型下放到 15-25 万主流市场，重塑配置预期。", BLUE)
    s.card(8.8, 5.98, 3.15, 0.68, "车云一体", "OTA、数据闭环和AI模型让车辆成为持续迭代产品。", GREEN)
    s.footer()
    slides.append(s)

    s = Slide("政策与外部环境：国内支持延续，海外贸易摩擦抬高出海门槛", "09 政策环境")
    s.card(0.85, 1.45, 3.65, 1.05, "国内政策", "新能源汽车购置税减免政策延续至 2027 年，地方促消费和以旧换新政策继续支撑需求。", GREEN)
    s.card(4.85, 1.45, 3.65, 1.05, "产业政策", "充电基础设施、智能网联汽车试点、动力电池回收和车网互动是政策重点方向。", TEAL)
    s.card(8.85, 1.45, 3.65, 1.05, "海外环境", "欧盟、美国等市场对中国电动车和电池供应链的贸易限制增加，倒逼本地化生产。", RED)
    s.rect(1.0, 3.3, 11.05, 2.25, WHITE, radius=True, line=True, line_color="E5DED2")
    s.text("政策影响传导", 1.25, 3.55, 2.0, 0.24, 11, INK, bold=True)
    chain = [("税费减免", GREEN), ("消费刺激", TEAL), ("基础设施", BLUE), ("产业标准", AMBER), ("出海合规", RED)]
    for i, (label, color) in enumerate(chain):
        x = 1.35 + i * 2.1
        s.rect(x, 4.18, 1.28, 0.48, color, radius=True, line=False)
        s.text(label, x + 0.08, 4.34, 1.12, 0.14, 7.5, WHITE, bold=True, align="ctr")
        if i < len(chain) - 1:
            s.text("→", x + 1.42, 4.32, 0.25, 0.14, 12, "9AA3AE", bold=True)
    s.text("结论：政策红利不再是单纯补贴，而是通过税费、基础设施、标准和国际规则塑造行业边界。", 1.25, 5.04, 9.8, 0.22, 8.5, MUTED)
    s.footer("资料来源：财政部、税务总局、工信部、国家能源局、公开贸易政策报道")
    slides.append(s)

    s = Slide("风险：价格战、盈利压力和海外壁垒将考验生态韧性", "10 主要风险")
    risks = [
        ("价格战常态化", "终端折扣侵蚀毛利，弱势品牌出清加速。", RED),
        ("产能与库存", "行业扩张过快，车型生命周期缩短，库存管理要求提升。", AMBER),
        ("技术路线不确定", "电池技术、智能驾驶法规、芯片供应和软件栈仍在快速演进。", BLUE),
        ("补能利用率", "建桩速度快，但站点质量、利用率和电网接入决定实际回报。", TEAL),
        ("海外合规", "关税、本地化、数据合规、供应链溯源增加出海复杂度。", GREEN),
        ("消费者信任", "安全事故、保值率、售后服务会影响品牌长期口碑。", DARK),
    ]
    for i, (t, b, c) in enumerate(risks):
        s.card(0.75 + (i % 3) * 4.05, 1.52 + (i // 3) * 1.82, 3.65, 1.24, t, b, c)
    s.rect(0.85, 5.55, 11.4, 0.68, "17212B", radius=True, line=False)
    s.text("生态分析的核心问题不是“谁销量最大”，而是“谁能在价格战下保持现金流、用户体验和技术迭代速度”。", 1.1, 5.78, 10.7, 0.2, 9.5, WHITE, bold=True, align="ctr")
    s.footer()
    slides.append(s)

    s = Slide("战略机会：从整车销售走向“车 + 能源 + 服务”的复利生态", "11 机会判断")
    opps = [
        ("高压快充网络", "围绕 800V 平台、液冷超充和目的地充电，建立体验差异。", TEAL),
        ("主流价位智能化", "15-25 万元市场将成为智能驾驶和座舱体验平权主战场。", BLUE),
        ("电池生命周期", "电池检测、残值评估、梯次利用和回收将形成新利润池。", GREEN),
        ("出海本地化", "从出口转向本地制造、本地供应链和本地服务体系。", AMBER),
        ("车网互动", "V2G、储能、光伏和电力交易把车辆接入城市能源系统。", RED),
        ("数据服务", "基于车队、充电、维修和用户行为的数据能力进入商业化探索期。", DARK),
    ]
    for i, (t, b, c) in enumerate(opps):
        x = 0.75 + (i % 2) * 5.95
        y = 1.42 + (i // 2) * 1.55
        s.rect(x, y, 5.45, 1.05, WHITE, radius=True, line=True, line_color="E5DED2")
        s.rect(x + 0.24, y + 0.28, 0.35, 0.35, c, radius=True, line=False)
        s.text(t, x + 0.78, y + 0.22, 1.65, 0.22, 10, INK, bold=True)
        s.text(b, x + 0.78, y + 0.52, 4.15, 0.28, 7.8, MUTED)
    s.card(0.85, 6.2, 11.35, 0.52, "总体判断", "中国纯电汽车行业不会简单回到高增速时代，但会在能源化、智能化和服务化中继续释放结构性机会。", TEAL)
    s.footer()
    slides.append(s)

    s = Slide("未来 3-5 年：行业将进入三类玩家分化", "12 生态演进")
    lanes = [
        ("生态整合者", "掌握整车、电池、软件、渠道和能源入口，目标是持续扩大用户生命周期价值。", GREEN),
        ("效率制造者", "以平台化、供应链和成本控制为核心，在主流价格带获取规模优势。", TEAL),
        ("垂直服务商", "聚焦电池、补能、智能驾驶、车后服务等环节，嵌入头部生态。", BLUE),
    ]
    for i, (t, b, c) in enumerate(lanes):
        y = 1.65 + i * 1.45
        s.rect(1.0, y, 2.25, 0.58, c, radius=True, line=False)
        s.text(t, 1.15, y + 0.19, 1.95, 0.14, 8.5, WHITE, bold=True, align="ctr")
        s.rect(3.55, y, 7.85, 0.58, WHITE, radius=True, line=True, line_color="E5DED2")
        s.text(b, 3.78, y + 0.18, 7.25, 0.16, 8.3, MUTED)
    s.rect(1.0, 6.0, 10.4, 0.32, "E9E4DA", radius=True, line=False)
    s.rect(1.0, 6.0, 3.0, 0.32, GREEN, radius=True, line=False)
    s.rect(4.0, 6.0, 3.35, 0.32, TEAL, radius=True, line=False)
    s.rect(7.35, 6.0, 4.05, 0.32, BLUE, radius=True, line=False)
    s.text("2026：出清与整合", 1.0, 6.38, 2.5, 0.18, 7.3, INK, bold=True)
    s.text("2027-2028：智能化平权", 4.0, 6.38, 2.8, 0.18, 7.3, INK, bold=True)
    s.text("2029+：能源与服务复利", 7.35, 6.38, 3.2, 0.18, 7.3, INK, bold=True)
    s.footer()
    slides.append(s)

    s = Slide("资料来源与方法", "13 Appendix")
    sources = [
        "新华社 / 中国汽车工业协会：2025 年中国新能源汽车产销均超 1600 万辆的公开报道。",
        "央视网等公开报道：2025 年中国纯电动汽车产销均超过 1060 万辆。",
        "IEA Global EV Outlook 2025：中国在全球电动车销量、生产和电池供应链中的领先地位。",
        "国家能源局、中国充电联盟及央视网：2025 年全国充电基础设施规模与补能网络进展。",
        "财政部、税务总局、工信部：新能源汽车车辆购置税减免政策延续安排。",
        "SNE Research、企业年报/公告、公开新闻报道：动力电池竞争格局与技术路线。",
    ]
    y = 1.42
    for i, src in enumerate(sources):
        s.rect(0.95, y + i * 0.63, 0.22, 0.22, TEAL if i % 2 == 0 else BLUE, radius=True, line=False)
        s.text(src, 1.32, y + i * 0.59, 10.7, 0.28, 8.5, INK)
    s.card(0.95, 5.72, 11.0, 0.78, "方法说明", "本报告为生态分析型演示稿，公开数据用于判断行业方向；竞争矩阵和机会判断为基于公开资料的战略分析示意，非投资建议。", AMBER)
    s.footer("生成时间：2026-05-13")
    slides.append(s)

    return slides


def package(slides: list[Slide]):
    tmp = ROOT / "05_源文件PPT" / "_pptx_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "_rels").mkdir(parents=True)
    (tmp / "docProps").mkdir()
    (tmp / "ppt" / "_rels").mkdir(parents=True)
    (tmp / "ppt" / "slides" / "_rels").mkdir(parents=True)
    (tmp / "ppt" / "slideMasters" / "_rels").mkdir(parents=True)
    (tmp / "ppt" / "slideLayouts" / "_rels").mkdir(parents=True)
    (tmp / "ppt" / "theme").mkdir(parents=True)
    (tmp / "ppt" / "media").mkdir(parents=True)

    shutil.copy2(ASSET, tmp / "ppt" / "media" / ASSET.name)

    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, len(slides) + 1):
        overrides.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
    (tmp / "[Content_Types].xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>{''.join(overrides)}</Types>""",
        encoding="utf-8",
    )
    (tmp / "_rels" / ".rels").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>""",
        encoding="utf-8",
    )
    (tmp / "docProps" / "core.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>中国纯电汽车行业生态分析</dc:title><dc:creator>Codex</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">2026-05-13T00:00:00Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2026-05-13T00:00:00Z</dcterms:modified></cp:coreProperties>""",
        encoding="utf-8",
    )
    (tmp / "docProps" / "app.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application><PresentationFormat>宽屏</PresentationFormat><Slides>{len(slides)}</Slides></Properties>""",
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
    (tmp / "ppt" / "theme" / "theme1.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Codex Premium"><a:themeElements><a:clrScheme name="Codex"><a:dk1><a:srgbClr val="17212B"/></a:dk1><a:lt1><a:srgbClr val="F7F5EF"/></a:lt1><a:dk2><a:srgbClr val="111827"/></a:dk2><a:lt2><a:srgbClr val="FFFFFF"/></a:lt2><a:accent1><a:srgbClr val="00A6A6"/></a:accent1><a:accent2><a:srgbClr val="2563EB"/></a:accent2><a:accent3><a:srgbClr val="22A06B"/></a:accent3><a:accent4><a:srgbClr val="D99A1E"/></a:accent4><a:accent5><a:srgbClr val="C2413A"/></a:accent5><a:accent6><a:srgbClr val="66717F"/></a:accent6><a:hlink><a:srgbClr val="2563EB"/></a:hlink><a:folHlink><a:srgbClr val="00A6A6"/></a:folHlink></a:clrScheme><a:fontScheme name="Microsoft YaHei"><a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface="Microsoft YaHei"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/><a:ea typeface="Microsoft YaHei"/></a:minorFont></a:fontScheme><a:fmtScheme name="Codex"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>""",
        encoding="utf-8",
    )

    for i, slide in enumerate(slides, start=1):
        (tmp / "ppt" / "slides" / f"slide{i}.xml").write_text(slide.xml(), encoding="utf-8")
        (tmp / "ppt" / "slides" / "_rels" / f"slide{i}.xml.rels").write_text(slide.rels_xml(), encoding="utf-8")

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
    package(slides)
    print(f"created: {OUT}")
    print(f"slides: {len(slides)}")
    print(f"size: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
