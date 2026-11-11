"""Crée huit diapositives du mini-projet 03, inspirées de la mise en page fournie."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'Presentation_Projet_03.pptx'
prs=Presentation()
prs.slide_width=Inches(13.333)
prs.slide_height=Inches(7.5)
BG=RGBColor(11,19,43); DARK=RGBColor(28,37,65); GREEN=RGBColor(0,92,56)
PALE=RGBColor(236,253,245); WHITE=RGBColor(255,255,255)
INK=RGBColor(28,39,58); MUTED=RGBColor(87,105,124); BORDER=RGBColor(226,232,240)

def rect(sl,x,y,w,h,color,rounded=False):
 sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
 sh.fill.solid();sh.fill.fore_color.rgb=color;sh.line.fill.background()
 if rounded:
  try: sh.adjustments[0]=.12
  except: pass
 return sh

def txt(sl,text,x,y,w,h,size=18,color=INK,bold=False,align=None):
 sh=sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
 tf=sh.text_frame;tf.clear();tf.word_wrap=True
 tf.margin_left=Pt(0);tf.margin_right=Pt(0);tf.margin_top=Pt(0);tf.margin_bottom=Pt(0)
 for i,line in enumerate(text.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.space_after=Pt(5)
  if align:p.alignment=align
  for r in p.runs:
   r.font.name='Aptos';r.font.size=Pt(size);r.font.bold=bold;r.font.color.rgb=color
 return sh

def picture(sl,path,x,y,w,h):
 im=Image.open(path);iw,ih=im.size; ratio=min(w/iw,h/ih);ww=iw*ratio;hh=ih*ratio
 sl.shapes.add_picture(str(path), Inches(x+(w-ww)/2), Inches(y+(h-hh)/2), width=Inches(ww),height=Inches(hh))

def base(section,title,n):
 sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=RGBColor(248,250,252)
 rect(sl,0,0,13.333,1.08,WHITE);rect(sl,.78,.2,.08,.72,GREEN)
 txt(sl,section.upper(),.99,.16,9,.22,10,GREEN,True)
 txt(sl,title,.99,.4,10.9,.55,24,INK,True)
 picture(sl,ROOT/'report/figures/logos/INSEA_logo.png',11.75,.16,.72,.8)
 rect(sl,.8,6.96,11.73,.015,BORDER)
 txt(sl,'INSEA · Mini-projet 03 · Efficacité énergétique',.8,7.07,8,.24,10,MUTED)
 txt(sl,f'{n} / 8',11.6,7.07,.9,.24,10,MUTED,align=PP_ALIGN.RIGHT)
 return sl

def card(sl,x,y,w,h,title,body,accent=GREEN):
 rect(sl,x,y,w,h,WHITE,True);rect(sl,x,y,.07,h,accent)
 txt(sl,title,x+.22,y+.2,w-.45,.55,17,INK,True)
 txt(sl,body,x+.22,y+.85,w-.45,h-1,15,MUTED)

def notes(sl,text):
 try: sl.notes_slide.notes_text_frame.text=text
 except Exception: pass

# 1 : couverture
s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=BG
rect(s,.85,1.87,4.6,.42,DARK,True)
txt(s,'INSEA · MINI-PROJET DE MACHINE LEARNING',1.02,1.94,4.45,.25,12,WHITE,True)
picture(s,ROOT/'report/figures/logos/INSEA_logo.png',10.85,.62,1.35,1.5)
txt(s,'Prédiction des besoins\nénergétiques des bâtiments',.9,2.55,10.8,1.55,31,WHITE,True)
txt(s,'Charge de chauffage Y1 · Comparaison de cinq modèles',.9,4.3,10.6,.5,18,RGBColor(166,211,189))
for j,(name) in enumerate(['ELKIHEL ELMEHDI','EL ASSRI L’HOUCINE','SAID CHARAF']):
 x=.9+j*4.05;rect(s,x,5.3,3.78,1.1,DARK,True);rect(s,x+.2,5.45,3.38,.04,GREEN)
 txt(s,name,x+.2,5.7,3.38,.45,16,WHITE,True)
txt(s,'Année universitaire 2026–2027',.9,6.93,8,.3,11,WHITE)
notes(s,'Présenter le sujet : prédire la charge de chauffage de bâtiments simulés. Dire que les cinq modèles ont été entraînés sur le jeu Energy Efficiency de l’UCI.')

# 2 : question + données
s=base('Cadrage','Question centrale et jeu de données',2)
rect(s,.8,1.39,11.73,1.2,PALE,True)
txt(s,'Quel modèle prédit le plus précisément la charge de chauffage Y1, et où apparaissent les erreurs ?',1.05,1.72,11.2,.62,21,GREEN,True)
card(s,.8,2.88,3.7,3.52,'768 configurations','Bâtiments simulés du jeu Energy Efficiency (UCI).',GREEN)
card(s,4.82,2.88,3.7,3.52,'8 caractéristiques','Géométrie, hauteur, orientation et vitrages : X1 à X8.',GREEN)
card(s,8.84,2.88,3.7,3.52,'1 cible : Y1','Charge de chauffage. Y2, la charge de refroidissement, est exclue.',GREEN)
notes(s,'768 lignes sans valeurs manquantes. Y1 est la seule cible. Y2 ne doit jamais entrer dans X, car ce serait une autre sortie du jeu.')

# 3 : EDA
s=base('Exploration','Distribution de Y1 et relations avec les variables',3)
rect(s,.8,1.38,11.73,4.8,WHITE,True)
picture(s,ROOT/'figures/01_exploration.png',1,1.55,11.3,4.42)
rect(s,.8,6.3,11.73,.48,PALE,True)
txt(s,'Les relations observées suggèrent de comparer des modèles linéaires et non linéaires.',1,6.41,11.2,.28,14,GREEN,True)
notes(s,'Montrer la distribution de Y1 et quelques relations avec X1, X2, X4, X5 et X7. Ces graphiques ne prouvent pas de causalité.')

# 4 : protocole
s=base('Méthode','Protocole : apprendre, régler, puis évaluer',4)
for j,(num,title,body) in enumerate([
 ('01','Séparer','614 observations pour apprendre ; 154 gardées pour le test. Tirage fixé à 42.'),
 ('02','Valider','Cinq plis sur l’entraînement. Les réglages minimisent le RMSE moyen.'),
 ('03','Évaluer','MAE, MSE, RMSE et R² calculés sur les 154 observations de test.')]):
 x=.8+j*4.0;rect(s,x,1.65,3.73,4.15,WHITE,True)
 rect(s,x+.24,1.95,.65,.65,PALE,True);txt(s,num,x+.35,2.09,.5,.32,18,GREEN,True)
 txt(s,title,x+.24,2.87,3.2,.5,20,INK,True)
 txt(s,body,x+.24,3.53,3.2,1.55,16,MUTED)
rect(s,.8,6.05,11.73,.63,PALE,True)
txt(s,'Standardisation et encodage appris dans chaque pli : le jeu de test reste à l’écart.',1.05,6.2,11.1,.3,15,GREEN,True)
notes(s,'Le scaler est ajusté dans chaque pli et jamais sur le test. X6 et X8 sont encodées comme catégories. Une graine fixe rend la séparation reproductible.')

# 5 : modèles
s=base('Modélisation','Cinq modèles et leurs hyperparamètres retenus',5)
models=[
 ('Régression linéaire','Référence : aucun réglage'),
 ('Ridge','Alpha = 0,1\nRégularisation des coefficients'),
 ('KNN','5 voisins ; distance Manhattan\nPoids uniformes'),
 ('Arbre de décision','Profondeur = 8\nAu moins 2 cas par feuille'),
 ('Random Forest','200 arbres ; profondeur = 10\nAu moins 1 cas par feuille'),
]
for j,(title,body) in enumerate(models):
 x=.8+(j%3)*4.0;y=1.48+(j//3)*2.48
 card(s,x,y,3.72,2.18,title,body)
rect(s,8.8,3.96,3.72,2.18,PALE,True)
txt(s,'4 modèles réglés',9.08,4.43,3.17,.5,20,GREEN,True)
txt(s,'Choix par validation croisée à 5 plis, selon le RMSE.',9.08,5.05,3.15,.74,15,MUTED)
notes(s,'Expliquer que les hyperparamètres sont des réglages choisis avant le test. Ridge : alpha 0,1. KNN : 5 voisins, distance Manhattan (p=1), poids uniformes. Arbre : profondeur 8, au moins 2 cas par feuille. Random Forest : 200 arbres, profondeur 10, au moins 1 cas par feuille. Les choix utilisent le RMSE moyen des 5 plis de validation.')

# 6 : résultats sous forme de graphiques
s=base('Résultats','Cinq modèles : comparer RMSE et R² en un regard',6)
rect(s,.8,1.38,11.73,4.9,WHITE,True)
picture(s,ROOT/'figures/02_comparaison.png',1.02,1.6,11.25,4.42)
rect(s,.8,6.39,11.73,.43,PALE,True)
txt(s,'RMSE : plus bas = mieux. R² : plus proche de 1 = mieux. La forêt est sélectionnée par validation.',1,6.48,11.14,.27,13,GREEN,True)
notes(s,'Présenter les cinq barres de RMSE et les cinq barres de R². L’arbre a RMSE test 0,531, la forêt 0,536. Mais la forêt avait le meilleur RMSE CV : 0,535. Le test sert à évaluer, pas à changer le choix du modèle.')

# 7 : erreurs
s=base('Diagnostic','Prédictions et résidus de Random Forest',7)
rect(s,.8,1.38,5.68,4.87,WHITE,True)
picture(s,ROOT/'figures/03_observe_predit.png',.98,1.69,5.3,4.05)
rect(s,6.72,1.38,5.81,4.87,WHITE,True)
picture(s,ROOT/'figures/04_residus.png',6.9,1.68,5.45,4.05)
rect(s,.8,6.37,11.73,.43,PALE,True)
txt(s,'Résidu = Y1 observée − Y1 prédite. Les écarts de sous-groupes restent descriptifs.',1,6.48,11.1,.25,13,GREEN,True)
notes(s,'À gauche : diagonale = prédiction parfaite. À droite : les résidus proches de zéro sont meilleurs. La MAE pour X5=3,5 est 0,171 (72 cas) ; pour X5=7 elle est 0,546 (82 cas). Cela ne prouve pas un effet causal de la hauteur.')

# 8 : conclusion
s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=BG
picture(s,ROOT/'report/figures/logos/INSEA_logo.png',11.25,.45,1.15,1.25)
txt(s,'Conclusion',.9,.62,7,.65,30,WHITE,True)
for j,(title,body) in enumerate([
 ('Choix selon la validation','Random Forest : RMSE CV = 0,535.'),
 ('Performance sur le test','RMSE = 0,536 ; R² = 0,997 sur 154 cas.'),
 ('Limite essentielle','Données simulées : validation externe nécessaire.')]):
 x=.9+j*4.05;rect(s,x,1.8,3.75,2.25,DARK,True)
 txt(s,title,x+.22,2.12,3.3,.58,17,WHITE,True)
 txt(s,body,x+.22,2.91,3.25,.85,15,RGBColor(197,223,210))
rect(s,.9,4.65,11.55,1.7,DARK,True)
txt(s,'Merci pour votre attention',3.3,4.99,6.8,.52,25,WHITE,True,PP_ALIGN.CENTER)
txt(s,'Questions ?',5.55,5.62,2.2,.35,16,RGBColor(166,211,189),False,PP_ALIGN.CENTER)
txt(s,'Source : UCI Energy Efficiency, dataset 242 · Année 2026–2027',.9,7.06,9.5,.25,10,WHITE)
notes(s,'Conclusion : les arbres dominent les modèles linéaires sur cette expérience. Random Forest est choisi par CV ; l’arbre est très proche sur le test. Ne pas extrapoler aux bâtiments réels sans validation externe.')

prs.save(OUT)
print(f'{len(prs.slides)} diapositives écrites dans {OUT}')
