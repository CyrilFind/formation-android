# TP 2 - Actions & Intents

L'objectif de ce TP est d'implémenter des actions sur nos tâches, en naviguant entre des `Activity` et de les partager des infos entre elle ou dans une autre application avec des `Intent`.

## Suppression d'une tache

Dans le layout de votre ViewHolder, ajouter un `ImageButton` qui servira à supprimer la tâche associée. Vous pouvez utiliser par exemple l'icone `@android:drawable/ic_menu_delete`

**Rappel:** Une [lambda](https://kotlinlang.org/docs/reference/lambdas.html) est un type de variable qui contient un bloc de code pouvant prendre des arguments et retourner un résultat, c'est donc une fonction que l'on utilise comme une variable !

Aidez vous des lignes de code plus bas pour réaliser un "Click Listener" à l'aide d'une lambda en suivant ces étapes:

- Dans l'adapteur, ajouter une propriété lambda `onDeleteTask` qui prends en arguments une `Task` et ne renvoie rien: `(Task) -> Unit` et l'initier à `null` (elle ne fait rien par défaut)
- Utilisez cette lambda dans le `onClickListener` du bouton supprimer
- Dans le fragment, accéder à `onDeleteTask` depuis l'adapter et implémentez là: donnez lui comme valeur une lambda qui va supprimer la tache passée en argument de la liste

```kotlin
// Déclaration de la variable lambda dans l'adapter:
var onDeleteTask: ((Task) -> Unit)? = null

// "implémentation" de la lambda dans le fragment:
adapter.onDeleteTask = { task ->
    // Supprimer la tâche
}

// Utilisation de la lambda dans le ViewHolder:
onDeleteTask?.invoke(task)
```

## Ajout de tâche complet

- Créer un package `task`
- Créez y la nouvelle `TaskActivity`, n'oubliez pas de la déclarer dans le manifest
- Créer un layout contenant 2 `EditText`, pour le titre et la description et un bouton pour valider
- Définir une constante statique `ADD_TASK_REQUEST_CODE`:

```kotlin
companion object {
    const val ADD_TASK_REQUEST_CODE = 666
}
```

> **Rappel**: La valeur importe peu, elle servira seulement à savoir d'où on vient dans `onActivityResult(...)`

- Changer l'action du FAB pour qu'il ouvre cette activité avec un `Intent`, en attendant un resultat:

```kotlin
val intent = Intent(activity, TaskActivity::class.java)
startActivityForResult(intent, ADD_TASK_REQUEST_CODE)
```

- Dans le `onCreate` de la nouvelle activité, récupérer le bouton de validation puis setter son `onClickListener` pour qu'il crée une tâche:

```kotlin
// Instanciation d'un nouvel objet [Task]
val newTask = Task(id = UUID.randomUUID().toString(), title = "New Task !")
```

- Faites hériter `Task` de `Serializable` pour pouvoir passer des objets `Task` dans les `intent`
- Passez `newTask` dans l'intent avec `putExtra(...)`
- utlisez `setResult(...)` et `finish()` pour retourner à l'activité principale
- Dans celle ci, overrider `onActivityResult` dans le `TaskFragment` pour récupérer cette task et l'ajouter à la liste

```kotlin
val task = data?.getSerializableExtra(TaskActivity.TASK_KEY) as? Task
```

- Faites en sorte que la nouvelle tache s'affiche au retour sur l'activité principale
- Maintenant, récupérez les valeurs entrées dans les `EditText` pour les donner à la création de votre tâche (vous devrez faire un `toString()`)

## Édition d'une tâche

- Ajouter une bouton permettant d'éditer chaque tâche en ouvrant l'activité `TaskActivity` pré-remplie avec les informations de la tâche
- Pour transmettre des infos d'une activité à l'autre, vous pouvez utiliser la méthode `putExtra` depuis une instance d'`intent`
- Inspirez vous de l'implémentation du bouton supprimer et du bouton ajouter
- Vous pouvez ensuite récupérer dans le `onCreate` de l'activité les infos que vous avez passées:

  - récupérez la tâche passée avec un `getSerializableExtra` et un `as? Task`
  - Vous pourrez tirer parti de la variable `Task?` (nullable) pour réutiliser le code de la création et remplir les `EditText`
  - De même vous pourrez utiliser l'opérateur `?:` pour setter l'`id` en utilisant la méthode `UUID...` précédente par défaut
  - Utilisez `setText` pour préremplir les `EditText`

- Au retour dans `onActivityResult`, vous pouvez utiliser `indexOfFirst { /* une condition */ }` sur votre liste pour trouver la tache concernée et la remplacer dans la liste, et s'il n'y  a pas, c'est qu'il s'agit d'un ajout
- Vérifier que les infos éditées s'affichent bien à notre retour sur l'activité principale.

## Nouvelle API ActivityResult

Depuis peu il existe une façon plus élégante et simple de lancer une activité en attendant un résultat, basée sur les lambdas: lisez la [documentation][3]

Dans le fichier `app/build.gradle` > `dependencies {...}`, ajouter:

```groovy
implementation 'androidx.activity:activity-ktx:1.2.0-rc01'
implementation 'androidx.fragment:fragment-ktx:1.3.0-rc01'
```

Changez votre code pour utiliser cette nouvelle méthode, par ex avec `StartActivityForResult()`:

```kotlin
val startForResult = registerForActivityResult(StartActivityForResult()) {...}
// ...
startForResult.launch(intent)
```

Mais vous pouvez aussi définir un [contrat spécifique](https://developer.android.com/training/basics/intents/result#custom):

```kotlin
class EditTask : ActivityResultContract<Task, Task>() {
    override fun createIntent(...)
    override fun parseResult(...)
}
```

## Partager

- En modifiant `AndroidManifest.xml`, ajouter la possibilité de partager du texte **depuis les autres applications** (par ex en surlignant un texte dans un navigateur puis en cliquant sur "partager") et ouvrir le formulaire de création de tâche avec une description pré-remplie ([Documentation][1])
- En utilisant un `Intent` **implicite**, ajouter la possibilité de partager du texte **vers les autres applications** (avec un `OnLongClickListener` sur les tâches par ex ou bien avec un bouton dans la vue formulaire) ([Documentation][2])

## Changements de configuration

Que se passe-t-il si vous tournez votre téléphone pour passer l'app en mode paysage ? 🤔

- Une façon de régler ce soucis est d'overrider la méthode suivante:

```kotlin
override fun onSaveInstanceState(outState: Bundle)
```

- Il faudra utiliser `putParcelableArrayList`

- Il faudra aussi que votre classe `Task` hérite de `Parcelable`: pour implémenter [automatiquement][4] les méthodes nécessaires, ajoutez le plugin `kotlin-parcelize` à votre `app/build.gradle` et l'annotation `@Parcelize` à votre classe `Task`

- Puis, pour récupérer cette liste, utilisez l'argument `savedInstanceState` et la méthode `getParcelableArrayList` dans `onCreateView`

[1]: https://developer.android.com/training/sharing/receive

[2]: https://developer.android.com/training/sharing/send

[3]: https://developer.android.com/training/basics/intents/result

[4]: https://developer.android.com/kotlin/parcelize
