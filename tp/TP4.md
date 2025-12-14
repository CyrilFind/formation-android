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

Selon votre projet, ajoutez un parcours de login à votre app pour remplacer le TOKEN en dur dans le code si c'est possible (ou autre méthode d'authentification)
