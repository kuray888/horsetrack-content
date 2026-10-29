"""Génère un réel « conversation » (POV message) à partir de modeles/floy_chat.html.
Usage : python3 scripts/make_chat.py  (construit tous les CONFIGS ci-dessous dans modeles/)
Règle de hook v2 : le titre et le 1er message sont visibles dès t = 0 (pas de fondu depuis un écran vide)."""
import json, re, os
BASE = os.path.join(os.path.dirname(__file__), '..', 'modeles')
src = open(os.path.join(BASE, 'floy_chat.html'), encoding='utf-8').read()

CONFIGS = {
 'floy_ep5_dentiste': dict(
  pov='POV : ton cheval<br><i>a ton numéro</i> 📱', ep='ÉPISODE 5 · LE DENTISTE 🦷',
  name='Floy 🐴', avatar='<img src="../captures/avatar.png">',
  msg=[['h','pourquoi y a un monsieur avec une râpe géante dans l’allée ? 😨',-0.4],
       ['h','c’est pour qui ??',1.2],
       ['m','c’est le dentiste mon cœur',2.5],
       ['h','et tu l’as su quand ?',3.8],
       ['m','ce matin… sur le groupe de l’écurie 🙃',5.1],
       ['h','ma dernière visite c’était quand ?',6.6],
       ['m','l’hiver dernier ? ou celui d’avant ?',8.0],
       ['h','tu sais pas. j’en étais sûr 💀',9.5],
       ['h','la prochaine fois tu notes tout dans Horsetrack',10.9],
       ['img','../captures/sante_crop.png',12.1],
       ['h','et tu reçois un rappel la veille. de rien 🙂',15.6]],
  notif=13.8, notif_t='Horsetrack · Rappel', notif_b='Dentiste pour Floy De Tus demain 🦷', end_t=17.4,
  e1='Envoie-le à celle<br><i>qui oublie toujours</i> 👇',
  nx='Un rappel avant chaque soin · gratuit pour 1 cheval<br>Épisode 6 bientôt · abonne-toi'),
 'dp_23h': dict(
  pov='23 h 04.<br><i>Ta DP t’écrit</i> 📱<br>', ep='LA GALÈRE DU SOIR 😬',
  name='Léa · DP de Floy', avatar='<div style="width:100px;height:100px;border-radius:50%;background:#B8B0F2;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;color:#231B6B">L</div>',
  msg=[['h','il a perdu un fer 😬',-0.4],
       ['h','arrière gauche',1.2],
       ['m','NON. le maréchal passe quand déjà ??',2.5],
       ['h','je sais pas, c’est toi qui gères 🙃',4.0],
       ['m','attends je regarde',5.4],
       ['img','../captures/sante_crop.png',6.5],
       ['m','dans 30 jours… j’appelle le maréchal demain pour avancer 📞',9.6],
       ['h','tu peux me partager la fiche, que je suive aussi ?',11.2],
       ['m','je t’ajoute sur la fiche de Floy 👌',12.6],
       ['h','enfin une propriétaire organisée 🥹',13.9]],
  notif=None, notif_t='', notif_b='', end_t=15.6,
  e1='Envoie-le<br><i>à ta DP</i> 👇',
  nx='Partage avec ta DP : inclus dans Premium<br>Gratuit pour 1 cheval sur iPhone'),
 'floy_hs_heure': dict(
  pov='POV : ton cheval<br><i>a ton numéro</i> 📱', ep='SPÉCIAL CHANGEMENT D’HEURE 🌚',
  name='Floy 🐴', avatar='<img src="../captures/avatar.png">',
  msg=[['h','il est quelle heure là ?',-0.4],
       ['m','17 h 30 pourquoi',1.2],
       ['h','il fait NUIT 🌚',2.4],
       ['h','tu viens me voir quand maintenant ?',3.6],
       ['m','à la frontale comme tout le monde 🔦',5.0],
       ['h','génial. et ma séance alors ?',6.5],
       ['m','je la cale samedi matin, quand il fait jour',7.9],
       ['h','tu vas oublier.',9.3],
       ['m','non, elle est dans le planning Horsetrack 📅',10.5],
       ['h','…ok. j’ai rien dit 🙃',13.6]],
  notif=11.9, notif_t='Horsetrack · Rappel', notif_b='Séance de Floy De Tus samedi à 10 h 📅', end_t=15.3,
  e1='Tu montes le matin ☀️<br><i>ou le soir</i> 🌙 ? 👇',
  nx='Ton planning d’écurie · gratuit pour 1 cheval<br>Floy a ton numéro · abonne-toi'),
 'floy_ep6_vacances': dict(
  pov='POV : ton cheval<br><i>a ton numéro</i> 📱', ep='ÉPISODE 6 · LES VACANCES 🧳',
  name='Floy 🐴', avatar='<img src="../captures/avatar.png">',
  msg=[['h','pourquoi t’as une valise ? 🧳',-0.4],
       ['h','tu pars ??',1.2],
       ['m','juste 4 jours pour la Toussaint 🙈',2.5],
       ['h','et qui me nourrit ? qui me sort ? qui me fait des bisous ?',3.9],
       ['m','Léa, ta DP 💜',5.5],
       ['h','elle sait que j’ai peur des bâches ?',6.8],
       ['h','elle sait quand passe le maréchal ??',8.1],
       ['m','je lui ai partagé ta fiche, elle a tout 👇',9.5],
       ['img','../captures/partage_crop.png',10.7],
       ['h','ok. mais tu me ramènes des carottes 🥕',14.0]],
  notif=None, notif_t='', notif_b='', end_t=15.8,
  e1='Envoie-le à ta DP<br><i>avant de partir</i> 👇',
  nx='Partage avec ta DP : inclus dans Premium<br>Gratuit pour 1 cheval · Floy a ton numéro'),
 'maman_dimanche': dict(
  pov='Dimanche midi.<br><i>Ta mère t’écrit</i> 📱', ep='LA VIE DE PROPRIÉTAIRE 🐴',
  name='Maman 💐', avatar='<div style="width:100px;height:100px;border-radius:50%;background:#B8B0F2;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;color:#231B6B">M</div>',
  msg=[['h','tu viens déjeuner aujourd’hui ? 🍗',-0.4],
       ['m','je peux pas, je suis à l’écurie',1.3],
       ['h','encore ?',2.6],
       ['h','et dimanche prochain ?',3.7],
       ['m','le maréchal passe 🔨',4.9],
       ['h','et Noël ??',6.2],
       ['m','attends je regarde son planning',7.5],
       ['img','../captures/sante_crop.png',8.6],
       ['m','c’est bon, Noël je suis libre 🎄',11.0],
       ['h','ton cheval a un meilleur agenda que moi 😭',12.4]],
  notif=None, notif_t='', notif_b='', end_t=14.3,
  e1='Envoie-le à ta mère<br><i>(elle comprendra)</i> 👇',
  nx='Le planning de ton cheval · gratuit pour 1 cheval<br>Sur iPhone · lien en bio'),
 'floy_hs_equita': dict(
  pov='POV : ton cheval<br><i>a ton numéro</i> 📱', ep='SPÉCIAL EQUITA LYON 🛍️',
  name='Floy 🐴', avatar='<img src="../captures/avatar.png">',
  msg=[['h','t’es où ? ça fait 2 jours 👀',-0.4],
       ['m','à Equita Lyon 🤩',1.2],
       ['h','c’est quoi',2.3],
       ['m','un salon… plein de chevaux',3.4],
       ['h','D’AUTRES CHEVAUX ???',4.6],
       ['m','non mais j’y suis pour toi !',5.9],
       ['h','ah. tu m’as acheté quoi ?',7.2],
       ['m','un tapis 💜 et un bonnet assorti',8.4],
       ['h','j’ai déjà 9 tapis.',9.7],
       ['m','oui mais pas violets',10.8],
       ['h','et tu as dépensé combien ?',12.0],
       ['m','je note tout dans le budget Horsetrack 💸',13.2],
       ['h','montre-moi le total du mois 🙂',14.5],
       ['m','…non.',15.6]],
  notif=None, notif_t='', notif_b='', end_t=17.0,
  e1='Envoie-le à ta copine<br><i>de shopping</i> 👇',
  nx='Ton budget cheval · gratuit pour 1 cheval<br>Floy a ton numéro · abonne-toi'),
 'pension_couverture': dict(
  pov='7 h 12.<br><i>La pension t’écrit</i> 📱', ep='LA GALÈRE DE NOVEMBRE 🧥',
  name='Sophie · pension', avatar='<div style="width:100px;height:100px;border-radius:50%;background:#B8B0F2;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;color:#231B6B">S</div>',
  msg=[['h','bonjour ! petit souci avec Floy 😬',-0.4],
       ['h','il a retiré sa couverture cette nuit',1.2],
       ['m','retiré ? comment ça retiré ??',2.5],
       ['h','elle est dans la boue. en 2 morceaux.',3.8],
       ['m','c’est la neuve 😭',5.1],
       ['h','il a l’air très fier de lui',6.4],
       ['m','il fait combien ce matin ?',7.6],
       ['h','3 degrés. je lui mets celle de secours ?',8.8],
       ['m','oui merci 🙏 je passe ce soir',10.2],
       ['m','et je note la couture dans son budget… encore 💸',11.5],
       ['h','c’est la 2e ce mois-ci 🙃',12.9]],
  notif=None, notif_t='', notif_b='', end_t=14.6,
  e1='Envoie-le à ta copine<br><i>d’écurie</i> 👇',
  nx='Budget, soins, rendez-vous · gratuit pour 1 cheval<br>Sur iPhone · lien en bio'),
 'floy_ep7_tonte': dict(
  pov='POV : ton cheval<br><i>a ton numéro</i> 📱', ep='ÉPISODE 7 · LA TONTE 🪒',
  name='Floy 🐴', avatar='<img src="../captures/avatar.png">',
  msg=[['h','pourquoi t’as sorti la tondeuse ? 😨',-0.4],
       ['h','on est en NOVEMBRE',1.2],
       ['m','justement, tu transpires sous ta couverture 🙃',2.5],
       ['h','et après j’aurai froid moi ?',3.8],
       ['m','t’auras ta couverture, promis 🧥',5.1],
       ['h','tu me fais quoi comme dessin ?',6.4],
       ['m','une tonte irlandaise, ça t’ira très bien',7.7],
       ['h','l’an dernier t’as raté le côté gauche.',9.1],
       ['h','j’ai de la mémoire. toi non.',10.4],
       ['m','c’est pour ça que je note tout dans ton journal 📸',11.7],
       ['img','../captures/journal_crop.png',12.9],
       ['h','garde la photo où je suis beau. pas celle d’après 🙂',16.4]],
  notif=None, notif_t='', notif_b='', end_t=18.2,
  e1='Ép. 8 : tu choisis<br><i>1 · la boue<br>2 · le véto<br>3 · Noël</i>',
  nx='Réponds 1, 2 ou 3 en commentaire<br>Son journal · gratuit pour 1 cheval sur iPhone'),
 'groupe_ecurie': dict(
  pov='7 h 03.<br><i>Le groupe de l’écurie</i> 📱', ep='47 MESSAGES NON LUS 😵',
  name='Écurie des Chênes 🐴', avatar='<div style="width:100px;height:100px;border-radius:50%;background:#B8B0F2;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;color:#231B6B">É</div>',
  msg=[['h','Julie : QUI a laissé le pré ouvert ?? 😡',-0.4],
       ['h','Marc : pas moi',1.2],
       ['h','Julie : 4 chevaux dans le potager du proprio',2.4],
       ['h','Inès : ah c’était pour ça les carottes 🥕',3.7],
       ['h','Sophie : rappel, maréchal JEUDI 8 h 🔨',5.0],
       ['h','Marc : c’est pas mardi ?',6.3],
       ['h','Inès : il m’a dit mercredi 🙃',7.5],
       ['m','chez moi c’est noté jeudi 8 h, avec un rappel la veille',8.9],
       ['h','Inès : tu peux faire un screen pour tout le monde 🙏',11.9],
       ['h','Julie : et le pré, alors ?? c’était qui ?',13.3]],
  notif=10.2, notif_t='Horsetrack · Rappel', notif_b='Maréchal-ferrant pour Floy De Tus demain à 8 h 🔨', end_t=15.0,
  e1='Identifie celle<br><i>qui a laissé le pré ouvert</i>',
  nx='Tes rendez-vous avec un rappel · gratuit pour 1 cheval<br>Sur iPhone · lien en bio'),
}

for name, c in CONFIGS.items():
    h = src
    c['msg'] = [[w, t.replace(' ?', '\u00a0?').replace(' !', '\u00a0!') if w != 'img' else t, a] for w, t, a in c['msg']]
    c['e1'] = c['e1'].replace(' 👇', '')
    h = re.sub(r'<div class="abs" id="pov">.*?</div></div>',
               f'<div class="abs" id="pov">{c["pov"]}<div id="ep">{c["ep"]}</div></div>', h, flags=re.S)
    h = h.replace('<img src="../captures/avatar.png"><div><div class="n">Floy 🐴</div>',
                  f'{c["avatar"]}<div><div class="n">{c["name"]}</div>')
    h = h.replace('<div class="t">Horsetrack · Rappel</div><div class="b">Maréchal-ferrant pour Floy De Tus dans 3 jours 🔨</div>',
                  f'<div class="t">{c["notif_t"]}</div><div class="b">{c["notif_b"]}</div>')
    h = re.sub(r'<div class="abs" id="e1">.*?</div>', f'<div class="abs" id="e1">{c["e1"]}</div>', h, flags=re.S)
    h = re.sub(r'<div class="abs" id="nx">.*?</div>', f'<div class="abs" id="nx">{c["nx"]}</div>', h, flags=re.S)
    h = re.sub(r'const MSG=\[.*?\n\];', 'const MSG=' + json.dumps(c['msg'], ensure_ascii=False) + ';', h, flags=re.S)
    notif = 'null' if c['notif'] is None else str(c['notif'])
    h = h.replace('const NOTIF=14.2, END_T=18.6,', f'const NOTIF={notif}, END_T={c["end_t"]},')
    h = h.replace(".concat([[NOTIF,'notif']]);", ".concat(NOTIF===null?[]:[[NOTIF,'notif']]).filter(s=>s[0]>=0);")
    # hook visible à t=0 : plus de fondu d'opacité, juste une petite pulsation
    h = h.replace("const hp=oB(P(t,0,0.45)); tf($('#pov'),{s:0.7+0.3*hp,o:P(t,0,0.1)});",
                  "const hp=oB(P(t,0,0.45)); tf($('#pov'),{s:0.94+0.06*hp,o:1});")
    h = h.replace("tf($('#head'),{y:(1-oC(P(t,0.1,0.4)))*-40,o:P(t,0.1,0.25)});", "tf($('#head'),{o:1});")
    h = h.replace("const np=oB(P(t,NOTIF,0.5)), nq=io(P(t,NOTIF+1.35,0.35));",
                  "const np=NOTIF===null?0:oB(P(t,NOTIF,0.5)), nq=NOTIF===null?0:io(P(t,NOTIF+1.35,0.35));")
    h = h.replace("const buzz=(t>NOTIF&&t<NOTIF+0.4)", "const buzz=(NOTIF!==null&&t>NOTIF&&t<NOTIF+0.4)")
    h = h.replace("window._ov=(window._ov===undefined?over:window._ov+(over-window._ov)*0.3)", "window._ov=(window._ov===undefined||t===0?over:window._ov+(over-window._ov)*0.3)")
    open(os.path.join(BASE, name + '.html'), 'w', encoding='utf-8').write(h)
    print('ok', name)
