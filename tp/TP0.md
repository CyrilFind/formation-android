# TP 0 - Introduction

## Mise en place

Avant le premier cours, vérifiez que votre poste de travail est opérationnel:

- Installez - **sur un disque où vous avez de la place** - la dernière version d'[Android Studio][android_studio_download], ou mettez le à jour si vous l'avez déjà
- Créez un projet vide (laissez l'api minimale proposée)
- Si vous avez un appareil Android physique et un cable qui fonctionne, passez le en mode développeur (en tapant 7 fois sur le numéro de build dans les paramètres) et prenez le avec vous en cours, ce sera plus simple.
- Sinon: Dans `Device Manager > Create virtual device` choisissez un device avec le triangle du PlayStore, puis une version d'OS Android récente.
- Essayez de le lancer le projet (en cliquant sur le triangle vert)

<aside class="positive">

N'hésitez pas à me contacter en avance si vous avez un soucis (vous pouvez aussi suivre des [tutos Google][android_studio_pathway])

Problème courants:

- manque d'espace pour le SDK, l'émulateur: installez sur un disque secondaire si il y a + de place
- la connexion de l'école qui ne permet pas toujours de télécharger les dépendances: passez en partage de connexion ou sur un autre réseau
- problèmes de permissions (ex `Failed to create jwk directory`): lancez Android Studio en mode Administrateur
- problèmes divers d'execution et de performances de l'émulateur: vous pouvez tenter des conseils [ici](https://developer.android.com/studio/run/emulator-acceleration)

D'une manière générale, si vous avez un device physique et un cable, ça vous évitera pas mal de soucis.

</aside>

## Paramétrage

Prenez en main l'IDE: vous pouvez aller dans les paramètres (`File > Settings` ou `Android Studio > Preferences`) et personnalisez l'IDE, je vous conseille notamment ceci:

- Activez tout dans `Editor > Inlay Hints`
- Activez les imports automatiques: `Editor > General > Auto Import > Kotlin (en bas) > cocher les 2 cases`
- Personnalisez la coloration syntaxique dans `Settings > Editor > Color Scheme` (vous pouvez utiliser ma config avec `⚙ > Import Scheme` et ce [fichier](../../assets/Darculai.icls))
- Personnalisez les raccourcis clavier

## Android Studio

🚀 Aidez vous de l'IDE: Android Studio fait beaucoup de travail pour vous donc utilisez l'autocompletion et les raccourcis:

- `CTRL/CMD` + `click` pour voir les usages ou la définition d'un élément
- `Alt` + `Enter` pour des "💡 QuickFix" (suggestions de l'IDE)
- `Shift, Shift + "recherche"` pour tout le reste (variable, fonction, classe, actions, options, ...)
- `CTRL/CMD + alt + L` pour ré-indenter correctement tout le code (ou la sélection)
- Cliquez sur `Sync Now` (dans la barre bleue en haut)quand l'IDE vous le propose: ça arrive notamment quand on change des fichiers de configs comme les fichiers gradle par exemple pour ajouter des dépendances. Cela permet à l'IDE de fonctionner correctement.

## Kotlin Basics

Pour prendre en main les bases du langage:

- [Nullable types](https://play.kotlinlang.org/koans/Introduction/Nullable%20types/Task.kt)
- [String templates](https://play.kotlinlang.org/koans/Introduction/String%20templates/Task.kt)
- [Lambdas](https://play.kotlinlang.org/koans/Introduction/Lambdas/Task.kt)
- [Data classes](https://play.kotlinlang.org/koans/Classes/Data%20classes/Task.kt)
- [Smart casts](https://play.kotlinlang.org/koans/Classes/Smart%20casts/Task.kt)

Pour aller plus loin sur Kotlin : [Kotlin Bootcamp](https://developer.android.com/courses/kotlin-bootcamp/overview)

## Jetpack Compose Basics

- [Compose Texts][compose_text_codelab]
- [Compose Images][compose_images_codelab]
- [Compose Buttons][compose_buttons_codelab]
- [Constraint Layout][constraint_layout_codelab]

<aside class="negative">
⚠️ Ne perdez pas de temps sur les pages "Introduction", "Overview", etc... ni sur les dernières étapes: questions, exercices, etc...
</aside>

Pour continuer voir [les autres codelabs Google](https://developer.android.com/courses/android-basics-compose/course)

## Projet

Pendant les prochains TP, vous allez créer un projet en binôme que vous compléterez au fil des TPs.

Par défaut c'est une simple Todo app, mais vous pouvez choisir un autre sujet qui vous intéresse plus, mais dans tous les cas il faudra que le résultat final utilise les briques de base suivantes:

- Avoir une UI correcte en Jetpack compose
- Naviguer entre plusieurs écrans: Liste/Détail a minima
- Interaction avec une API distante (avec `Retrofit`, `kotlinx.serialization` et `kotlinx.coroutines`)
- Afficher des images locales et distantes avec `Coil`
- Respecter une architecture minimale (avec `ViewModel` et `Repository`)
- écrire un minimum de tests unitaires

Et selon le sujet choisi, vous pourrez aussi implémenter:

- Une mécanique de login
- Demander une ou plusieurs permissions
- Stocker des données localement (avec `DataStore` ou `Room`) si l'API permet seulement de GET par exemple
- Gérer des tâches en arrière plan (avec `WorkManager`)
- Gérer l'accessibilité (via `TalkBack`)
- ...

Quelques idées d'applications:

- Affichage d'horaires de trains
- Client alternatif pour Twitch, Twitter, Bluesky, ...
- Traqueur de films, séries, jeux, etc
- Jeux à UI simple: Quiz, Memory, Wordle, Food Guessr, etc

Si vous avex un mac et/ou un iPhone (ou juste si ça vous intéresse) on fera du Kotlin Mutliplatform afin de pouvoir lancer votre app également sur iOS !

Exemples d'années précédentes:

- Cémantix
- Reigns-like
- Jukebox Spotify

Exemples d'API gratuites:

- <https://trakt.docs.apiary.io>
- <https://imgflip.com/api>
- <https://developer.themoviedb.org/v4/reference/>
- <https://dev.splitwise.com/>
- <https://developer.atlassian.com/cloud/trello/rest/>
- <https://docs.github.com/en/rest>
- <https://www.file.io/developers>
- <https://developers.google.com/books/docs/v1/reference>
- <https://spoonacular.com/food-api/docs>
- <https://openfoodfacts.github.io/openfoodfacts-server/api/ref-v3>

Moins permissives (pas de POST par ex):

- <https://pokeapi.co/docs/v2>
- <https://lyricsovh.docs.apiary.io>
- <http://numbersapi.com/#random/trivia>
- <https://openweathermap.org/api>
- <https://api.nasa.gov/>
- <https://www.thecocktaildb.com>
- <https://api.watchmode.com/docs>
- autres: <https://rapidapi.com/collection/list-of-free-apis>

[android_studio_pathway]: https://developer.android.com/courses/pathways/android-basics-compose-unit-1-pathway-2
[android_studio_download]: https://developer.android.com/studio
[compose_text_codelab]: https://developer.android.com/codelabs/basic-android-kotlin-compose-text-composables
[compose_images_codelab]: https://developer.android.com/codelabs/basic-android-kotlin-compose-add-images
[compose_buttons_codelab]: https://developer.android.com/codelabs/basic-android-kotlin-compose-build-a-dice-roller-app
[constraint_layout_codelab]: https://developer.android.com/codelabs/constraint-layout
