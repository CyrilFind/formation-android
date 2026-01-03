# TP 4: Project perso

## À vous de jouer

<aside class="positive">

C'est le moment de commencer votre projet perso, inspirez vous de ce qu'on a fait jusqu'ici et demandez moi de vous aider !

</aside>

- Comme précédemment, commencez par créer encore une nouvelle Activity Compose et faites d'elle la "main" dans le Manifest.

<aside class="negative">

⚠️ Ne créez pas un nouveau projet, le but est que vous ayez un seul rendu à m'envoyer à la fin !

</aside>

- Refaites également un Scaffold avec un bouton dans une `TopAppBar` contenant un bouton qui retourne à `ComposeActivity`, un composant principal `MyApp()`, etc

## Liste et Internet

- Dans un 1er temps, vous allez de voir afficher une liste d'éléments depuis une API
- Commencez par tester votre API (avec `curl` par exemple)
- Vous pouvez récupérer quasiment toute la logique dans `Api`: Copiez collez le fichier et renommez selon votre Api (ex: FacebookApi)
- Dans la plupart des cas vous aurez juste à changer la `baseUrl()` et le `TOKEN`
- Si la méthode d'authentification est différente je pourrai vous aider à adapter

## Détails et Édition

- Créez une navigation avec `NavDisplay`
- Créez un nouvel écran de détails
- Dans celui ci, affichez des informations plus complètes sur vos éléments
- Faites en sorte de naviguer dans ce nouvel écran en cliquant sur un item dans la liste, en vous inspirant de ceci (en cas de conflit de nommage avec les écrans précédents, renommez les comme vous le souhaitez):

```kotlin
@Serializable
data object ListNavScreen : NavKey
@Serializable
data class DetailNavScreen(val id: String) : NavKey
```

<aside class="positive">

🧑‍🏫 Dans cet exemple, contrairement à précédemment, on passe un ID au lieu de l'objet entier.

C'est une meilleure pratique, un peu commen en web quand vous cliquez sur un profil le lien est `.../profile/1234`, il ne contient pas toutes les infos à afficher.

Donc ici pour gérer votre écran détail vous allez faire un autre ViewModel, un autre call réseau, etc...

</aside>

## Images

Faire en sorte d'afficher des images en utilisant [Coil](https://coil-kt.github.io/coil/), dans la liste et/ou dans le détail si possible.

Si ça ne colle pas du tout à votre projet, ajoutez en au moins quelques unes pour habiller votre interface.

## Login

Si votre projet le permet, ajoutez un parcours de login à votre app pour remplacer le TOKEN en dur dans le code si c'est possible (ou autre méthode d'authentification)

## Architecture

Respectez une architecture minimale:

- Écrans Compose: affichage seulement
- ViewModels: map les données en états à afficher et remonte les events
- Repository: requête les webservice et/ou bases de données et map les données

[Doc](https://developer.android.com/topic/architecture)

## Injection de Dépendance

Implémentez de l'injection de dépendances avec [Koin](https://insert-koin.io/)

[Doc](https://developer.android.com/training/dependency-injection)

## Tests

Implémentez des tests unitaires:

[Doc](https://developer.android.com/training/testing/local-tests)

## Permissions

Selon votre projet, vous pourriez avoir besoin d'accéder à certaines ressources nécessitant des permissions, notamment des "Runtime Permission"

[Doc](https://developer.android.com/guide/topics/permissions)

## Caméra

[Doc](https://developer.android.com/media/camera/get-started-with-camera)

## Location

[Doc](https://developer.android.com/develop/sensors-and-location/location)

## Sensors

[Doc](https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview)

## Stockage

Selon votre projet (si l'API permet seulement de GET par exemple), aidez vous de la documentation pour choisir une solution de stockage de données locale (`DataStore`, `Room`, etc) adaptée.

[Doc](https://developer.android.com/training/data-storage)

## Background

Selon votre projet, aidez vous de la documentation pour choisir une solution de travail en arrière-plan.
Par exemple pour envoyer des notifications, des rappels avec une alarme, télécharger des données, etc

[Documentation](https://developer.android.com/develop/background-work/background-tasks)

## Audio/Video

[Documentation](https://developer.android.com/media/audio-and-video)

## A11y

Gérer l'accessibilité (via `TalkBack`)

[Doc](https://developer.android.com/guide/topics/ui/accessibility/apps)

## Graphs

[Lib](https://github.com/patrykandpatrick/vico)

## Autres

Pour toute autre sujets, voyez avec moi !

[Codelabs](https://developer.android.com/get-started/codelabs)

## Rendu et Barême approximatif

- TP1: liste en RecyclerView - ajout, suppression, édition, etc / 3
- TP2: liste en Jetpack Compose - ajout, suppression, édition, etc / 3
- TP3: connexion à une API distante, afficher user, ViewModel, etc / 2
- TP4: projet perso complet / 6
- Qualité globale du code et architecture / 3
- UI correcte: un minimum "joli" / 1
- UX correcte: utilisable, navigation facile / 2
- bonus si vous allez au bout de chaque TP / ?
- malus si je dois demander un accès / -1
- malus si le projet n'est pas bien commité / -1
- malus si je dois bricoler pour que ça marche / -1

Pas de soutenance mais une capture video de présentation rapide de chacune de vos fonctionnalités en quelques minutes à mettre sur le repo git.
