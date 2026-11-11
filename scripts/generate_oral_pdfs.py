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

SCRIPTS = [
    ('01_ELKIHEL.pdf', 'Elkihel Elmehdi', 'Diapositives 1 à 3 · environ 1 min 50', [
        ('Diapositive 1 — Présentation',
         "Bonjour. Nous allons présenter notre mini-projet sur la prédiction des besoins énergétiques des bâtiments. Notre objectif est d’estimer la charge de chauffage, appelée Y1, puis de comparer cinq méthodes de machine learning. Nous sommes Elkihel, El Assri et Said. Les données proviennent du jeu public Energy Efficiency de l’UCI et décrivent des configurations simulées de bâtiments."),
        ('Diapositive 2 — Question et données',
         "Notre question centrale est la suivante : quel modèle prédit le plus précisément la charge de chauffage, et dans quels cas se trompe-t-il ? Le tableau comporte 768 configurations, sans valeurs manquantes. Chaque ligne contient huit caractéristiques, notées X1 à X8 : par exemple la surface, la hauteur, l’orientation et les vitrages. Y1 est la seule valeur que nous voulons prédire. Le fichier contient aussi Y2, la charge de refroidissement, mais nous ne l’utilisons pas comme entrée, car notre sujet concerne uniquement le chauffage."),
        ('Diapositive 3 — Exploration',
         "Nous avons commencé par regarder la distribution de Y1 et sa relation avec plusieurs caractéristiques. Dans l’histogramme, on voit combien de configurations correspondent à chaque niveau de charge. Dans les nuages de points, chaque point représente une configuration. Les relations ne paraissent pas toutes simples ou droites. Cela nous donne une raison de comparer des méthodes linéaires et des méthodes capables de représenter des relations plus complexes. Ces graphiques restent descriptifs : ils ne prouvent pas qu’une variable cause à elle seule une variation de la charge. Je passe maintenant la parole à El Assri pour expliquer le protocole et les modèles."),
    ]),
    ('02_EL_ASSRI.pdf', 'El Assri L’Houcine', 'Diapositives 4 et 5 · environ 2 min 05', [
        ('Diapositive 4 — Comment nous avons travaillé',
         "Je vais expliquer comment nous avons appris et vérifié les modèles. Imaginez un élève qui révise sur des exercices, puis passe un examen avec des exercices différents. Ici, nous faisons pareil : 614 configurations de bâtiments servent à l’entraînement et 154 sont gardées pour le test final. Les modèles ne regardent pas ces 154 exemples pendant l’apprentissage. Pour choisir leurs réglages, nous partageons les 614 exemples en cinq parties. À chaque étape, le modèle apprend sur quatre parties et nous contrôlons ses prédictions sur la cinquième. C’est la validation croisée à cinq plis. Nous choisissons les réglages qui donnent la plus petite erreur moyenne, appelée RMSE. Certaines mesures sont aussi mises sur des échelles comparables. Cette préparation est faite uniquement avec les données utilisées pour apprendre, afin de ne pas fausser le contrôle."),
        ('Diapositive 5 — Les cinq modèles',
         "Nous comparons cinq méthodes. La régression linéaire est notre point de départ : elle combine les mesures pour prévoir la charge de chauffage. Ridge fonctionne de façon proche, avec un frein qui évite des coefficients trop grands. KNN cherche les bâtiments connus les plus ressemblants ; notre réglage retient cinq voisins. L’arbre de décision pose des questions successives sur les mesures, un peu comme un jeu de « si… alors… ». Random Forest combine plusieurs arbres ; le réglage retenu en utilise deux cents. Les réglages de Ridge, KNN, de l’arbre et de la forêt ont été choisis avec la validation croisée, sans utiliser le test final. Nous pouvons maintenant comparer les erreurs de ces cinq méthodes. Said va présenter les résultats."),
    ]),
    ('03_SAID.pdf', 'Said Charaf', 'Diapositives 6 à 8 · environ 2 min 05', [
        ('Diapositive 6 — Résultats',
         "Le graphique compare les cinq modèles. Pour le RMSE, une barre plus basse signifie de plus petites erreurs. Pour R deux, une valeur plus proche de un indique une meilleure adéquation sur ce test. Les deux modèles linéaires ont un RMSE de test proche de 2,87. KNN descend à 1,67. L’arbre et Random Forest sont proches de 0,53. Nous avons sélectionné Random Forest parce qu’il avait le meilleur RMSE moyen en validation croisée, 0,535. Sur le test, l’arbre obtient un résultat légèrement meilleur, 0,531 contre 0,536 pour la forêt. Cet écart minime sur une partition ne suffit pas à affirmer qu’un modèle est toujours supérieur."),
        ('Diapositive 7 — Prédictions et erreurs',
         "À gauche, plus un point est proche de la diagonale, plus la charge prédite est proche de la charge observée. À droite, les résidus représentent la valeur observée moins la valeur prédite. Un résidu positif signale une sous-estimation ; un résidu négatif, une surestimation. Nous avons aussi comparé les erreurs de sous-groupes. Pour la hauteur X5 égale à 3,5, l’erreur absolue moyenne est de 0,171 sur 72 cas ; pour X5 égale à 7, elle est de 0,546 sur 82 cas. C’est une observation descriptive, pas une preuve que la hauteur cause cette différence."),
        ('Diapositive 8 — Conclusion',
         "En conclusion, les méthodes non linéaires prédisent mieux que les méthodes linéaires dans cette expérience. Random Forest est le modèle choisi par validation croisée, et l’arbre de décision donne un résultat final très proche. Notre limite principale est que les bâtiments sont simulés et que le test repose sur une seule séparation. Avant une utilisation pratique, il faudrait vérifier les performances sur des bâtiments réels et indépendants. Merci pour votre attention. Nous sommes prêts à répondre à vos questions."),
    ]),
]

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
