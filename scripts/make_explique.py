"""Génère les réels « Floy t'explique » (personnage qui parle, fond quadrillé) à partir de modeles/floy_explique_base.html.
Usage : python3 scripts/make_explique.py"""
import json, os
BASE = os.path.join(os.path.dirname(__file__), '..', 'modeles')
src = open(os.path.join(BASE, 'floy_explique_base.html'), encoding='utf-8').read()
NB = ' '
def fix(s): return s.replace(' ?', NB + '?').replace(' !', NB + '!').replace(' :', NB + ':').replace('« ', '«' + NB).replace(' »', NB + '»')
CONFIGS = {
 'floy_explique_1_amour': dict(
  ep='FLOY T’EXPLIQUE · LEÇON 1', title='Comment savoir si<br>ta propriétaire <i>t’aime</i> 💜',
  lines=[['Signe n°1 : elle arrive avec des carottes. Facile.', '🥕', ''],
         ['Signe n°2 : elle connaît la date du maréchal…', '🔨', ''],
         ['…sans fouiller le groupe de l’écurie pendant 20 minutes.', '💬', '20 min'],
         ['Signe n°3 : elle note mes séances. Même les ratées.', '📒', ''],
         ['La mienne a tout dans Horsetrack, avec un rappel. Donc oui : elle m’aime.', '📱', 'Horsetrack'],
         ['Et la tienne, elle coche combien de signes ?', '👇', '']],
  end_q='Ta propriétaire<br>coche <i>combien de signes</i> ?'),
 'floy_explique_2_budget': dict(
  ep='FLOY T’EXPLIQUE · LEÇON 2', title='Pourquoi je coûte<br><i>si cher</i> 💸',
  lines=[['Spoiler : c’est pas ma faute.', '🙅', ''],
         ['La pension ? Il faut bien que je dorme quelque part.', '🏠', ''],
         ['Le maréchal ? Toutes les 5 à 6 semaines. C’est la règle.', '🔨', '5–6 sem.'],
         ['Le 9e tapis violet ? Ça, c’est elle.', '🛍️', 'elle'],
         ['Le bonnet assorti ? Encore elle.', '🧢', 'encore elle'],
         ['Elle note tout dans le budget Horsetrack. Moi, je regarde le total… et je ris.', '📊', 'budget'],
         ['Ton cheval te coûte combien par mois ? Plus ou moins ?', '👇', '']],
  end_q='Ton cheval te coûte<br><i>combien par mois</i> ?'),
}
for name, c in CONFIGS.items():
    lines = [[fix(a), b, l] for a, b, l in c['lines']]
    h = src.replace('__EP__', c['ep']).replace('__TITLE__', fix(c['title'])).replace('__END_Q__', fix(c['end_q']))
    h = h.replace('__LINES__', json.dumps(lines, ensure_ascii=False))
    open(os.path.join(BASE, name + '.html'), 'w', encoding='utf-8').write(h)
    print('ok', name)
