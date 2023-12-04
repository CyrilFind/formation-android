# TP 0 - Introduction

## Mise en place

Avant le premier cours, vérifiez que votre poste de travail est opérationnel ([tuto](https://developer.android.com/courses/pathways/android-basics-kotlin-two)):

- Installez [Android Studio](https://developer.android.com/studio) ([tuto](https://developer.android.com/codelabs/basic-android-kotlin-training-install-android-studio?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-two%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-install-android-studio#0))
- Créez un projet vide (laissez l'api minimale proposée) et essayez de le lancer: ([tuto](https://developer.android.com/codelabs/basic-android-kotlin-training-first-template-project?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-two%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-first-template-project#0))
- Si vous avez un appareil Android physique et un cable qui fonctionne, passez le en mode développeur (en tapant 7 fois sur le numéro de build dans les paramètres) et prenez le avec vous en cours, ce sera plus simple. ([tuto](https://developer.android.com/codelabs/basic-android-kotlin-training-run-on-mobile-device?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-two%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-run-on-mobile-device#0))
- Sinon, créez un émulateur: choisissez un device avec le triangle du PlayStore puis une version d'OS Android (pour éviter des problèmes, ne choisissez pas la toute dernière, mais l'avant dernière par ex). Si vous êtes sous Windows, vous aurez peut être des paramètres BIOS à changer pour la virtualisation.

<aside class="positive">
N'hésitez pas à me contacter en avance si vous avez un soucis (les liens 'tuto' ne sont pas nécessaire normalement mais ils peuvent aider aussi)
</aside>

## Paramétrage

Prenez en main l'IDE: vous pouvez aller dans les paramètres (`File > Settings` ou `Android Studio > Preferences`) et personnalisez l'IDE, je vous conseille notamment ceci:

- Activez tout dans `Editor > Inlay Hints`
- Activez les imports automatiques: `Editor > General > Auto Import > Kotlin (en bas) > cocher les 2 cases`
- Personnalisez la coloration syntaxique dans `Settings > Editor > Color Scheme > ⚙ > Import Scheme` (ex: le plugin "Rainglow Color Schemes")
- Personnalisez les raccourcis clavier

## Android Studio

🚀 Aidez vous de l'IDE: Android Studio fait beaucoup de travail pour vous donc utilisez l'autocompletion et les raccourcis:

- `CTRL/CMD` + `click` pour voir les usages ou la définition d'un élément
- `Alt` + `Enter` pour des "💡 QuickFix" (suggestions de l'IDE)
- `Shift, Shift + "recherche"` pour tout le reste (rechercher une variable, fonction, classe, actions, options, ...)
- `CTRL/CMD + alt + L` pour ré-indenter correctement tout le code (ou la sélection)

## Google Codelabs

On va commencer en douceur en se basant sur les [Codelabs Google](https://developer.android.com/courses/android-basics-kotlin/course)

<aside class="negative">
Ces tutos sont "not maintained" parce qu'il s'agit de l'ancien système de vues, mais il faut aussi en apprendre les bases, on passera au nouveau ensuite.
</aside>

Tous ces tutos ne sont pas indispensable pour des presque-ingénieurs tels que vous alors on va en faire seulement quelques uns:

- 1e partie: [XML layouts](https://developer.android.com/codelabs/basic-android-kotlin-training-xml-layouts?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-unit-2-pathway-1%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-xml-layouts)
- 2e partie: [ViewBinding](https://developer.android.com/codelabs/basic-android-kotlin-training-tip-calculator?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-unit-2-pathway-1%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-tip-calculator)
<!-- - 3e partie: [RecyclerView](https://developer.android.com/codelabs/basic-android-kotlin-training-recyclerview-scrollable-list?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-unit-2-pathway-3%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-recyclerview-scrollable-list#0) -->

<aside class="negative">
⚠️ Ne perdez pas de temps sur les pages "Introduction", "Overview", ... des codelabs, ce sont juste des résumés de ce que vous allez faire, ni sur les dernières étapes (questions, exercices)
</aside>

## Kotlin Koans

Exercices pour prendre en main le langage: [try.kotl.in/koans](http://try.kotl.in/koans)

Si vous voulez aller plus loin sur Kotlin : [Kotlin Bootcamp](https://developer.android.com/courses/kotlin-bootcamp/overview)

## Projet

Pendant les prochains TP, vous allez créer un projet en binôme que vous compléterez au fil des TPs.

Par défaut c'est une simple Todo app, mais vous pouvez choisir un autre sujet qui vous intéresse plus, mais dans tous les cas il faudra que le résultat final respecte certaines specifications:

- Liste scrollable d'éléments (avec `RecyclerView`)
- Interaction avec une API distante (avec `Retrofit`, `kotlinXcoroutines` et `kotlinXserialization`)
- Afficher des images (avec `Coil`)
- Naviguer entre plusieurs écrans en échangeant des infos (`Intent`, Navigation Component, Activity Result)
- Respecter une architecture minimale (avec `ViewModel` et `Repository`)
- Demander une ou plusieurs permissions

Quelques idées d'applications:

- Affichage d'horaires de trains
- Client alternatif pour Twitch, Twitter, etc
- Traqueur de films, séries, jeux, etc
- Jeux à UI simple: Quiz, Memory, etc
- un chatbot spécialisé

Exemples d'années précédentes:

- Cémantix
- Reigns-like

Exemples d'API:

- <https://trakt.docs.apiary.io>
- <https://imgflip.com/api>

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