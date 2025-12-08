# TP 0 - Introduction

## Mise en place

Avant le premier cours, vérifiez que votre poste de travail est opérationnel:

- Installez - **sur un disque où vous avez de la place** - la dernière version d'[Android Studio](https://developer.android.com/studio), ou mettez le à jour si vous l'avez déjà
- Créez un projet vide (laissez l'api minimale proposée)
- Si vous avez un appareil Android physique et un cable qui fonctionne, passez le en mode développeur (en tapant 7 fois sur le numéro de build dans les paramètres) et prenez le avec vous en cours, ce sera plus simple.
- Sinon: Dans `Device Manager > Create virtual device` choisissez un device avec le triangle du PlayStore, puis une version d'OS Android récente.
- Essayez de le lancer le projet (en cliquant sur le triangle vert)

<aside class="positive">

N'hésitez pas à me contacter en avance si vous avez un soucis

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
- Personnalisez les raccourcis clavier: par ex "comment block" et "rename" ne sont pas très pratiques par défaut surtout en clavier azerty

## Android Studio

🚀 Aidez vous de l'IDE: Android Studio fait beaucoup de travail pour vous donc utilisez l'autocompletion et les raccourcis:

- `CTRL/CMD` + `click` pour voir les usages ou la définition d'un élément
- `Alt` + `Enter` pour des "💡 QuickFix" (suggestions de l'IDE)
- Clic droit pour plus d'actions: notamment "Refactor" qui contient pas mal de fonctions pratiques comme par exemple "rename" qui va renommer partout où l'élément est utilisé (il y a parfois des raccourcis existant ou alors vous pouvez en définir)
- `Shift, Shift + "recherche"` pour tout le reste (variable, fonction, classe, actions, options, ...)
- `CTRL/CMD + alt + L` pour ré-indenter correctement tout le code (ou la sélection)
- Cliquez sur `Sync Now` (dans la barre bleue en haut)quand l'IDE vous le propose: ça arrive notamment quand on change des fichiers de configs comme les fichiers gradle par exemple pour ajouter des dépendances. Cela permet à l'IDE de fonctionner correctement.

## Kotlin Basics

<aside class="positive">
🧑‍🏫 Rappels de vocabulaire:

```kotlin
val text: String = "hello"

val user: User? = null

class MutableList<T> : List<T> {
  // ...
  val count: String
  override fun add(element: E): Boolean
 }
```

- `text` est une **variable** de **type** `String` qui est un type **Primitive**
- `user` est une **variable** de **Class** `User?` qui est une classe **nullable** qui contient soit une **instance* de `User` soit `null`
- `Array<T>` est une **Class** qui prend un **type parameter** (ou **Generic**) et qui hérite de `List<T>`, comme `List<T>` est une **interface** on dit que `Array<T>` **implémente** `List<T>`
- `count` est une variable définie dans une **classe**: on dit que c'est une **propriété**
- `add` est une **fonction** qui **surcharge** une **fonction** ayant la même **signature** dans une des ses **classes mère**, comme elle est définie dans une **classe**, on dit que c'est une **méthode**

</aside>

Pour prendre en main les bases du langage, avec qq indices:

- [Nullable types](https://play.kotlinlang.org/koans/Introduction/Nullable%20types/Task.kt)

```kotlin
  // on peut "chaîner" les appels nullable avec `?.`:
  val email = client?.personalInfo?.email
```

- [String templates](https://play.kotlinlang.org/koans/Introduction/String%20templates/Task.kt)

```kotlin
 // pour "interpoler" une variable dans une string on utilise '$'
 fun getPattern(): String = """<pattern qui match 2 digits> $month <pattern qui match 4 digits>"""
```

- [Lambdas](https://play.kotlinlang.org/koans/Introduction/Lambdas/Task.kt)

```kotlin
val isEven = number % 2 == 0 // check division par 2
val lambdaWithExplicitParam = { explicitParam -> explicitParam == 42 }
val lambdaWithImplicitParam = { it == 42 }
```

- [Data classes](https://play.kotlinlang.org/koans/Classes/Data%20classes/Task.kt)

```kotlin
data class Person(
  val ...
  val ...
)
```

Pour aller plus loin sur Kotlin : [Kotlin Bootcamp](https://developer.android.com/courses/kotlin-bootcamp/overview)

## Jetpack Compose Basics

[Codelab: Jetpack Compose Basics](https://developer.android.com/codelabs/jetpack-compose-basics)

Pour continuer voir [les autres codelabs Google](https://developer.android.com/get-started/codelabs)

## Projet

Pendant les prochains TP, vous allez créer un projet en binôme que vous compléterez au fil des TPs.

On prends comme base une simple Todo app, mais vous choisirez ensuite un autre sujet que l'on intégrera dans le même projet pour simplifier le rendu. L'objectif est d'utiliser les briques de base suivantes:

- Avoir une UI correcte en Jetpack compose
- Naviguer entre plusieurs écrans: Liste/Détail a minima avec `Navigation3`
- Interaction avec une API distante (avec `Retrofit`, `kotlinx.serialization` et `kotlinx.coroutines`)
- Afficher des images locales et/ou distantes avec `Coil`
- Respecter une architecture minimale (`ViewModel`, `Repository`)
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

Ne perdez pas de temps et passez au TP1 !