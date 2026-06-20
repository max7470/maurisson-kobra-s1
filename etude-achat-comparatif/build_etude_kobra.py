# -*- coding: utf-8 -*-
"""Étude complète — Anycubic Kobra S1 Combo. 10/06/2026."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, HRFlowable, KeepTogether)

BASE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(BASE, "photos")
OUT = os.path.join(BASE, "Etude-complete-Anycubic-Kobra-S1-Combo.pdf")

PAGE_W, PAGE_H = A4
M = 16 * mm

INK = colors.HexColor("#1a2332")
ACCENT = colors.HexColor("#0f6f5c")
ACCENT_LIGHT = colors.HexColor("#e6f2ef")
GOLD = colors.HexColor("#b07a1e")
GOLD_LIGHT = colors.HexColor("#fdf3e0")
RED = colors.HexColor("#a33327")
RED_LIGHT = colors.HexColor("#fbeae7")
GREY = colors.HexColor("#5b6470")
LINE = colors.HexColor("#d7dce3")
ROW_ALT = colors.HexColor("#f4f6f8")

ss = getSampleStyleSheet()
def st(name, **kw):
    base = kw.pop("parent", ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

S_TITLE = st("t", fontName="Helvetica-Bold", fontSize=24, leading=29, textColor=INK)
S_SUB   = st("sub", fontName="Helvetica", fontSize=12, leading=16, textColor=GREY)
S_H1    = st("h1", fontName="Helvetica-Bold", fontSize=15.5, leading=19, textColor=INK, spaceBefore=4*mm, spaceAfter=2.5*mm)
S_H2    = st("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT, spaceBefore=2.8*mm, spaceAfter=1.4*mm)
S_BODY  = st("b", fontName="Helvetica", fontSize=9.2, leading=12.8, textColor=INK)
S_BODY_S= st("bs", fontName="Helvetica", fontSize=8.4, leading=11.4, textColor=INK)
S_CELL  = st("c", fontName="Helvetica", fontSize=8.2, leading=10.6, textColor=INK)
S_CELL_B= st("cb", fontName="Helvetica-Bold", fontSize=8.2, leading=10.6, textColor=INK)
S_QUOTE = st("q", fontName="Helvetica-Oblique", fontSize=8.8, leading=12, textColor=INK, leftIndent=5*mm)
S_QSRC  = st("qs", fontName="Helvetica", fontSize=7.4, leading=9.6, textColor=GREY, leftIndent=5*mm)
S_CAPT  = st("cp", fontName="Helvetica-Oblique", fontSize=7.6, leading=9.8, textColor=GREY, alignment=TA_CENTER)
S_BADGE = st("bd", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.white)
S_SMALL = st("sm", fontName="Helvetica", fontSize=7.4, leading=9.6, textColor=GREY)

def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(GOLD)
        canvas.rect(0, PAGE_H - 8*mm, PAGE_W, 8*mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.drawString(M, PAGE_H - 5.6*mm, "ÉTUDE COMPLÈTE — ANYCUBIC KOBRA S1 COMBO")
        canvas.drawRightString(PAGE_W - M, PAGE_H - 5.6*mm, "Forums, wiki officiel, tests longue durée · 10 juin 2026")
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(PAGE_W - M, 8*mm, f"Page {doc.page}")
    canvas.drawString(M, 8*mm, "Sources : Reddit/forums (via index), lesimprimantes3d.fr, wiki.anycubic.com, GitHub, Tom's Hardware, Notebookcheck, 3DWithUs, Trustpilot")
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=14*mm, bottomMargin=14*mm)
frame = Frame(M, 13*mm, PAGE_W - 2*M, PAGE_H - 28*mm, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=header_footer)])
E = []

def kv(rows, col1=44*mm):
    data = [[Paragraph(k, S_CELL_B), Paragraph(v, S_CELL)] for k, v in rows]
    t = Table(data, colWidths=[col1, PAGE_W - 2*M - col1])
    sty = [("VALIGN", (0,0), (-1,-1), "TOP"),
           ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
           ("TOPPADDING", (0,0), (-1,-1), 2.4), ("BOTTOMPADDING", (0,0), (-1,-1), 2.4),
           ("LINEBELOW", (0,0), (-1,-2), 0.4, LINE)]
    for i in range(len(rows)):
        if i % 2 == 0:
            sty.append(("BACKGROUND", (0,i), (-1,i), ROW_ALT))
    t.setStyle(TableStyle(sty))
    return t

def box(title, body, bg, border):
    t = Table([[Paragraph(f"<b>{title}</b><br/>{body}", S_CELL)]], colWidths=[PAGE_W - 2*M])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg), ("BOX", (0,0), (-1,-1), 0.8, border),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
    return t

def quote(txt, src):
    t = Table([[Paragraph("« " + txt + " »", S_QUOTE)], [Paragraph(src, S_QSRC)]], colWidths=[PAGE_W - 2*M])
    t.setStyle(TableStyle([
        ("LINEBEFORE", (0,0), (0,-1), 2, GOLD),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("TOPPADDING", (0,0), (-1,-1), 1.6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1.6)]))
    return t

# ================= PAGE 1 — COUVERTURE =================
E.append(Spacer(1, 6*mm))
E.append(Paragraph("Anycubic Kobra S1 Combo", S_TITLE))
E.append(Paragraph("Étude complète — specs, montage, retours utilisateurs des forums, fiabilité, écosystème", S_SUB))
E.append(Spacer(1, 4*mm))
E.append(HRFlowable(width="100%", thickness=1.2, color=GOLD))
E.append(Spacer(1, 4*mm))

w = (PAGE_W - 2*M - 6*mm) / 2
img_row = Table([[
    [Image(os.path.join(PHOTOS, "kobra-s1-1.jpg"), width=w, height=58*mm, kind="proportional"),
     Spacer(1, 1.5*mm), Paragraph("La machine + 1 ACE Pro (config du combo bol.com, 4 couleurs)", S_CAPT)],
    [Image(os.path.join(PHOTOS, "kobra-s1-2.jpg"), width=w, height=58*mm, kind="proportional"),
     Spacer(1, 1.5*mm), Paragraph("Config 8 couleurs : 2 ACE Pro empilés A CÔTÉ de la machine", S_CAPT)],
]], colWidths=[w + 3*mm, w + 3*mm])
img_row.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("ALIGN", (0,0), (-1,-1), "CENTER"),
                             ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 3*mm)]))
E.append(img_row)
E.append(Spacer(1, 4*mm))

E.append(Paragraph("L'essentiel en 10 lignes", S_H2))
E.append(Paragraph(
    "CoreXY <b>fermée</b>, 250 × 250 × 250 mm, multi-couleurs via le module ACE Pro (4 bobines, séchage actif 55 °C) posé "
    "<b>à côté</b> de la machine. <b>Prémontée à ~95 %</b> : 10 à 20 minutes de débridage, calibration 100 % automatique, "
    "premier Benchy réussi en 13 minutes chez quasi tous les testeurs. Qualité mono-couleur au niveau Bambu/Prusa, "
    "ABS excellent grâce au caisson + buse 320 °C. Les forums confirment une machine <b>« set and forget » une fois rodée</b> — "
    "mais une <b>loterie de contrôle qualité à réception</b> (les unités défectueuses existent, le SAV remplace vite) et un "
    "<b>ACE Pro qui est le maillon faible</b> (bourrages documentés, bobines carton à adapter). Le gros défaut du lancement, "
    "le slicer, a été <b>largement corrigé en 2025-2026</b> (Slicer Next basé OrcaSlicer) et la communauté a tout déverrouillé "
    "via le firmware Rinkhals. En juin 2026, à 429,99 € sur bol.com, elle reste quasi seule sur la case « CoreXY fermée "
    "multi-couleurs sous 450 € » — toujours recommandée par les guides d'achat.", S_BODY))
E.append(Spacer(1, 3.5*mm))

E.append(Paragraph("Réponse à ta question : prémontée ?", S_H2))
E.append(box("OUI — ce n'est pas un kit. 10 à 20 minutes chrono du carton au premier print.",
    "L'ACE Pro voyage à l'intérieur du caisson. Il reste : retirer 9 vis de transport (toutes marquées de grosses flèches rouges), "
    "extraire les mousses, visser le hub filament à l'arrière, brancher 4 tubes PTFE + 2 câbles (ports détrompés, impossible de se "
    "tromper) et 2 prises secteur. L'écran est préinstallé. Ensuite l'assistant fait tout : Wi-Fi, auto-test, nivellement LeviQ 3.0, "
    "compensation de vibrations, PID — zéro réglage manuel. Détail complet en page 3.", GOLD_LIGHT, GOLD))
E.append(Spacer(1, 3.5*mm))
E.append(Paragraph("Correction par rapport au dossier comparatif précédent", S_H2))
E.append(Paragraph(
    "Le passage à 8 couleurs coûte plus cher qu'estimé : le 2e module ACE Pro est à <b>249 €</b> sur le store EU Anycubic "
    "(et non ~100-130 €), et il faut en plus un <b>hub filament 8 couleurs</b> (vendu séparément, ou imprimable selon le guide "
    "officiel). Le combo 8 couleurs d'usine vaut 668 €. À savoir si tu rêves en huit teintes.", S_BODY))
E.append(PageBreak())

# ================= 1. FICHE TECHNIQUE =================
E.append(Paragraph("1 · Fiche technique complète", S_H1))
E.append(kv([
    ("Architecture", "CoreXY entièrement fermée (structure interne métal, habillage et capot plastique — attention, ça se raye) · 400 × 410 × 490 mm · 18 kg · colis ~30 kg (être deux pour le porter)"),
    ("Volume / filament", "250 × 250 × 250 mm · filament 1,75 mm"),
    ("Mouvement", "X/Y : tiges acier avec palier graphène autolubrifiant (PAS de rails linéaires profilés) · Z : tiges + vis · vitesse max 600 mm/s (300 recommandé) · accél. max 20 000 mm/s² · surveillance de tension de courroie intégrée"),
    ("Hotend", "320 °C max, gorge céramique, quick-release SANS outil (levier) · <b>format propriétaire : on remplace le bloc complet buse+gorge+chauffe</b> (13-16 € pièce) · 0,4 laiton de série ; acier trempé 0,4/0,6/0,8 dispo (~16 €) · alternative tierce Micro Swiss FlowTech"),
    ("Extrudeur", "Direct drive double engrenage + <b>cutter de filament intégré</b> (lame remplaçable ~8 €, point d'usure n°1 : vérifier toutes les 3-5 bobines)"),
    ("Plateau", "PEI texturé double face, acier ressort magnétique · 120 °C max (chauffe en moins d'1 min)"),
    ("Calibration", "LeviQ 3.0 : auto-nivellement + Z-offset auto + input shaping + calibration de flux — relancée à chaque print, aucune dérive signalée"),
    ("Capteurs / sécurité", "Fin de filament · reprise après coupure de courant (confirmée) · caméra incluse : timelapse + détection spaghetti IA (faux positifs corrigés par firmware, désactivable) · NB : ouvrir la porte ne met PAS en pause"),
    ("Filtration / éclairage", "Sachet de charbon actif (anti-odeurs basique, pas un vrai HEPA) · barre LED intégrée"),
    ("Connectivité", "Wi-Fi <b>2,4 GHz uniquement</b> + USB · écran tactile 4,3\" inclinable 0-90°"),
    ("Bruit / conso (mesurés)", "44 dB(A) à 1 m (Notebookcheck) — très silencieuse… machine seule ; le sécheur ACE Pro ajoute du bruit de ventilation · ~250 W en impression, ~300 W avec ACE actif, pic ~800 W en préchauffe"),
    ("ACE Pro (module)", "365,9 × 282,8 × 234,5 mm · 4,6 kg · 4 bobines · séchage actif PTC 55 °C (jusqu'à 24 h en continu, 230 W max) · RFID bobines Anycubic (matériau/couleur auto) · filaments tiers OK en déclaration manuelle · bobines 1 kg standard uniquement (ni 250 g ni 3 kg) · 2 modules chaînables = 8 couleurs (+ hub 8 voies requis)"),
    ("Firmware", "Kobra OS — fork fermé de <b>Klipper</b> sur SoC Rockchip · verrouillé d'origine (pas de SSH) · déverrouillable par Rinkhals (voir § 5)"),
    ("Matériaux", "PLA, PETG, ABS, ASA (caisson + 320 °C) · TPU 95A : OUI mais en alimentation directe par le porte-bobine arrière — <b>incompatible ACE Pro</b>, donc pas de TPU multi-couleurs · abrasifs (CF) : passer en hotend acier trempé"),
]))
E.append(PageBreak())

# ================= 2. DU CARTON AU PREMIER PRINT =================
E.append(Paragraph("2 · Du carton au premier print", S_H1))
E.append(Paragraph("Le débridage, étape par étape (10-20 min)", S_H2))
E.append(Paragraph(
    "1. Dévisser les <b>2 vis avant</b> qui verrouillent l'ACE Pro dans le caisson, le sortir par le haut.<br/>"
    "2. Sortir le carton d'accessoires et les mousses internes.<br/>"
    "3. Dévisser <b>4 vis</b> de la base d'immobilisation de l'ACE (au-dessus du plateau).<br/>"
    "4. Débloquer le plateau : <b>3 vis</b> (clé Allen 2,5 fournie). Un plateau encore bridé au premier démarrage peut endommager la machine — c'est LE piège.<br/>"
    "5. Libérer la tête : couper le serre-câble, retirer le carton de protection et le polystyrène de l'éjecteur de purge.<br/>"
    "6. Glisser le sachet de charbon actif dans sa trappe.<br/>"
    "7. Visser à l'arrière le hub filament/détecteur anti-emmêlement (2 vis) + le support de bobine externe (2 vis).<br/>"
    "8. Brancher les <b>4 tubes PTFE</b> ACE-vers-hub (retirer les 4 clips bleus — l'étape la plus pénible, une pince fine aide) et le Bowden de la tête.<br/>"
    "9. Brancher câble signal 6 broches + câble hub 4 broches (détrompés) et les <b>2 câbles secteur</b>.<br/>"
    "<b>Toutes les vis de transport sont marquées de flèches rouges.</b> Temps constaté : 10 min (3DWithUs), ~20 min en prenant son temps (LesImprimantes3D.fr).", S_BODY))
E.append(Paragraph("Dans le carton", S_H2))
E.append(Paragraph(
    "2 câbles secteur · câble signal · hub 4 voies + support bobine externe · 4 tubes PTFE 700 mm · clé USB 4 Go (slicer + manuel PDF) "
    "· clés Allen 2,5/2/1,5 · aiguille de débouchage · graisse · pièces de rechange pour l'essuie-buse · charbon actif · échantillon PLA 10 m "
    "· plateau PEI double face · manuels papier. <b>Pas de buse de rechange fournie.</b> Emballage jugé très bon partout, pas de casse transport récurrente signalée.", S_BODY))
E.append(Paragraph("Première mise en route", S_H2))
E.append(Paragraph(
    "Boot ~40 s, puis assistant : langue (interface en <b>français</b>) · Wi-Fi (2,4 GHz !) · auto-test complet de quelques minutes "
    "(axes, vibrations, PID, nivellement). <b>Compte Anycubic NON obligatoire</b> pour imprimer (USB/LAN) — requis seulement pour l'app mobile "
    "et le pilotage cloud. Mise à jour firmware proposée à l'écran : à faire immédiatement. Chargement filament ACE : poser la bobine, "
    "redresser les 10 derniers cm du filament (sinon il ressort dans l'ACE), pousser jusqu'à l'entraînement. Bobines Anycubic = RFID auto ; "
    "autres marques = déclaration manuelle à l'écran. Premier print : modèles pré-tranchés en mémoire, dont un <b>Benchy de 13 min</b>. "
    "Manuel officiel en français disponible (PDF sur wiki.anycubic.com — le manuel papier des premiers lots était en anglais seul).", S_BODY))
E.append(Paragraph("Les 10 pièges de débutant documentés", S_H2))
E.append(Paragraph(
    "1. Vis de transport oubliées (2+4+3, suivre les flèches rouges). &nbsp;2. Buffers de l'ACE montés à l'envers en usine sur certaines "
    "premières unités (erreur « impossible d'extruder » : vérifier l'orientation). &nbsp;3. <b>Nettoyer le plateau PEI avant le 1er print</b> "
    "(eau chaude + liquide vaisselle, ne plus toucher avec les doigts) — jamais mis en avant par Anycubic, indispensable pour l'adhérence. "
    "&nbsp;4. Slots 3 et 4 de l'ACE parfois capricieux au chargement. &nbsp;5. Wi-Fi 5 GHz invisible (2,4 GHz only). &nbsp;6. TPU jamais via "
    "l'ACE Pro. &nbsp;7. Laisser la clé USB branchée en permanence (timelapse + impression à distance). &nbsp;8. Multi-couleurs = purge énorme : "
    "un Benchy 4 couleurs passe de 1 h 16 à ~14 h 30 avec 310 changements — c'est normal, pas une panne. &nbsp;9. Détection spaghetti IA trop "
    "sensible (désactivable). &nbsp;10. Prévoir 2 prises secteur (alim auto 120/230 V, rien à régler).", S_BODY))
E.append(Spacer(1, 2*mm))
E.append(box("Verdict accessibilité",
    "Un débutant complet s'en sort — consensus unanime (TechRadar la recommande même comme première machine multi-filament). "
    "La réserve : la RÉPARATION (ex. filament cassé dans le circuit ACE) peut demander l'aide du support.", ACCENT_LIGHT, ACCENT))
E.append(PageBreak())

# ================= 3. LA VOIX DES FORUMS =================
E.append(Paragraph("3 · Ce que disent les vrais utilisateurs (forums, Reddit, groupes FB)", S_H1))
E.append(Paragraph(
    "<b>Note de méthode :</b> Reddit, Trustpilot et les groupes Facebook bloquent la lecture directe par les outils automatisés ; les retours "
    "ci-dessous viennent du contenu réel des fils tel qu'indexé par les moteurs de recherche, plus le forum français lesimprimantes3d.fr "
    "(accessible), le wiki officiel Anycubic (dont les guides de dépannage trahissent les pannes récurrentes) et GitHub.", S_SMALL))
E.append(Spacer(1, 2*mm))
E.append(Paragraph("Satisfaction globale : « mixed-positive » avec effet loterie", S_H2))
E.append(Paragraph(
    "Les propriétaires d'une unité saine sont très contents : machine fiable, « set and forget » après des centaines d'heures, meilleur rapport "
    "qualité-prix de la catégorie. Le consensus Reddit ajoute une nuance : la réussite « dépend fortement du setup initial, de l'entretien régulier "
    "et de la volonté de dépanner soi-même ». Les déçus sont vocaux : un early adopter a retourné deux unités successives ; la première unité de "
    "Creative Bloq est morte en 2 semaines (la remplaçante : parfaite). <b>Qui rachèterait ?</b> Ceux qui impriment surtout en mono-couleur "
    "(avec Rinkhals + OrcaSlicer) : oui, massivement. Ceux venus pour le multi-couleurs intensif : bien plus mitigés — c'est la population qui "
    "revend. En français : fils dédiés sur lesimprimantes3d.fr (« Retours Kobra S1 et fiabilité marque Anycubic », mars 2026).", S_BODY))
E.append(Paragraph("Problèmes récurrents, classés par fréquence réelle", S_H2))
freq = [
    ("TRÈS FRÉQUENT", "1. Bourrages dans le chemin filament ACE Pro — LE problème n°1, au point qu'Anycubic a publié un guide de démontage dédié et une série vidéo officielle de dépannage. 2. Bobines carton : patinent et génèrent des débris — problème officiellement reconnu, Anycubic recommande d'imprimer un anneau adaptateur. 3. Purge multi-couleurs énorme + contrôle limité dans le slicer stock. 4. Hotend qui se rebouche (surtout ABS) — guides officiels dédiés ; remède : hotend acier + 10-20 °C. 5. Bruit du sécheur ACE Pro (« une bête bruyante » avec l'ACE actif)."),
    ("FRÉQUENT", "6. Cutter de filament qui se coince (fils dédiés FB + forum FR). 7. Wi-Fi : 2,4 GHz only, déconnexions (antenne), pas de mise à jour firmware en mode LAN. 8. Mises à jour firmware ratées (codes d'erreur officiels 10801/10805) — des bugs « machine figée » ont été corrigés au fil des versions. 9. Loterie QC à réception : unités mortes à l'arrivée documentées (Tom's Hardware, Creative Bloq, Trustpilot) — à chaque fois remplacées rapidement."),
    ("ANECDOTIQUE", "10. Adhérence plateau — quasi toujours résolue par le nettoyage eau chaude + liquide vaisselle. 11. Capteurs (détection filament) — cas isolés, codes d'erreur documentés au wiki."),
]
ft = Table([[Paragraph(f"<b>{k}</b>", S_CELL_B), Paragraph(v, S_CELL)] for k, v in freq],
           colWidths=[30*mm, PAGE_W - 2*M - 30*mm])
ft.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("BACKGROUND", (0,0), (0,0), RED_LIGHT), ("BACKGROUND", (0,1), (0,1), GOLD_LIGHT), ("BACKGROUND", (0,2), (0,2), ACCENT_LIGHT),
    ("LINEBELOW", (0,0), (-1,-2), 0.4, LINE),
    ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3)]))
E.append(ft)
E.append(Paragraph("Citations représentatives (traduites)", S_H2))
E.append(quote("Après des centaines d'heures d'impression, c'est une machine fiable qu'on peut lancer et oublier.", "Maker Hacks — test longue durée"))
E.append(quote("Pour une CoreXY fermée avec multi-filament et séchage actif, c'est le meilleur rapport qualité-prix du marché… mais la S1 et l'ACE Pro forment une bête bruyante, et l'ACE Pro provoque parfois des blocages de filament.", "BGeek"))
E.append(quote("Un Benchy de 10,9 g a produit 183 g de déchets de purge — 17 fois plus de filament gaspillé qu'utilisé. Bonne imprimante, mauvais slicer.", "Tom's Hardware (leur 1re unité est aussi morte d'une puce défectueuse, remplacée par le SAV)"))
E.append(quote("Avec les bobines en papier, des glissements peuvent se produire et générer des débris ; il est recommandé d'imprimer un anneau adaptateur.", "Anycubic, wiki officiel — aveu du problème bobines carton"))
E.append(quote("Nettoyage du plateau à l'eau chaude et liquide vaisselle, essuyage, pas de doigts dessus ensuite.", "Alain D., lesimprimantes3d.fr — LA réponse type aux soucis d'adhérence"))
E.append(quote("Le support Anycubic a répondu vite et professionnellement, et a organisé le remplacement de l'écran sans hésitation.", "Propriétaire S1 Max, Trustpilot"))
E.append(PageBreak())

# ================= 4. ACE PRO EN USAGE RÉEL =================
E.append(Paragraph("4 · L'ACE Pro en usage réel — le maillon faible, et comment vivre avec", S_H1))
E.append(kv([
    ("Fiabilité durée", "Le maillon faible du combo : bourrages au buffer, glissement de bobines. Anycubic recommande de remplacer les tubes PTFE tous les 2 mois en usage normal (tous les mois avec abrasifs). Les utilisateurs multi-ACE (8 couleurs) sont surreprésentés dans les fils de bourrage : plus de tubes = plus de friction."),
    ("Le séchage, honnêtement", "Utile pour MAINTENIR un filament sec pendant l'impression (PETG surtout). Insuffisant pour assécher une bobine vraiment humide (plafond 55 °C). Reste un vrai plus quotidien en climat belge."),
    ("Bobines compatibles", "1 kg standard plastique uniquement (largeur 60-68 mm, diam. 195-200 mm). Carton : adaptateur imprimable obligatoire (reconnu officiellement). Ni 250 g ni 3 kg. Pas de détection de bobine vide sur ce module gen 1."),
    ("TPU", "Jamais via l'ACE Pro — alimentation directe par le porte-bobine arrière (le support de bobine amélioré de Printables est le mod le plus téléchargé pour ça)."),
    ("Passer à 8 couleurs", "2e ACE Pro : 249 € (store EU) + hub filament 8 voies (séparé ou imprimable, guide officiel). Combo 8 couleurs d'usine : 668 €. Peu de retours longue durée sur le chaînage."),
    ("ACE 2 Pro (successeur)", "Sorti depuis : 65 °C, moteurs brushless, joint d'étanchéité, contrôle d'humidité actif — chaque amélioration répond à un mode de défaillance connu de la v1, ce qui en dit long. ATTENTION : ACE Pro et ACE 2 Pro ne se mixent PAS sur la même machine. Un combo « S1 ACE 2 Pro » existe au catalogue (~459 $ US)."),
]))
E.append(Spacer(1, 3*mm))
E.append(Paragraph("5 · Logiciel et firmware — de « mauvais » à « très bon » en un an", S_H1))
E.append(kv([
    ("Slicer Anycubic Next", "Open-source, basé OrcaSlicer. Au lancement : LE point noir (verdict « good printer, bad slicer »). Les mises à jour 2025-2026 ont rattrapé le gros : calcul des volumes de purge activable, Beam Staggering (jonctions multi-couleurs renforcées), Adaptive Pressure Advance, calibration de flux, version Linux. Le contrôle fin de purge reste en deçà d'OrcaSlicer pur."),
    ("OrcaSlicer officiel", "Profils Kobra S1 intégrés en amont dans OrcaSlicer + profils communautaires améliorés (MPC561, ditschi sur GitHub). Config communautaire standard : Rinkhals + OrcaSlicer. Bémol connu : le G-code de changement de filament du profil Orca par défaut diverge de Slicer Next (issue #11632)."),
    ("Firmware Rinkhals", "LE mod de référence (GitHub jbatonnet/Rinkhals, migre vers rinkhals-community). S'installe PAR-DESSUS le firmware stock via USB et garde tout (écran, calibrations, ACE, cloud). Ajoute : Mainsail + Fluidd + Moonraker (contrôle web type Klipper), SSH root, caméra dans l'interface web, impression directe depuis OrcaSlicer, apps (OctoEverywhere, Tailscale, Home Assistant via Moonraker). Risques : brick possible (procédure de récupération existe), zone grise garantie, CPU modeste (ne pas empiler les apps)."),
    ("App mobile / cloud", "Envoi d'impressions + monitoring vidéo multi-machines via le cloud Anycubic (compte requis). Mode LAN 100 % local dispo mais exclusif : LAN activé = app/cloud coupés. App jugée parfois instable (avis bol + presse) ; SimplyPrint supporte officiellement la S1."),
]))
E.append(PageBreak())

# ================= 6. QUALITÉ + VITESSES =================
E.append(Paragraph("6 · Qualité d'impression et vitesses réelles", S_H1))
E.append(kv([
    ("PLA / PETG", "Excellents — « quasi parfaits du premier coup » avec les profils par défaut, stringing minimal. Garage Journal : 80 h+ « sans faute », qualité comparée à Bambu/Prusa. Premières couches fiables grâce au LeviQ 3.0."),
    ("ABS / ASA", "Le point fort distinctif : caisson + 320 °C (vs 300 °C d'un Bambu P1S). Tom's Hardware : « facilement le meilleur ABS jamais sorti de la machine ». ASA haute vitesse OK."),
    ("TPU", "Très bon en alimentation directe (jamais via ACE)."),
    ("Multi-couleurs", "Alignement entre couleurs « fantastique », rendu « niveau professionnel » (3DWithUs). Le coût est ailleurs : temps et purge."),
    ("Vitesse réelle", "Benchy : 13-15 min en rapide, ~44 min en qualité fine. À 600 mm/s la qualité reste correcte sur PLA simple mais varie sur filaments exigeants — 300 mm/s est le réglage de croisière."),
    ("Le vrai prix du multi-couleurs", "~2 min par changement de couleur (vs ~35 s sur le récent Kobra X). Exemples mesurés : masque Kuchisake 73 h en multi vs 9 h en mono (x8) ; Benchy 4 couleurs : 1 h 16 en mono, ~14 h 30 avec 310 swaps. Purge : jusqu'à 17x le poids de la pièce en cas extrême. Mitigations : purge dans l'infill, objets sacrificiels, Flush Volume réduit à ~0.4, regrouper les couleurs par couches."),
    ("Ce que les proprios impriment", "Masques décoratifs grand format multicolores, kits d'enceintes fonctionnels, pièces mécaniques ABS/ASA (boîtiers, supports auto/garage), figurines 4-8 couleurs, pièces sim-racing."),
]))
E.append(Spacer(1, 3*mm))
E.append(Paragraph("7 · Maintenance, pièces, coûts d'usage", S_H1))
E.append(kv([
    ("Entretien courant", "Tiges X : NE PAS graisser (palier graphène autolubrifiant) — chiffon + alcool uniquement. Vis Z : graisse. Cutter : vérifier la lame toutes les 3-5 bobines (usure n°1). PTFE : remplacement ~tous les 2 mois en usage soutenu. Nettoyage plateau régulier."),
    ("Pièces (prix 3DJake, dispo UE)", "Hotend laiton 0,4 : ~13 € · acier trempé 0,4/0,6/0,8 : ~16 € · plaque PEI : ~32 € · courroie X : ~8 € · lame cutter : ~8 € · ventilateurs : ~6,50 € · caméra : ~20 € · extrudeur complet : ~24 € · cartes/alim/écran : 24-45 €. Bonne dispo Europe (3DJake, 3DPrima, Polyfab3D, eu.anycubic.com)."),
    ("Budget entretien annuel", "~30-70 €/an en usage régulier (1-2 hotends, 1 lame, charbon, éventuellement PEI la 2e année) — estimation synthèse, pas une donnée constructeur."),
    ("Garantie", "Machine 1 an (Anycubic) MAIS par composant : hotend/extrudeur/cartes/ventilos 3 mois, lit 6 mois. S'y ajoute la garantie légale UE de 2 ans via le vendeur (Vlotty/bol pour ton achat). SAV = diagnostic en ligne + envoi GRATUIT de pièces + auto-réparation guidée (pas de centre UE physique). Trustpilot : réponses sous 24 h, remplacements sans chichi — confirmé par les 2 cas presse. Rinkhals = zone grise garantie."),
]))
E.append(PageBreak())

# ================= 8. MARCHÉ + VERDICT =================
E.append(Paragraph("8 · Positionnement marché — juin 2026", S_H1))
E.append(Paragraph(
    "<b>Toujours pertinente.</b> Pas de « Kobra S1 v2 » ni de rappel produit ; la gamme s'est étoffée autour d'elle : "
    "<b>Kobra S1 ACE 2 Pro Combo</b> (~459 $, sécheur amélioré, jusqu'à 16 couleurs), <b>Kobra S1 Max</b> (350 mm³, 350 °C) et le petit "
    "<b>Kobra X</b> (~299 $, 4 couleurs natives dans la tête, purge réduite de 81 %, mais architecture plus simple orientée déco/famille). "
    "Chez Bambu, le P1S a été retiré du catalogue au profit du P2S, plus cher — la S1 Combo coûte environ le prix d'un P1S seul "
    "tout en incluant un AMS avec sécheur. Les guides d'achat 2026 la maintiennent comme référence de la case « CoreXY fermée "
    "multi-couleurs ~400-450 € », où elle est quasi seule avec l'Elegoo CC2 Combo. Prix repère : 444 € store officiel FR (promo), "
    "<b>429,99 € sur bol.com</b> (vendeur Vlotty, livraison demain si commande avant 15h) — le bon prix, pas une fausse promo.", S_BODY))
E.append(Spacer(1, 3*mm))
E.append(Paragraph("9 · Verdict final", S_H1))
E.append(box("Pour qui elle est faite — et c'est ton profil",
    "Quelqu'un qui veut une machine fermée, prémontée, qui imprime bien dès le premier jour (PLA/PETG/ABS), avec le multi-couleurs en bonus "
    "et un module qui sèche les bobines en permanence. Un minimum de goût pour la bidouille (toi : largement couvert) transforme la machine : "
    "Rinkhals + OrcaSlicer est LA config communautaire et lève ses deux vraies limites (slicer et cloud).", ACCENT_LIGHT, ACCENT))
E.append(Spacer(1, 2*mm))
E.append(box("Pour qui elle n'est PAS faite",
    "Celui qui veut du multi-couleurs intensif « qui marche tout seul » sans jamais ouvrir un capot : l'ACE Pro est le maillon faible "
    "(bourrages documentés) et la purge/lenteur du multi-couleurs est structurelle. Et celui qui n'accepte aucun risque à réception : "
    "la loterie QC existe — filet de sécurité = SAV réactif + garantie légale belge 2 ans via le vendeur.", RED_LIGHT, RED))
E.append(Spacer(1, 3*mm))
E.append(Paragraph("Check-list du jour 1 (condensé de toute l'étude)", S_H2))
E.append(Paragraph(
    "1. Déballage : suivre les flèches rouges (9 vis), surtout les 3 du plateau.<br/>"
    "2. Nettoyer le plateau PEI à l'eau chaude + liquide vaisselle avant tout print.<br/>"
    "3. Connecter au Wi-Fi 2,4 GHz et faire la mise à jour firmware immédiatement.<br/>"
    "4. Lancer le Benchy de test (13 min) en mono-couleur pour valider l'exemplaire — si quelque chose cloche d'entrée, "
    "ouvrir un ticket SAV sans bricoler : les unités défectueuses se font remplacer.<br/>"
    "5. Premier print utile : l'anneau adaptateur pour bobines carton + le « poop bucket » de purge + le support de bobine amélioré (Printables).<br/>"
    "6. Réglage purge : Flush Volume vers 0.4 + purge dans l'infill pour les prints multi-couleurs.<br/>"
    "7. Dans un mois, quand tu connaîtras la bête : envisager Rinkhals (Mainsail/Fluidd, OrcaSlicer direct, Home Assistant) — "
    "en connaissance de cause pour la garantie.<br/>"
    "8. Stock de consommables conseillé dès la commande : 1 hotend de rechange (~13-16 €) — aucun fourni dans le carton.", S_BODY))
E.append(Spacer(1, 3*mm))
E.append(Paragraph(
    "<b>Conclusion.</b> L'étude approfondie confirme le choix du dossier comparatif, en connaissance de cause : la Kobra S1 Combo est une "
    "excellente machine mono-couleur fermée avec un multi-couleurs honnête mais coûteux en temps/filament, un module sécheur unique dans sa "
    "gamme de prix, un écosystème logiciel devenu bon en 2026, une communauté très active qui a déjà tout corrigé — et deux risques connus "
    "et gérables : la loterie QC (couverte par le SAV + 2 ans de garantie légale) et les bourrages ACE Pro (mitigés par les adaptateurs et "
    "l'entretien). À 429,99 € livrée demain, le rapport équipement/prix reste imbattable sur sa case.", S_BODY))

doc.build(E)
print("OK:", OUT)
