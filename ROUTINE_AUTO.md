# Routine automatique Horsetrack — analyse → décision → production → publication

Exécutée **chaque lundi et chaque jeudi matin** par une tâche programmée.
La fondatrice a donné **carte blanche** (17/10/2026) : tu analyses, tu changes les hooks, les formats, les concepts et les horaires, tu produis et tu **programmes directement en publication automatique** (`draft: false`). Elle reçoit seulement le récap.

Objectif unique : **plus d'abonnés Instagram et plus de téléchargements de l'app**. Les vues ne comptent que si elles mènent à ça.

---

## 0. Garde-fous (non négociables)

1. Marque Metricool **Horsetrack uniquement** (`blogId 7469064`, Instagram @horsetrack.app). Ne jamais toucher une autre marque (ex. « alfit.lifee »).
2. Réseaux : Instagram. TikTok seulement s'il apparaît relié dans `getBrandSettings` (sinon, ne rien créer pour TikTok).
3. Règles de contenu (voir aussi `INSTRUCTIONS_CLAUDE.md`) :
   - vermifuge autorisé depuis le 21/10/2026 (décision de la fondatrice), uniquement comme rendez-vous/échéance à ne pas oublier : jamais de produit, de molécule, de dose ni de fréquence conseillée — « demande à ton véto » ;
   - maréchal : 5–6 semaines ; vaccins : 1 an (national) ou 6 mois (CSI) ; vaccin pas à jour = pas de départ ;
   - l'app organise, elle ne soigne pas : pour la santé, renvoyer vers le véto ; aucun conseil médical chiffré inventé ;
   - ne promettre que des fonctions réelles : iPhone uniquement, gratuit pour 1 cheval, Premium 3,99 €/mois ou 39,99 €/an ; planning, séances, soins & rappels, concours, journal (ressenti, photo, météo auto), budget, documents ; partage DP/coach = Premium ;
   - **jamais** de faux avis, faux témoignages, faux UGC présenté comme une vraie cliente, faux chiffres d'utilisateurs ;
   - ton : tutoiement, complice, autodérision de cavalière, zéro jargon marketing ;
   - charte : fond #F6F4F0, principal #231B6B, accents #6C5FD6 / #B8B0F2, rouge #E5533D seulement pour les erreurs ; titres Fraunces, texte Inter ; cheval de démo Floy De Tus.
4. Voix off IA : interdite sans MP3 fourni par la fondatrice. Si une vidéo contient de l'IA générative, déclarer `isAiGenerated: true`.
5. Pas de musique sous droits. Bruitages + fond synthétisé de `scripts/render_reel.py` uniquement.
6. **Contrôle qualité obligatoire avant publication** : générer 6–8 images d'aperçu de chaque vidéo (`render_reel.py preview`) et les **regarder** (Read). Texte coupé, chevauchement, faute, emoji manquant, info fausse → corriger et re-rendre. Si un doute persiste sur une vidéo (santé, exactitude, goût), la programmer en **brouillon** (`draft: true`) et le signaler dans le récap au lieu de la publier.
7. Volume : maximum **2 publications Instagram par jour**, minimum 1. Espacer d'au moins 6 h.
8. Ne jamais supprimer ni modifier un post déjà publié. Tu peux modifier/remplacer un post **programmé futur** si l'analyse le justifie (le noter dans le journal).
9. Si un appel échoue : ne pas boucler (un seul nouvel essai après avoir relu l'état avec `getScheduledPosts`), noter, continuer.

---

## 0 bis. Stratégie de croissance v2 (19/10/2026), à appliquer à chaque cycle

Diagnostic du 19/10 : environ 1 abonné net par jour, et un hook sous 31 % sur tous les réels. À ce rythme, il faudrait environ 2 ans pour atteindre 1 000 abonnés. Objectif : **≥ 15 abonnés nets par semaine dès maintenant, ≥ 30 à partir de mi-novembre, ≥ 60 ensuite**.

1. **Hook d'abord.** Sur la 1re image (t = 0), on voit déjà le texte du hook en entier (8 mots maximum, en gros) **et** la situation (carte, appel, notification). Pas de fondu depuis un écran vide, pas de logo au début. Il faut du mouvement avant 0,5 s. On n'apporte qu'une seule idée par vidéo, qui dure entre 12 et 20 s.
2. **Volume.** Tous les jours : 1 réel dans le fil, plus **1 Trial Reel** (`instagramData.type = "TRIAL_REEL"`), montré d'abord aux non-abonnés, jusqu'à 1 par jour, sans dépasser 2 publications par jour au total. Les Trial Reels servent à **tester les nouveaux concepts et hooks** sans encombrer le fil. Si un Trial Reel fait plus de 1,5 fois la médiane des vues : en refaire une variante pour le fil et prévenir la fondatrice. Elle peut aussi le « partager avec les abonnés » depuis l'app Instagram. Note : via l'API Metricool, `shareTrialAutomatically: true` est ignoré (reste à false, testé le 19/10).
3. **Faire parler et partager.** Chaque post se termine par une question facile à laquelle on répond en 1 mot ou 1 emoji (« 1, 2 ou 3 », « ton cheval en 3 emojis », « tu en coches combien ? »). Ajouter aussi « envoie-le à ta copine d'écurie ». **1 carrousel utile par semaine** du type « enregistre-le » (checklists, budget, calendrier de soins sans conseil médical) : ce sont les enregistrements qui font sortir le compte de sa base d'abonnés.
4. **Séries qui fidélisent.** « Floy a ton numéro », et une série pilotée par les commentaires (« le commentaire le plus liké devient l'épisode suivant »).
5. **Saisonnalité** (toujours vérifier les dates par une recherche web) : Equita Lyon du 28/10 au 1/11 ; vacances de la Toussaint jusqu'au 2/11 ; froid, couvertures et boue en novembre ; Salon du Cheval de Paris (dates à vérifier) ; cadeaux de Noël pour cavalière en décembre ; bilan et objectifs de saison en janvier (fonction Objectifs).
6. **Mesure.** À chaque cycle, regarder le hook (> 3 s), la durée moyenne vue par rapport à la durée de la vidéo, les partages et enregistrements pour 1 000 vues, et les abonnés gagnés. Vues des Trial Reels comparées à celles du fil. Ne juger qu'après 48 h.
7. **Ce que la routine ne peut pas faire** : répondre aux commentaires, envoyer des messages, faire des collaborations, modifier la bio, modifier l'App Store. Ces actions sont listées dans `PLAN_FONDATRICE.md` : les rappeler dans le récap tant qu'elles ne sont pas faites.

## 0 ter. Mandat du directeur de la croissance (fondatrice, 21/10/2026)

- **Mission** : faire percer les vidéos, gagner des abonnés qualifiés, générer des téléchargements. Carte blanche sur les concepts, les hooks et les formats.
- **Ce qu'on peut dire de l'app** : gratuit pour 1 cheval sans limite de durée ; 1 mois d'essai Premium ; sans pub ; Face ID ; carnet de santé en PDF. Premium : chevaux illimités, rappels illimités, coffre-fort documents, partage avec la DP, le coach ou le groom, suivi concours détaillé. Pas d'Android. Pas de conseil vétérinaire.
- **Analyse** : pour chaque vidéo, relever vues, durée moyenne vue, % vu en entier, partages, enregistrements, commentaires, abonnés gagnés. **Partages, enregistrements et abonnés comptent plus que les vues.**
- **Diagnostic** : classer les vidéos en **top 20 % et flop 20 %**. Pour chaque top : pourquoi elle a marché (hook, sujet, format, émotion, durée, heure). Pour chaque flop : le point de décrochage le plus probable (souvent les 2 premières secondes).
- **Décision** : **70 % de formats qui ont fait leurs preuves** (déclinaisons, suites, séries), **30 % d'expériences nouvelles**. Cette règle remplace le 60/30/10 du § 3.
- **Hook** : tout se joue en 1,5 s. Écrire **3 hooks par vidéo** et garder le plus fort. Tenir à jour `analyses/banque_hooks.md`. Types à tester : galère reconnaissable, question piège, chiffre choc, POV humour, « personne n'en parle », liste.
- **Récap** : ce qui a marché, ce qu'on a appris, ce qu'on change, et **les 3 meilleures idées de la semaine**.

---

## 1. Collecte (Metricool)

- `getBrandSettings` → vérifier la marque et les réseaux reliés.
- Réels publiés depuis le début (ou 28 derniers jours) : `getAnalyticsDataByMetrics`, réseau instagram, connecteur reels :
  `IGRE02` date/heure, `IGRE03` texte, `IGRE06` url, `IGRE11` portée, `IGRE23` vues, `IGRE28` taux de vue >3 s (**le hook**), `IGRE27` rétention %, `IGRE24` durée moyenne vue, `IGRE21` partages, `IGRE12` enregistrements, `IGRE07` commentaires, `IGRE10` likes, `IGRE26` durée vidéo.
- Compte : `IGEV01` abonnés, `IGEV43` abonnés gagnés, `IGEV44` perdus, `IGEV06` portée du compte, par jour.
- Carrousels : connecteur posts (lister avec `getAnalyticsAvailableMetrics` si besoin).
- Relier chaque réel à son concept grâce à `historique.md` et aux `planning/*.json` (titre, légende, fichier).
- Enregistrer les données brutes dans `analyses/donnees_AAAA-MM-JJ.json`.

## 2. Analyse

Un réel n'est jugé qu'après **48 h** de vie. Indicateurs, dans cet ordre :
1. **Hook** = taux de vue >3 s (`IGRE28`). < 50 % : le début ne retient pas → changer la 1re image/phrase.
2. **Rétention** (`IGRE27`) et durée moyenne vs durée vidéo. Vidéo trop longue pour sa rétention → raccourcir le format.
3. **Partages + enregistrements pour 1 000 vues** : c'est ce qui fait sortir Instagram de la base d'abonnés.
4. **Abonnés gagnés** les jours de publication (corrélation, pas preuve).
5. Commentaires : le CTA fonctionne-t-il ?

Classer les **concepts/formats** (pas seulement les vidéos) : POV notifications, quiz, journal/émotion, Floy a ton numéro, dis vs réalité, mets pause, carrousel utile, coût/budget, actu de saison…
Prudence statistique : avec < 3 vidéos par concept ou < 300 vues, parler de **tendance**, pas de conclusion. Ne jamais tuer un concept sur une seule vidéo, sauf hook < 30 %.

## 3. Décision (règle d'allocation)

Pour les publications du prochain cycle :
- **~60 %** : variantes des concepts gagnants (nouveau sujet, même mécanique ; ou même vidéo avec un **nouveau hook** testé).
- **~30 %** : itérations sur les concepts moyens (hook différent, plus court, CTA différent, autre horaire).
- **~10 %** (au moins 1 par semaine) : **un concept totalement nouveau** à tester.
- Couper un concept après 3 vidéos sous la médiane sur hook ET partages.
- Tester les horaires : garder 18 h–19 h en base, essayer 1 créneau différent par semaine (ex. 12 h 30, 21 h), comparer.
- Ancrer au moins 1 vidéo par cycle dans l'actualité/saison équestre (vérifier les dates par recherche web : concours, salons type Equita Lyon, météo, fêtes, vacances scolaires).

Idées de concepts à tester quand il faut du neuf (non exhaustif) : « ton cheval en 3 emojis », « red flags / green flags d'une pension », « classement des tâches d'écurie », « avant/après d'une semaine organisée », « ce que coûte une sortie en concours », « choses que seules les propriétaires comprennent », « le checklist du coffre de concours », « réponds en commentaire et je fais la suite » (série pilotée par les commentaires), carrousels « enregistre-le » très utiles.

## 4. Production

- Horizon : avoir **toujours 5 à 6 jours de publications programmées d'avance**. Lundi : remplir jusqu'au dimanche ; jeudi : jusqu'au mercredi suivant. Ne pas dupliquer un créneau déjà rempli (`getScheduledPosts`).
- Modèles animés dans `modeles/` (fonction `render(t)`, `END`, `SOUNDS`). Créer de nouveaux modèles librement en s'inspirant de `ecran_notifs.html`, `quiz_cheval.html`, `journal_souvenirs.html`. Captures de l'app dans `captures/`.
- Rendu : `python3 scripts/render_reel.py preview modeles/X.html <dossier> t1 t2 …` puis `python3 scripts/render_reel.py video modeles/X.html medias/videos/Horsetrack_Reel_<Nom>.mp4 rythme|calme`.
  (installer si besoin : `pip install --break-system-packages playwright soundfile numpy` ; Chromium : `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.)
- Règles de forme qui marchent sur les réels : texte lisible en 1 s, hook visible dès la 1re image (pas d'intro vide), 12–25 s pour un réel classique (quiz/série jusqu'à 30 s), une seule fonction de l'app par vidéo, CTA final « Gratuit pour 1 cheval · lien en bio ».
- Légende : la 1re ligne = un hook qui donne envie de dérouler ; puis question pour les commentaires ; 1 phrase app ; 5–8 hashtags (large + niche).
- Carrousels : 1080×1350, `scripts/render_car.py` et `modeles/carrousel.html`.

## 5. Publication

- Pousser médias, modèles et `planning/programmation_AAAA-MM-JJ.json` sur `main` ; vérifier que chaque URL raw répond 200.
- `createScheduledPost` : `blogId 7469064`, `draft: false`, `autoPublish: true`, `publicationDate` en Europe/Paris, `date` avec le bon décalage (+02:00 en heure d'été, +01:00 en heure d'hiver), `instagramData {"type":"REEL","showReelOnFeed":true,"isAiGenerated":false}` (ou `{"type":"POST"}` pour un carrousel).
- Relire avec `getScheduledPosts` : bonne date, pas de doublon, `draft` correct.

## 6. Mémoire et récap

- Ajouter une entrée dans `analyses/journal.md` : date du cycle, chiffres clés (abonnés, meilleurs/pires réels avec hook %, rétention, partages), **décisions prises et pourquoi**, hypothèses en test, ce qu'on regardera au prochain cycle.
- Mettre à jour `historique.md` (une ligne par publication : date, format/concept, sujet, statut).
- Commit + push.
- Envoyer à la fondatrice un **récap court** (SendUserMessage), en français, tutoiement :
  1. abonnés : total et +/− depuis le dernier cycle ;
  2. ce qui marche / ce qui ne marche pas (2–3 lignes, chiffres) ;
  3. ce que tu as changé et pourquoi ;
  4. le planning programmé (tableau date / heure / vidéo) ;
  5. ce qu'elle doit faire, s'il y a quelque chose (ex. relier TikTok, répondre aux commentaires, un brouillon douteux à regarder).
