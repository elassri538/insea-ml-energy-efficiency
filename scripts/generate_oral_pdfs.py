"""Génère les trois scripts individuels pour un oral total de six minutes."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scripts_oraux'
OUT.mkdir(exist_ok=True)
font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if Path(font).exists():
    pdfmetrics.registerFont(TTFont('DV', font))
    pdfmetrics.registerFont(TTFont('DVB', bold))
    BODY, HEAD = 'DV', 'DVB'
else:
    BODY, HEAD = 'Helvetica', 'Helvetica-Bold'
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MainTitleFR', parent=styles['Title'], fontName=HEAD, fontSize=17,
                          leading=22, textColor=colors.HexColor('#005C38'), spaceAfter=10))
styles.add(ParagraphStyle(name='SubFR', parent=styles['Normal'], fontName=BODY, fontSize=10.5,
                          leading=15, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name='PartFR', parent=styles['Heading2'], fontName=HEAD, fontSize=11,
                          leading=15, textColor=colors.HexColor('#005C38'), spaceBefore=11, spaceAfter=5))
styles.add(ParagraphStyle(name='SpeechFR', parent=styles['BodyText'], fontName=BODY, fontSize=10.3,
                          leading=16, spaceAfter=7))
styles.add(ParagraphStyle(name='HintFR', parent=styles['Normal'], fontName=BODY, fontSize=8.5,
                          leading=12, textColor=colors.HexColor('#526579'), spaceAfter=4))

from oral_content import SCRIPTS

for filename, name, subtitle, sections in SCRIPTS:
    story = [Paragraph('Script oral — mini-projet 03', styles['MainTitleFR']),
             Paragraph(escape(name) + '<br/>' + escape(subtitle), styles['SubFR']),
             HRFlowable(width='100%', thickness=1, color=colors.HexColor('#005C38')),
             Spacer(1, .15*cm)]
    for title, body in sections:
        story += [Paragraph(escape(title), styles['PartFR']), Paragraph(escape(body), styles['SpeechFR'])]
    story += [Spacer(1, .2*cm), Paragraph('Conseil : parle naturellement, en montrant le graphique ou la diapositive concernée. Les durées sont indicatives ; répétez ensemble pour rester sous six minutes.', styles['HintFR'])]
    doc = SimpleDocTemplate(str(OUT/filename), pagesize=A4, rightMargin=2.1*cm,
                            leftMargin=2.1*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
                            title=f'Script oral — {name}', author='Équipe mini-projet 03 INSEA')
    doc.build(story)
    print(filename, sum(len(body.split()) for _, body in sections), 'mots')
