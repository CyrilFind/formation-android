# TP 0 - Introduction

## Mise en place

Avant le premier cours, vérifiez que votre poste de travail est opérationnel:

- Installez - **sur un disque où vous avez de la place** - la dernière version d'[Android Studio][android_studio_download],ou mettez le à jour si vous l'avez déjà
- Créez un projet vide (laissez l'api minimale proposée)
- Si vous avez un appareil Android physique et un cable qui fonctionne, passez le en mode développeur (en tapant 7 fois sur le numéro de build dans les paramètres) et prenez le avec vous en cours, ce sera plus simple.
- Sinon: Dans `Device Manager > Create virtual device` choisissez un device avec le triangle du PlayStore, puis une version d'OS Android récente.
- Essayez de le lancer le projet (en cliquant sur le triangle vert)

<aside class="positive">

N'hésitez pas à me contacter en avance si vous avez un soucis (vous pouvez aussi suivre des [tutos Google][android_studio_pathway])

Un problème courant est le manque d'espace notamment pour le SDK et l'émulateur ou la connexion de l'école qui ne permet pas toujours de télécharger les dépendances

Si vous êtes sous Windows, vous aurez peut être des paramètres BIOS à changer pour la virtualisation.
</aside>

## Paramétrage

Prenez en main l'IDE: vous pouvez aller dans les paramètres (`File > Settings` ou `Android Studio > Preferences`) et personnalisez l'IDE, je vous conseille notamment ceci:

- Activez tout dans `Editor > Inlay Hints`
- Activez les imports automatiques: `Editor > General > Auto Import > Kotlin (en bas) > cocher les 2 cases`
- Personnalisez la coloration syntaxique dans `Settings > Editor > Color Scheme` (vous pouvez utiliser ma config avec `⚙ > Import Scheme` et ce [fichier](./assets/Darculai.icls))
- Personnalisez les raccourcis clavier

## Android Studio

🚀 Aidez vous de l'IDE: Android Studio fait beaucoup de travail pour vous donc utilisez l'autocompletion et les raccourcis:

- `CTRL/CMD` + `click` pour voir les usages ou la définition d'un élément
- `Alt` + `Enter` pour des "💡 QuickFix" (suggestions de l'IDE)
- `Shift, Shift + "recherche"` pour tout le reste (variable, fonction, classe, actions, options, ...)
- `CTRL/CMD + alt + L` pour ré-indenter correctement tout le code (ou la sélection)
- Cliquez sur `Sync Now` (dans la barre bleue en haut)quand l'IDE vous le propose: ça arrive notamment quand on change des fichiers de configs comme les fichiers gradle par exemple pour ajouter des dépendances. Cela permet à l'IDE de fonctionner correctement.

## Kotlin

Pour prendre en main les bases du langage: [try.kotl.in/koans][koans]

Commencez par ces exercices:

- [Nullable types](https://play.kotlinlang.org/koans/Introduction/Nullable%20types/Task.kt)
- [String templates](https://play.kotlinlang.org/koans/Introduction/String%20templates/Task.kt)
- [Lambdas](https://play.kotlinlang.org/koans/Introduction/Lambdas/Task.kt)
- [Data classes](https://play.kotlinlang.org/koans/Classes/Data%20classes/Task.kt)
- [Smart casts](https://play.kotlinlang.org/koans/Classes/Smart%20casts/Task.kt)

Pour aller plus loin sur Kotlin : [Kotlin Bootcamp](https://developer.android.com/courses/kotlin-bootcamp/overview)

## Google Codelabs

On va commencer en douceur en se basant sur les [Codelabs Google](https://developer.android.com/courses/android-basics-compose/course)

Tous ces tutos ne sont pas indispensable pour des presque-ingénieurs tels que vous alors on va en faire seulement quelques uns:

- [Compose Texts][compose_text_codelab]
- [Compose Images][compose_images_codelab]
- [Compose Buttons][compose_buttons_codelab]
- [Constraint Layout][constraint_layout_codelab]

<aside class="negative">
⚠️ Ne perdez pas de temps sur les pages "Introduction", "Overview", etc... ni sur les dernières étapes: questions, exercices, etc...
</aside>

## Projet

Pendant les prochains TP, vous allez créer un projet en binôme que vous compléterez au fil des TPs.

Par défaut c'est une simple Todo app, mais vous pouvez choisir un autre sujet qui vous intéresse plus, mais dans tous les cas il faudra que le résultat final respecte certaines specifications:

- Liste scrollable d'éléments (dont une `RecyclerView`)
- Interaction avec une API distante (avec `Retrofit`, `kotlinx.serialization` et `kotlinx.coroutines`)
- Afficher des images local et distantes (avec `Coil`)
- Naviguer entre plusieurs écrans en échangeant des infos (`Intent`, Navigation Component, Activity Result)
- Respecter une architecture minimale (avec `ViewModel` et `Repository`)
- Demander une ou plusieurs permissions

Quelques idées d'applications:

- Affichage d'horaires de trains
- Client alternatif pour Twitch, Twitter, Bluesky, ...
- Traqueur de films, séries, jeux, etc
- Jeux à UI simple: Quiz, Memory, etc
- un chatbot spécialisé

Exemples d'années précédentes:

- Cémantix
- Reigns-like

Exemples d'API gratuites:

- <https://trakt.docs.apiary.io>
- <https://imgflip.com/api>

Si vous le souhaitez, on peut aussi essayer de faire du Kotlin Mutliplatform afin de pouvoir lancer votre app également sur iOS !

Au moment de setup le projet, demandez moi un coup de main, on utilisera [cet outil](https://kmp.jetbrains.com/)

<!--
Barème approximatif /10 :
- base /2
- TP features principales /3
- propreté et stabilité /2
- TP complets /3
- bonus (UI, sujet personnalisé)

-> ReadMe

soutenance?

-->

[android_studio_pathway]: https://developer.android.com/courses/pathways/android-basics-compose-unit-1-pathway-2
[android_studio_download]: https://developer.android.com/studio
[compose_text_codelab]: https://developer.android.com/codelabs/basic-android-kotlin-compose-text-composables
[compose_images_codelab]: https://developer.android.com/codelabs/basic-android-kotlin-compose-add-images
[compose_buttons_codelab]: https://developer.android.com/codelabs/basic-android-kotlin-compose-build-a-dice-roller-app
[koans]: http://try.kotl.in/koans
[constraint_layout_codelab]: https://developer.android.com/codelabs/constraint-layout
