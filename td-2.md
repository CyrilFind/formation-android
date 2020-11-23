# TD 2 - RecyclerView

*Objectif*: implémenter un écran affichant une liste de tâches et permettre de créer des nouvelles tâches.

⚠️ Lisez toutes les questions: souvent vous bloquez simplement parce que vous n'avez pas encore regardé l'étape suivante.

🚀 Aidez vous de l'IDE: Android Studio fait beaucoup de travail pour vous donc utilisez l'autocompletion et les raccourcis: `Alt` + `Enter` pour des "💡 QuickFix" et `Shift, Shift + "recherche"` pour tout le reste (recherches, actions, options, ...)

## Créer un projet

- Utilisez l'IDE pour créer un projet "Empty Activity"
- Donnez lui un nom personnalisé (ex: ToDoNicolasAlexandre)
- Choisissez un package name (ex: `com.nicoalex.todo`)
- Language "Kotlin"
- Minimum API Level: API 23, Android 6.0 (Marshmallow)
- Initialisez un projet git et faites un commit initial
- Committez régulièrement: à chaque fois que vous avez quelque chose qui compile et qui fonctionne.

## Ajout de Dépendances

Dans le fichier `app/build.gradle`, ajouter la ligne suivante dans `dependencies { ... }`:

```groovy
implementation "androidx.recyclerview:recyclerview:1.1.0"
```

## Gestion des fichiers

Les fichiers source Java ou Kotlin sont rangés en "packages" (noté en haut de chaque classe: `package com.nicoalex.todo.nomdupackage`) qui sont aussi répliqués en tant que dossiers dans le file system

Dans le volet "Projet" (à gauche d'Android Studio), vous pouvez choisir diverses visualisations de vos fichers: la plus adaptée est "Android", mais il peut parfois être pratique de passer en "Project Files" par ex

- Ouvrez l'arborescence de fichiers jusqu'à la racine de vos fichiers source et créez un package `tasklist`:

`app > java > com.nicoalex.todo > clic droit > New > package > "tasklist"`

Vous y mettrez tous les fichiers source (Kotlin) concernant la liste de tâches

## TaskListFragment

- Créez y un fichier kotlin `TaskListFragment.kt` qui contiendra la classe `TaskListFragment`:

```kotlin
class TaskListFragment : Fragment() {}
```

- Créer le layout associé `fragment_task_list.xml`
- Dans `TaskListFragment`, overrider la méthode `onCreateView(...)`: commencez à taper `onCrea...` et utilisez l'auto-completion de l'IDE pour vous aider (vous pouvez supprimer la ligne `super.onCreateView(...)`)
- Cette méthode vous demande de *retourner* la `rootView` à afficher: créez la à l'aide de votre nouveau layout comme ceci:

```kotlin
val rootView = inflater.inflate(R.layout.fragment_task_list, container, false)
```

- Remplacez la balise `<TextView.../>` par une balise `<fragment.../>` dans votre activité principale:
  - Utilisez le glisser-déplacé en mode Design ou bien l'autocomplétion en mode Text pour spécifier l'attribut `android:name`: il faut donner la classe de Fragment qui sera affichée dans cette balise (ex: `"com.nicoalex.todo.tasklist.TaskListFragment"`)
  - Ajoutez un id: `android:id="@+id/fragment_tasklist"` pour...ne pas faire crasher l'app 🤷‍♂️

## La liste des tâches

- Pour commencer, la liste des tâches sera simplement une liste de `String`:

```kotlin
private val taskList = listOf("Task 1", "Task 2", "Task 3")
```

- Dans le layout associé à `TaskListFragment`, placez une balise `<androidx.recyclerview.widget.RecyclerView...>`:

- Créer une nouvelle classe `TaskListAdapter`:

```kotlin
class TaskListAdapter(private val taskList: List<String>) : RecyclerView.Adapter<TaskListAdapter.TaskViewHolder>() {}
```

- À l'intérieur de `TaskListAdapter`, créer la classe `TaskViewHolder`:

```kotlin
inner class TaskViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
  fun bind(taskTitle: String) {
    itemView.apply { // `apply {}` permet d'éviter de répéter `itemView.*`
    // TODO: afficher les données et attacher les listeners aux différentes vues de notre [itemView]
    }
  }
}
```

- Créer le layout `item_task.xml` correspondant à une cellule (`TaskViewHolder`)

```xml
<LinearLayout
  xmlns:android="http://schemas.android.com/apk/res/android"
  android:orientation="vertical"
  android:layout_width="match_parent"
  android:layout_height="wrap_content">

  <TextView
      android:id="@+id/task_title"
      android:background="@android:color/holo_blue_bright"
      android:layout_width="match_parent"
      android:layout_height="wrap_content" />
</LinearLayout>
```

- Dans `TaskListFragment > onViewCreated`, récupérer la `RecyclerView` du layout en utilisant un "synthetic" ou un `findViewbyId`:

```kotlin
    // Pour une [RecyclerView] ayant l'id "recycler_view":
    var recyclerView = view.findById<RecyclerView>(R.id.recycler_view)
    recyclerView.layoutManager = ...

    // En utilisant les synthetics, on écrit juste l'id directement (c'est magique ✨):
    recycler_view.layoutManager = ...
```

- Donnez lui un `layoutManager`: `LinearLayoutManager(activity)`
- Donnez lui un `adapter`: `TaskListAdapter(taskList)` (ne marche pas pour l'instant)

**Rappel**: l'Adapter gère le recyclage des cellules (`ViewHolder`): il en `inflate` juste assez pour remplir l'écran (coûteux) puis change seulement les données quand on scroll (peu coûteux)

## Implémentation du RecyclerViewAdapter

Dans le `TaskListAdapter`, implémenter toutes les méthodes requises:

**Astuce**: Pré-remplissez votre adapter en cliquant sur le nom de votre classe (qui doit être pour l'instant soulignée en rouge) et cliquez sur l'ampoule jaune ou tapez `Alt` + `ENTER` (sinon, `CTRL` + `O` n'importe où dans la classe)

- `getItemCount` doit renvoyer la taille de la liste de tâche à afficher
- `onCreateViewHolder` doit retourner un nouveau `TaskViewHolder`
  en générant un `itemView`, à partir du layout `item_task.xml`:

```kotlin
val itemView = LayoutInflater.from(parent.context).inflate(R.layout.item_task, parent, false)
```

- `onBindViewHolder` doit insèrer la donnée dans la cellule (`TaskViewHolder`) en fonction de sa `position` dans la liste en utilisant la méthode `bind()` que vous avez créée dans `TaskViewHolder` (elle ne fait rien pour l'instant)
- Implémentez maintenant `bind()` qui doit récupérer une référence à la `TextView` dans `item_layout.xml` et y insérer le texte récupéré en argument
- Lancez l'app: vous devez voir 3 tâches s'afficher 👏

## Ajout de la data class Task

- Dans un nouveau fichier, créer une `data class Task` avec 3 attributs: un id, un titre et une description
- Ajouter une valeur par défaut à la description.
- Dans le `TaskListFragment`, remplacer la liste `taskList` par

 ```kotlin
private val taskList = listOf(
    Task(id = "id_1", title = "Task 1", description = "description 1"),
    Task(id = "id_2", title = "Task 2"),
    Task(id = "id_3", title = "Task 3")
)
```

- Corriger votre code en conséquence afin qu'il compile de nouveau
- Enfin afficher la description en dessous du titre
- Admirez avec fierté le travail accompli 🤩

## Ajout de tâche simple

- Changez la root view de `fragment_task_list.xml` en ConstraintLayout en faisant un clic droit dessus en mode design
- Ouvrez le volet "Resource Manager" à gauche, cliquez sur le "+" en haut à gauche puis "Vector Asset" puis double cliquez sur le clipart du logo android et trouvez une icone "+" (en tapant "add") puis "finish" pour ajouter une icone à vos resource
- Ajouter un Floating Action Button (FAB) en bas à droite de ce layout et utilisez l'icone créée
- Par défaut l'icône est noire mais vous pourrez utiliser l'attribut `android:tint` du bouton pour la rendre blanche (tapez "white" et laissez l'IDE compléter)
- Donnez des contraintes en bas et à droite de ce bouton (vous pouvez utiliser le mode "Aimant" qui essaye de donner les bonnes contraintes automagiquement)
- Transformer votre liste de tâches `taskList` en `mutableListOf(...)` afin de pouvoir y ajouter ou supprimer des éléments
- Utilisez `.setOnClickListener {}` sur le FAB pour ajouter une tâche à votre liste:

```kotlin
// Instanciation d'un objet task avec des données préremplies:
Task(id = UUID.randomUUID().toString(), title = "Task ${taskList.size + 1}")
```

- Dans cette lambda, **notifier l'adapteur** (aidez vous des suggestions de l'IDE) pour que votre modification s'affiche

## Aller plus loin

Recherchez la documentation pour chaque étape et n'hésitez pas à poser des questions:

- Simplifier l'implémentation de `TasksListAdapter` en héritant de `ListAdapter` au lieu de `RecyclerView.Adapter`
- Utiliser du `ViewBinding` à la place des "synthetics" ou des `findViewByIds` et pour `inflate` les différents layouts
- Utiliser du `DataBinding` pour également `bind`-er les tasks directement dans le XML
- Créer un `BindingAdapter` pour également databinder la liste de tâches
