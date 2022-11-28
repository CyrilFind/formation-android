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

## Compose: DetailActivity

<aside class="positive">
Cet écran étant assez simple, on va en profiter pour s'initer à Jetpack Compose, qui remplace le système XML utilisé jusqu'ici
</aside>

- Créez un package `detail` dans votre package principal
- Créez-y avec l'IDE une nouvelle Activity: `DetailActivity`: `Clic droit sur le package > New > Activity > Gallery... > Empty Compose Activity`
- L'IDE devrait automatiquement compléter `app/build.gradle` pour configurer Compose (buildFeatures, dependencies, etc) et l'ajouter au `AndroidManifest.xml`

<aside class="positive">

Afin de naviguer vers notre nouvelle Activity, nous allons utiliser un [Intent explicite](https://developer.android.com/guide/components/intents-filters#Types):

```kotlin
val intent = Intent(context, DetailActivity::class.java)
```
</aside>

- Faire en sorte de lancer la nouvelle Activity depuis le bouton + de la première activity

```kotlin
startActivity(intent)
```

- Renommez `Greeting` en `Detail` et `GreetingPreview` en `DetailPreview` et supprimez l'argument `name`

<aside class="positive">
Compose étant assez récent, ça ne marche pas toujours parfaitement, mais en théorie, si vous affichez le volet de Preview ("Split"), il affiche ce qui est dans `DetailPreview` sans avoir à relancer l'app à chaque fois
</aside>

- Changez le texte affiché dans le component `Text(...)` par un titre: `"Task Detail"`
- Ajoutez lui un `style` : `MaterialTheme.typography.h1`
- Ajoutez deux autres `Text()` avec comme contenu `"title"` et `"description"`
- Mettez les 3 `Text` dans une `Column {}`: c'est l'équivalent d'un `LinearLayout` vertical
- Ajoutez un `modifier` à votre `Column` pour ajouter un padding de `16.dp`
- Ajoutez un `verticalArrangement` à votre `Column` pour espacer ses enfants de `16.dp` (`Arrangement.spacedBy(...)`)
- Ajoutez un `Button` de validation dans la `Column`
- Personalisez un peu l'UI si vous le souhaitez
- Vérifiez que vous naviguez bien vers l'écran en cliquant sur + et qu'il s'affiche correctement

## Ajout de tâche complet: Launcher

<aside class="positive">

Afin de récupérer un résultat de cette nouvelle Activity, nous allons utiliser un ["launcher"](https://developer.android.com/training/basics/intents/result#register) avec le "contrat" générique[StartActivityForResult](https://developer.android.com/reference/androidx/activity/result/contract/ActivityResultContracts.StartActivityForResult)

**remarque**: Auparavant, il fallait utiliser `startActivityForResult(intent)` et `override fun onActivityResult(...)` avec un request code, etc.

</aside>

- Créez un "launcher" en propriété de la classe `TaskListFragment` qui permettra de lancer votre nouvelle activité et d'utiliser son résultat:

```kotlin
val createTask = registerForActivityResult(StartActivityForResult()) { result ->
  // dans cette callback on récupèrera la task et on l'ajoutera à la liste
}
```

- Remplacez l'action du bouton d'ajout pour qu'il ouvre cette activité avec un `Intent`

```kotlin
createTask.launch(intent)
```

## Ajout de tâche complet: DetailActivity

- Dans votre composant `Detail`, ajoutez un paramètre `onValidate: (Task) -> Unit` et appelez cette lambda dans le `onClick` de votre bouton de validation, en passant une nouvelle task:

```kotlin
val newTask = Task(id = UUID.randomUUID().toString(), title = "New Task !")
```

- Dans `onCreate`, `Detail` va donc maintenant nécessiter une lambda `onValidate`, que nous allons définir et utiliser:


<aside class="positive">

Toute Activity a une propriété `intent` déjà définie: ici il aura la valeur que l'on a passée à `createTask`, on va utiliser ce même intent pour retourner un résultat

</aside>

<!-- - Changez le contenu de vos 2 `Text` pour qu'ils affichent le `title` et la `description` de votre `Task` (la description sera vide pour l'instant) -->

- Ajouter `newTask` dans `intent`: `intent.putExtra("task", newTask)`: ça ne compilera pas car `Task` ne fait pas partie des types de base autorisés dans un intent !
- L'un de ces types est `Serializable`: Faites donc hériter `Task` de `java.io.Serializable`, comme c'est une `data class`, il n'y a rien à implémenter !
- utilisez `setResult(RESULT_OK, intent)` pour signifier que l'action s'est bien passée (idéalement, on aurait aussi géré des cas d'erreur)
- utilisez `finish()` pour quitter cette activité, et donc retourner à l'écran précédent

## Ajout de tâche complet: Résultat

- Dans la lambda de retour de `createTask` récupérer cette task:

```kotlin
val task = result.data?.getSerializableExtra("task") as Task?
```

- et ajoutez la à la liste, comme vous le faisiez avec le bouton d'ajout précédemment

<aside class="negative">

La syntaxe `as Task` permet de **"caster"** un objet récupéré en tant que `Task`: c'est à dire qu'on force l'objet à être considéré de type `Task`, qui est (depuis l'étape précédente) un sous-type de `Serializable` (retourné par `getSerializableExtra`)

ici on utilise `as Task?` (on pourrait utiliser `as? Task`) pour récupérer un **nullable** et éviter d'avoir une exception si le cast ne fonctionne pas en retournant `null` à la place

</aside>

- Faites en sorte que la nouvelle tache s'affiche dans la liste directement

<aside class="negative">
Pour l'instant notre Task est créée avec des données "en dur", on va changer ça et récupérer les valeurs entrées par l'utilisateur
</aside>

- Dans `DetailActivity`, changez les `Text` en `OutlinedTextField`, on va mettre à jour dynamiquement la Task affichée:

<aside class="positive">
Une fonction `@Composable` peut être *recomposée* (en gros: ré-exécutée) à tout moment donc on ne peut pas utiliser de variables simples car elles seraient remises à leur valeur de départ, on utilise donc `remember`:

```kotlin
var task by remember { mutableStateOf(Task(...)) } // faire les imports suggérés par l'IDE
```

Notez qu'on utilise également un `mutableStateOf` avec `by` qui permet à Compose de réagir automatiquement aux changements de valeurs mais pour cela vous devrez changer l'instance de task à chaque fois, on va utiliser `copy()` défini automatiquement pour les `data class` pour simplifier ça: `task = task.copy(title = "new title")`
</aside>

## Édition d'une tâche

Inspirez vous de ce que vous avez fait pour le bouton "supprimer" et le bouton "ajouter" pour créer un bouton "éditer" permettant de modifier chaque tâche en ouvrant l'activité `DetailActivity` pré-remplie avec les informations de la tâche en question:

- Créez un autre launcher dans le fragment
- Créez une autre lambda dans l'adapter
- Utilisez dans celle ci `putExtra` pour transmettre la `Task` à éditer (depuis `TaskListFragment` cette fois)
- Récupérez la `Task` dans le `onCreate` de `DetailActivity` avec `getSerializableExtra` comme précédemment (avec `intent` à la place de `result.data`)
- La `Task` récupérée est `nullable`: c'est utile car elle sera `null` quand vous êtes dans le cas "Ajout", et sinon, elle aura une vraie valeur car vous êtes dans le cas "Édition"
- utilisez la pour préremplir les `OutlinedTextField
- Utilisez l'opérateur `?:` pour réutiliser l'id précédent dans le cas de l'édition, et en créer un sinon:

```kotlin
val id = task?.id ?: UUID.randomUUID().toString()
```

- Au retour dans votre launcher, mettez à jour la liste: `taskList = taskList.map { if (it.id == task.id) task else it }`
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
