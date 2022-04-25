# TP 2 - Actions & Intents

## Objectif

implémenter des actions sur nos tâches, en naviguant entre des `Activity` et partager des infos entre elle ou dans une autre application avec des `Intent`.

## Suppression d'une tache

Dans le layout de vos item, ajouter un `ImageButton` qui servira à supprimer la tâche associée. Vous pouvez utiliser par exemple l'icône `@android:drawable/ic_menu_delete`

<aside class="positive">

**Rappel:** Une [lambda](https://kotlinlang.org/docs/reference/lambdas.html) est un type de variable qui contient un bloc de code pouvant prendre des arguments et retourner un résultat, c'est donc une fonction que l'on utilise comme une variable !

</aside>

Aidez vous des lignes de code plus bas pour réaliser un "Click Listener" à l'aide d'une lambda en suivant ces étapes:

- Dans l'adapter, ajouter une propriété `onClickDelete` de type lambda qui prends en arguments une `Task` et ne renvoie rien: `(Task) -> Unit` et l'initier à `{}` (elle ne fait rien par défaut)
- Utilisez cette lambda dans le `onClickListener` du bouton supprimer
- Dans le fragment, accéder à `onClickDelete` depuis l'adapter et implémentez là: donnez lui comme valeur une lambda qui va supprimer la tache passée en argument de la liste

```kotlin
// Déclaration de la variable lambda dans l'adapter:
var onClickDelete: (Task) -> Unit = {}

// Utilisation de la lambda dans le ViewHolder:
onClickDelete(task)

// "implémentation" de la lambda dans le fragment:
myAdapter.onClickDelete = { task ->
    // Supprimer la tâche
}
```

## Création de FormActivity

- Créez un package `form` dans votre package principal
- Créez y avec l'IDE une nouvelle ACtivity: `FormActivity` (`Clic droit sur le package > New > Activity > Empty Activity`)
- Dans le layout correspondant, créez 2 `EditText`, pour le titre et la description et un bouton pour valider

<aside class="negative">

⚠️ Si vous créez l'Activity "à la main", n'oubliez pas de la déclarer dans le manifest !

</aside>

## Ajout de tâche complet: Launcher

<aside class="positive">

Afin de naviguer vers notre nouvelle Activity, nous allons utiliser un [Intent explicite](https://developer.android.com/guide/components/intents-filters#Types), et afin de récupérer un résultat de celle ci, nous allons utiliser un ["launcher"](https://developer.android.com/training/basics/intents/result#register) avec le "contrat" générique[StartActivityForResult](https://developer.android.com/reference/androidx/activity/result/contract/ActivityResultContracts.StartActivityForResult)

**remarque**: Auparavant, il fallait utiliser `startActivityForResult(intent)` et `override fun onActivityResult(...)` avec un request code, etc.

</aside>

- Créez un "launcher" en propriété de la classe `TaskListFragment` qui permettra de lancer votre nouvelle activité et d'utiliser son résultat:

```kotlin
val createTask = registerForActivityResult(StartActivityForResult()) { result ->
  // ici on récupérera le résultat pour le traiter
}
```

- Changer l'action du bouton d'ajout pour qu'il ouvre cette activité avec un `Intent`

```kotlin
val intent = Intent(context, FormActivity::class.java)
createTask.launch(intent)
```

## Ajout de tâche complet: FormActivity

Dans le `onCreate` de la nouvelle activité, récupérer une référence au bouton de validation (comme précédemment avec le bouton d'ajout par ex) puis setter son `onClickListener` pour qu'il crée une tâche:

```kotlin
// Instanciation d'un nouvel objet [Task]
val newTask = Task(id = UUID.randomUUID().toString(), title = "New Task !")
```

<aside class="positive">

Toute Activity a une propriété `intent` déjà définie: ici il aura la valeur que l'on a passée à `createTask`, on va utiliser ce même intent pour retourner un résultat

</aside>

- Ajouter `newTask` dans `intent`: `intent.putExtra("task", newTask)`: ça ne compilera pas car `Task` ne fait pas partie des types de base autorisés dans un intent !
- L'un de ces types est `Serializable`: Faites donc hériter `Task` de `java.io.Serializable`, comme c'est une `data class`, il n'y a rien à implémenter !
- utilisez `setResult(RESULT_OK, intent)` pour signifier que l'action s'est bien passée (idéalement, on aurait aussi géré des cas d'erreur)
- utilisez `finish()` pour quitter cette activité, et donc retourner à l'écran précédent

## Ajout de tâche complet: Résultat

Dans la lambda de retour de `createTask` récupérer cette task et l'ajouter à la liste:

```kotlin
val task = result.data?.getSerializableExtra("task") as? Task
```

- Faites en sorte que la nouvelle tache s'affiche dans la liste directement
- Maintenant, récupérez les valeurs entrées pour les donner à la création de votre tâche (vous devrez faire un `toString()` car les `EditText` ne renvoient pas directement des `String`)

## Édition d'une tâche

Inspirez vous de ce que vous avez fait pour le bouton "supprimer" et le bouton "ajouter" pour créer un bouton "éditer" permettant de modifier chaque tâche en ouvrant l'activité `FormActivity` pré-remplie avec les informations de la tâche en question:

- Créez un autre launcher dans le fragment
- Créez une autre lambda dans l'adapter
- Utilisez dans celle ci `putExtra` pour transmettre la `Task` à éditer (depuis `TaskListFragment` cette fois)
- Récupérez la `Task` dans le `onCreate` de `FormActivity` avec `getSerializableExtra` comme précédemment (avec `intent` à la place de `result.data`)
- La `Task` récupérée est `nullable`: c'est utile car elle sera `null` quand vous êtes dans le cas "Ajout", et sinon, elle aura une vraie valeur car vous êtes dans le cas "Édition"
- utilisez la pour préremplir les `EditText` avec `setText()` (quand la task est `null`, ça remplira avec `""` donc pas de soucis)
- Utilisez l'opérateur `?:` pour réutiliser l'id précédent dans le cas de l'édition, et en créer un sinon:

```kotlin
val id = task?.id ?: UUID.randomUUID().toString()
```

- Au retour dans votre launcher, mettez à jour la liste: `taskList = taskList.map { if (it.id == newTask.id) newTask else it }`
- Vérifier que les infos éditées s'affichent bien à notre retour sur l'activité principale.

## Interface et délégation

Une façon plus classique de gérer les clicks d'un item est de définir une interface que l'on implémentera dans l'Activity/Fragment.
Mettez à jour votre code pour utiliser cette méthode:

```kotlin
interface TaskListListener {
  fun onClickDelete(task: Task)
  fun onClickEdit(task: Task)
}

class TaskListAdapter(val listener: TaskListListener) : ... {
  // use: listener.onClickDelete(task)
}

class TaskListFragment : Fragment {
  val adapterListener : TaskListListener = object : TaskListListener {
    override onClickDelete(task: Task) {...}
    override onClickEdit(task: Task) {...}
  }
  val adapter = TaskListAdapter(adapterListener)
}
```

## Partager

- En modifiant `AndroidManifest.xml`, ajouter la possibilité de partager du texte **depuis les autres applications** (par ex en surlignant un texte dans un navigateur puis en cliquant sur "partager") et ouvrir le formulaire de création de tâche avec une description pré-remplie ([Documentation][1])
- En utilisant un `Intent` **implicite**, ajouter la possibilité de partager du texte **vers les autres applications** (avec un `OnLongClickListener` sur les tâches par ex ou bien avec un bouton dans la vue formulaire) ([Documentation][2])

## Changements de configuration

Que se passe-t-il pour votre liste si vous tournez votre téléphone pour passer en mode paysage ? 🤔

- Une façon de régler ce soucis est d'overrider la méthode `onSaveInstanceState`
- Il faudra utiliser `putSerializable` (un peu comme précédemment avec `putExtra`) pour sauvegarder la liste
- Puis pour récupérer cette liste, la méthode `getSerializable` dans `onCreateView` ou `onViewCreated`, sur le paramètre `savedInstanceState`

[1]: https://developer.android.com/training/sharing/receive
[2]: https://developer.android.com/training/sharing/send
