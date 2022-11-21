# TP 0 - Introduction

## Mise en place

Avant le premier cours, vérifiez que votre poste de travail est opérationnel ([tuto](https://developer.android.com/courses/pathways/android-basics-kotlin-two)):

- Installez Android Studio ([tuto](https://developer.android.com/codelabs/basic-android-kotlin-training-install-android-studio?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-two%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-install-android-studio#0))
- Créez un projet vide (laissez l'api minimale proposée) et essayez de le lancer: ([tuto](https://developer.android.com/codelabs/basic-android-kotlin-training-first-template-project?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-two%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-first-template-project#0))
- Si vous avez un appareil Android physique et un cable qui fonctionne, passez le en mode développeur (en tapant 7 fois sur le numéro de build dans les paramètres) et prenez le avec vous en cours, ce sera beaucoup plus simple. ([tuto](https://developer.android.com/codelabs/basic-android-kotlin-training-run-on-mobile-device?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-two%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-run-on-mobile-device#0))
- Sinon, créez un émulateur: choisissez un device avec le triangle de google play services puis une version d'OS Android (pour éviter des problèmes, ne choisissez pas la toute dernière, mais l'avant dernière par ex). Si vous êtes sous Windows, vous aurez peut être des paramètres BIOS à changer pour la virtualisation.

<aside class="positive">
N'hésitez pas à me contacter en avance si vous avez un soucis
</aside>

## Paramètrage

Prenez en main l'IDE: vous pouvez aller dans les paramètres (`File > Settings` ou `Android Studio > Preferences`) et personnalisez l'IDE, je vous conseille notamment ceci:

- Activer tous dans `Editor > Inlay Hints`
- Activez les imports automatiques: `Editor > General > Auto Import > Kotlin > cocher "Add unambiguous import on the fly" et "Optimize imports on the fly..."`
- Personnalisez la coloration syntaxique (ex: le plugin "Rainglow Color Schemes", mon thème [Darculai](https://raw.githubusercontent.com/CyrilFind/intellij-settings-repository/master/colors/Darculai%20_cyrilfind_.icls) dans `Settings > Editor > Color Scheme > ⚙ > Import Scheme`)
- Personnalisez les raccourcis clavier (ex: [mon setup](https://raw.githubusercontent.com/CyrilFind/intellij-settings-repository/master/keymaps/cyrilfind.xml))

## Kotlin Koans

Petits exercices pour prendre en main le langage: [try.kotl.in/koans](http://try.kotl.in/koans)

Si vous voulez aller plus loin sur Kotlin : [Kotlin Bootcamp](https://developer.android.com/courses/kotlin-bootcamp/overview)

<aside class="negative">
⚠️ Ne restez pas trop longtemps à cette étape, si on est déjà passé à la suivante, faites de même!
</aside>

## Google Codelabs

Pour commencer, on va se baser sur les [Codelabs Google](https://developer.android.com/courses/android-basics-kotlin/course) mais tout n'est pas indispensable:

- Commencez directement par celui ci: [Create XML layouts for Android](https://developer.android.com/codelabs/basic-android-kotlin-training-xml-layouts?continue=https%3A%2F%2Fdeveloper.android.com%2Fcourses%2Fpathways%2Fandroid-basics-kotlin-unit-2-pathway-1%23codelab-https%3A%2F%2Fdeveloper.android.com%2Fcodelabs%2Fbasic-android-kotlin-training-xml-layouts#0)
- Puis continuer par les codelabs suivants: [Part 2](https://developer.android.com/courses/pathways/android-basics-kotlin-unit-2-pathway-2)

<aside class="negative">
⚠️ Ne perdez pas de temps sur les pages "Introduction", "Overview", ... des codelabs, ce sont juste des résumés de ce que vous allez faire.
</aside>

## Projet

Pendant les prochains TP, vous allez créer un projet en binôme que vous complèterez au fur à mesure.

C'est une simple Todo app, mais vous pouvez choisir un autre sujet qui vous intéresse plus, mais dans tous les cas il faudra que le résultat final respecte certaines specifications:

- Une liste scrollable d'éléments (avec `RecyclerView`)
- Intéragis avec une API distante (avec `Retrofit`, `kotlinXcoroutines` et `kotlinXserialization`)
- Afficher des images (avec `Coil`)
- Naviguer entre plusieurs écrans en échangeant des infos (`Intent`, Navigation Component, Activity Result)
- Respecter une architecture minimale (avec `ViewModel`)
- Demander une ou plusieurs permissions

Quelques idées d'applications:

- Affichage d'horaires de trains
- Client Twitch, Twitter, etc
- Traqueur de films, séries, jeux, etc
- Jeux à UI simple: Quiz, Memory, etc