# TD 3 - Actions & Intents

L'objectif de ce TD est d'implémenter des actions sur nos tâches, en naviguant entre des `Activity` et de les partager des infos entre elle ou dans une autre application avec des `Intent`.


## Suppression d'une tache

Dans le layout de votre ViewHolder, ajouter un `ImageButton` qui servira à supprimer la tâche associée. Vous pouvez utiliser par exemple l'icone `@android:drawable/ic_menu_delete`

**Rappel:** Une [lambda](https://kotlinlang.org/docs/reference/lambdas.html) est un type de variable qui contient un bloc de code pouvant prendre des arguments et retourner un résultat, c'est donc une fonction que l'on utilise comme une variable !

Aidez vous des lignes de code plus bas pour réaliser un "Click Listener" à l'aide d'une lambda en suivant ces étapes:

- Dans l'adapteur, ajouter une lambda `onDeleteClickListener` qui prends en arguments une `Task` et ne renvoie rien: `(Task) -> Unit`
- Utilisez cette lambda avec dans le `onClickListener` du bouton supprimer
- Dans le fragment, accéder au `onDeleteClickListener` depuis l'adapter et implémentez là: donnez lui comme valeur une lambda qui va supprimer la tache passée en argument de la liste 

```kotlin
// Déclaration de la variable lambda dans l'adapter:
var onDeleteClickListener: ((Task) -> Unit)? = null

// "implémentation" de la lambda dans le fragment:
adapter.onDeleteClickListener = { task ->
    // Supprimer la tâche
}

// Utilisation de la lambda dans le ViewHolder:
onDeleteClickListener?.invoke(task)
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
- Dans celle ci, overrider `onActivityResult`dans le `TaskFragment` pour récupérer cette task et l'ajouter à la liste
```kotlin
val task = data!!.getSerializableExtra(TaskActivity.TASK_KEY) as Task 
```
- Faites en sorte que la nouvelle tache s'affiche à notre retour sur l'activité principale
- Maintenant, récupérez les valeurs entrées dans les `EditText` pour les donner à la création de votre tâche (vous devrez faire un `toString()`)

## Édition d'une tâche

- Ajouter une bouton permettant d'éditer chaque tâche en ouvrant l'activité `TaskActivity` pré-remplie avec les informations de la tâche
- Pour transmettre des infos d'une activité à l'autre, vous pouvez utiliser la méthode `putExtra` depuis une instance d'`intent`
- Inspirez vous de l'implémentation du bouton supprimer et du bouton ajouter
- Vous pouvez ensuite récuperer dans le `onCreate` de l'activité les infos que vous avez passées:
    - récupérex la tâche passée avec un `getSerializableExtra` et un `as? Task`
    - Vous pourrez tirer parti de la variable `Task?` (nullable) pour réutiliser le code de la création et remplir les `EditText`
    - De même vous pourrez utiliser l'opérateur `?:` pour setter l'`id` en utilisant la méthode `UUID...` précédente par défaut
    - Utilisez `setText` pour préremplir les `EditText`
- Vérifier que les infos éditées s'affichent bien à notre retour sur l'activité principale.

> Pour la classe IIM - A5 IWM: passez au TD 4 tout de suite

---

## Changements de configuration

Que se passe-t-il si vous tournez votre téléphone ? 🤔

- Pour sauvegarder votre liste de task, implémentez la méthodes suivante:

```kotlin
override fun onSaveInstanceState(outState: Bundle)
```
Il faudra aussi que votre classe `Task` hérite de `Parcelable`: pour implémenter automatiquement les méthodes nécessaires, ajoutez à votre classe l'annotation `@Parcelize` et à `app/build.gradle`, ajouter:

```groovy
androidExtensions {
    experimental = true
}
```

- Puis, pour récupérer cette list, utilisez l'argument `savedInstanceState` de `onCreateView`

## Partager

- Ajouter la possibilité de partager du texte **depuis** les autres applications et ouvrir le formulaire de création de tâche pré-rempli ([Documentation][1])
- Ajouter la possibilité de partager du texte **vers** les autres applications avec un `OnLongClickListener` sur les tâches ([Documentation][2])


[1]: https://developer.android.com/training/sharing/receive

[2]: https://developer.android.com/training/sharing/send

