# Instructions pour Claude — Programmation Horsetrack dans Metricool

Ce fichier est la source de vérité pour programmer et gérer les publications Instagram et TikTok de **Horsetrack** (app iPhone de suivi du cheval, https://horsetrack.fr).

## Règles absolues
1. **Uniquement la marque Horsetrack** dans Metricool. Ne jamais toucher à une autre marque (par exemple « alfit.lifee »). Si aucune marque Horsetrack n'est visible, s'arrêter et le dire.
2. **Toujours en brouillon** : `"draft": true` dans chaque post. Rien n'est publié sans validation de la fondatrice dans l'app Metricool.
3. Fuseau horaire : `Europe/Paris`.
4. Avant de programmer, appeler `getScheduledPosts` sur la période pour **ne pas créer de doublon**.
5. Si un appel échoue, ne pas le relancer en boucle : noter l'erreur et passer au post suivant, puis faire un récapitulatif.

## Où sont les fichiers
- Dépôt GitHub public : https://github.com/kuray888/horsetrack-content (branche `main`)
- Planning à programmer : `planning/programmation_2026-10-19.json` → https://raw.githubusercontent.com/kuray888/horsetrack-content/main/planning/programmation_2026-10-19.json
- URL publique d'un média = `https://raw.githubusercontent.com/kuray888/horsetrack-content/main/` + le chemin indiqué dans `media` (ex. `https://raw.githubusercontent.com/kuray888/horsetrack-content/main/medias/videos/Horsetrack_Court_vaccins.mp4`).
- Chaque entrée du JSON contient : `network`, `date` (heure de Paris), `type`, `title`, `caption` (légende complète avec hashtags), `media` (liste de chemins).

## Correspondance JSON → Metricool (`createScheduledPost`)
Un post par entrée du JSON (Instagram et TikTok séparés, car les légendes diffèrent).

- `blogId` : l'id de la marque Horsetrack donné par `getBrandSettings`.
- `date` : la date du JSON + `+02:00` jusqu'au 24 octobre inclus, `+01:00` à partir du 25 octobre (changement d'heure).
- `info.text` : `caption`. `info.media` : les URL publiques. `info.draft` : true. `info.providers` : `[{"network":"instagram"}]` ou `[{"network":"tiktok"}]`.
- `info.publicationDate` : `{"dateTime": date du JSON, "timezone": "Europe/Paris"}`.
- Instagram `REEL` → `"instagramData": {"type":"REEL","showReelOnFeed":true,"isAiGenerated":<voir colonne IA>}`.
- Instagram `CAROUSEL` → `"instagramData": {"type":"POST"}` avec les 8 images dans l'ordre.
- TikTok `VIDEO` → `"tiktokData": {"privacyOption":"PUBLIC_TO_EVERYONE","isAigc":<voir colonne IA>,"title":title}`.
- TikTok `PHOTO_CAROUSEL` → `"tiktokData": {"privacyOption":"PUBLIC_TO_EVERYONE","photoCoverIndex":0,"autoAddMusic":true}`.
- Colonne **IA** = la vidéo contient une voix off générée par IA (ElevenLabs) → déclarer `true`. Les autres sont des animations sans voix → `false`.

## Planning de la première vague (23 posts)
| # | Date (Paris) | Réseau | Type | Titre | Média | IA |
|---|---|---|---|---|---|---|
| 1 | 2026-10-19 12:30 | tiktok | VIDEO | Floy a ton numéro · ép. 1 | Horsetrack_Reel_FloyMessages.mp4 | non |
| 2 | 2026-10-19 18:30 | instagram | CAROUSEL | Ton cheval est-il prêt pour l’hiver ? | 8 images c1 | non |
| 3 | 2026-10-19 19:00 | tiktok | VIDEO | Mets pause : quel type de cavalière ? | Horsetrack_Reel_MetsPause.mp4 | non |
| 4 | 2026-10-20 12:30 | tiktok | VIDEO | Le maréchal arrive dans 10 min | Horsetrack_Court_marechal.mp4 | oui |
| 5 | 2026-10-20 19:00 | instagram | REEL | « Floy a ton numéro » — épisode 3 : la demi-pension | Horsetrack_Reel_Floy_Ep3_DP.mp4 | non |
| 6 | 2026-10-20 19:00 | tiktok | VIDEO | Floy a ton numéro · ép. 2 · concours | Horsetrack_Reel_Floy_Ep2_Concours.mp4 | non |
| 7 | 2026-10-21 12:30 | tiktok | PHOTO_CAROUSEL | Carrousel photo : prêt pour l’hiver ? | 8 images c1 | non |
| 8 | 2026-10-21 18:30 | instagram | CAROUSEL | Ton cheval a plus de rendez-vous que toi | 8 images c2 | non |
| 9 | 2026-10-21 19:00 | tiktok | VIDEO | Ce que je dis vs la réalité | Horsetrack_Reel_DisVsRealite.mp4 | non |
| 10 | 2026-10-22 12:30 | tiktok | VIDEO | Mets pause : quel cheval as-tu ? | Horsetrack_Reel_MetsPause_QuelCheval.mp4 | non |
| 11 | 2026-10-22 19:00 | instagram | REEL | Ce que je dis vs la réalité | Horsetrack_Reel_DisVsRealite.mp4 | non |
| 12 | 2026-10-22 19:00 | tiktok | VIDEO | Floy a ton numéro · ép. 3 · la DP | Horsetrack_Reel_Floy_Ep3_DP.mp4 | non |
| 13 | 2026-10-23 12:30 | tiktok | VIDEO | Vaccin pas à jour = pas de départ | Horsetrack_Court_vaccins.mp4 | oui |
| 14 | 2026-10-23 18:00 | instagram | REEL | Vaccin pas à jour ? Pas de départ | Horsetrack_Court_vaccins.mp4 | oui |
| 15 | 2026-10-23 19:00 | tiktok | VIDEO | Cavalière de concours : dis vs réalité | Horsetrack_Reel_DisVsRealite_Concours.mp4 | non |
| 16 | 2026-10-24 10:00 | instagram | REEL | Changement d’heure : l’écurie le soir | Horsetrack_Reel_ChangementHeure.mp4 | non |
| 17 | 2026-10-24 10:00 | tiktok | VIDEO | Changement d’heure | Horsetrack_Reel_ChangementHeure.mp4 | non |
| 18 | 2026-10-24 18:00 | tiktok | VIDEO | Combien coûte vraiment un cheval ? | Horsetrack_Reel_CoutCheval.mp4 | non |
| 19 | 2026-10-25 11:00 | tiktok | VIDEO | 3 erreurs de propriétaires | Horsetrack_Reel_3Erreurs_v2.mp4 | oui |
| 20 | 2026-10-25 19:00 | tiktok | VIDEO | Floy a ton numéro · ép. 4 · l’hiver | Horsetrack_Reel_Floy_Ep4_Hiver.mp4 | non |
| 21 | 2026-10-26 19:00 | instagram | REEL | Floy a ton numéro · ép. 4 · l’hiver | Horsetrack_Reel_Floy_Ep4_Hiver.mp4 | non |
| 22 | 2026-10-28 18:30 | instagram | REEL | Mets pause : quel cheval as-tu ? | Horsetrack_Reel_MetsPause_QuelCheval.mp4 | non |
| 23 | 2026-10-30 19:00 | instagram | REEL | Cavalière de concours : dis vs réalité | Horsetrack_Reel_DisVsRealite_Concours.mp4 | non |

## Après la programmation
1. `getScheduledPosts` du 19 octobre au 1er novembre : vérifier que les 23 brouillons existent, à la bonne heure, sur la bonne marque.
2. Envoyer à la fondatrice un récapitulatif court : nombre de brouillons créés, erreurs éventuelles, et le rappel « Ouvre Metricool → Planificateur → valide chaque brouillon ». Pour TikTok, Metricool envoie une notification à valider dans l'app.
3. Mettre à jour `historique.md` dans le dépôt (statut « programmé en brouillon »).

## Routine hebdomadaire (chaque lundi)
Si on te demande de mettre en place ou d'exécuter la routine du lundi :
1. Lire `historique.md` pour ne pas répéter un sujet récent.
2. Produire la semaine suivante : environ 7 posts Instagram (réels + 2 carrousels) et 14 TikTok (2 par jour), avec les modèles de `modeles/` et les scripts de `scripts/` (rendu Playwright + ffmpeg, 1080×1920, 30 i/s ; carrousels 1080×1350).
3. Pousser les médias dans `medias/` et un nouveau `planning/programmation_AAAA-MM-JJ.json` au même format, vérifier qu'une URL raw répond 200.
4. Programmer en **brouillons** comme ci-dessus, mettre à jour `historique.md`, envoyer le récapitulatif.
5. Les vidéos avec voix ElevenLabs demandent que la fondatrice télécharge le MP3 elle-même : ne pas en prévoir sans lui demander.

## Règles de contenu (cavalière)
- Pas de sujet « vermifuge ».
- Maréchal : toutes les 5 à 6 semaines.
- Vaccins : tous les ans (compétitions nationales) ou tous les 6 mois (CSI). Vaccin pas à jour = pas de départ en concours.
- L'app organise, elle ne soigne pas : renvoyer vers le vétérinaire pour la santé. iPhone uniquement, gratuit pour 1 cheval, Premium 3,99 €/mois ou 39,99 €/an.
- Charte : fond #F6F4F0, principal #231B6B, accents #6C5FD6 et #B8B0F2, rouge #E5533D seulement pour les erreurs ; titres Fraunces, texte Inter. Cheval de démo : Floy De Tus.
- Ton : tutoiement, complice, autodérision de cavalière, pas de jargon marketing. Pas de faux avis ni de faux témoignages.
