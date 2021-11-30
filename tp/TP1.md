# TP 1 - RecyclerView

## Objectif

implémenter un écran affichant une liste de tâches et permettre de créer des nouvelles tâches.

<aside class="negative">

⚠️ Lisez toutes les questions: souvent vous bloquez simplement parce que vous n'avez pas encore regardé l'étape suivante ou le sujet dans son ensemble.

</aside>

🚀 Aidez vous de l'IDE: Android Studio fait beaucoup de travail pour vous donc utilisez l'autocompletion et les raccourcis:

- `Ctrl` ou `Cmd` + `click` pour voir les usages ou la définition d'un élément
- `Alt` + `Enter` pour des "💡 QuickFix"
- `Shift, Shift + "recherche"` pour tout le reste (rechercher une variable, fonction, classe, actions, options, ...)

## Créer un projet

Vous allez créer un unique projet "fil rouge" que vous mettrez à jour au fur à mesure des TPs:

- Utilisez l'IDE pour créer un projet `Empty Activity`
- Donnez lui un nom personnalisé comme `ToDoNicolasAlexandre` (⚠️ pas `TP1` SVP ⚠️)
- Choisissez un package name (ex: `com.nicoalex.todo`)
- Language `Kotlin`
- Minimum API Level: API 23, Android 6.0 (Marshmallow)
- Initialisez un projet git et faites un commit initial
- Committez régulièrement: à chaque fois que vous avez quelque chose qui compile et qui fonctionne.
- Faites au minimum un commit à la fin de chaque TP

## Ajout de Dépendances

Dans `./build.gradle` (celui du _projet_), vérifiez que `kotlin_version` est récent (ex: `1.5.31`)

Dans `app/build.gradle` (celui du _module_ `app`), ajouter les libs suivante dans `dependencies{}`:

```groovy
implementation "androidx.recyclerview:recyclerview:1.2.1"
implementation 'androidx.fragment:fragment-ktx:1.4.0'
implementation 'androidx.activity:activity-ktx:1.4.0'
```

Vérifiez que le block `android{}` ressemble à ceci:

```groovy
android {
    compileSdkVersion 31
    defaultConfig {
        applicationId "com.nicoalex.kodo"
        minSdkVersion 23
        targetSdkVersion 31
        // ...
    }

    // ...
    compileOptions {
        sourceCompatibility = 1.8
        targetCompatibility = 1.8
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }
  }
}
```

## Gestion des fichiers

Les fichiers source Java ou Kotlin sont rangés en "packages" (noté en haut de chaque classe: `package com.nicoalex.todo.nomdupackage`) qui sont aussi répliqués en tant que dossiers dans le filesystem

Dans le volet "Projet" (à gauche d'Android Studio), vous pouvez choisir diverses visualisations de vos fichiers: la plus adaptée pour nous est "Android", mais il peut parfois être pratique de passer en "Project Files" par ex pour voir l'arborescence réelle.

Créez un nouveau package `tasklist` dans votre package source de base:

`app > java > com.nicoalex.todo > clic droit > New > package > "tasklist"`

Vous y mettrez tous les fichiers source (Kotlin) concernant la liste de tâches

## MainActivity

Cette activity va servir de conteneur de fragments:

Dans `activity_main.xml`, remplacez la balise `TextView` par celle ci (à adapter):

```xml
 <androidx.fragment.app.FragmentContainerView
    android:name="com.nicoalex.todo.TaskListFragment"
    android:id="@+id/fragment_tasklist"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    />
```

## TaskListFragment

- Créez dans votre nouveau package `tasklist` un fichier kotlin `TaskListFragment.kt` qui contiendra la classe `TaskListFragment`:

```kotlin
class TaskListFragment : Fragment() {}
```

- Créer le layout associé `fragment_task_list.xml` dans `res/layout`

<aside class="positive">

vous pouvez aussi utiliser l'IDE pour créer les 2 fichiers à la fois: `Clic droit sur le package > New > Fragment > Fragment (Blank)`

</aside>

- Dans `TaskListFragment`, overrider la méthode `onCreateView(...)`: commencez à taper `onCrea...` et utilisez l'auto-completion de l'IDE pour vous aider (vous pouvez supprimer la ligne `super.onCreateView(...)`)
- Cette méthode vous demande de _retourner_ la `rootView` à afficher: créez la à l'aide de votre nouveau layout comme ceci:

```kotlin
val rootView = inflater.inflate(R.layout.fragment_task_list, container, false)
```

<aside class="negative">
⚠️ Si vous exécutez du code *avant* cette ligne `inflate`, il va crasher ou ne rien faire car votre vue n'existera pas encore
</aside>

- Pour commencer, la liste des tâches sera simplement une liste de `String` que vous pouvez ajouter en propriété de votre classe `TaskListFragment`:

```kotlin
private val taskList = listOf("Task 1", "Task 2", "Task 3")
```

## RecyclerView et Adapter

- Dans le layout associé à `TaskListFragment`, placez une balise `RecyclerView` (vous pouvez taper `< Recyc...>` et vous aider de l'IDE ou bien utilisez le mode visuel):

- Dans un nouveau fichier `TaskListAdapter.kt`, créez 2 nouvelles classes: `TaskListAdapter` et `TaskViewHolder`:

```kotlin
// l'IDE va râler ici car on a pas encore implémenté les méthodes nécessaires
class TaskListAdapter) : RecyclerView.Adapter<TaskListAdapter.TaskViewHolder>() {

  var taskList: List<String>

  // on utilise `inner` ici afin d'avoir accès aux propriétés de l'adapter directement
  inner class TaskViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    fun bind(taskTitle: String) {
      // on affichera les données ici
    }
  }
}

```

- Dans `TaskListFragment`, overridez `onViewCreated` pour y récupérer la `RecyclerView` du layout en utilisant un `findViewById`:

```kotlin
    val recyclerView = view.findViewById<RecyclerView>(R.id.id_de_votre_recycler_view)
    recyclerView.layoutManager = ...
```

- Donnez lui un `layoutManager`: `LinearLayoutManager(context)`
- créez un `adapter` et passez lui la liste actuelle:

```kotlin
val adapter = TaskListAdapter() // ne marche pas pour l'instant
adapter.tasklist = taskList
```

- assignez cet adapter à votre recyclerView

## Item View

- Créer le layout `item_task.xml` correspondant à une cellule (et donc lié à `TaskViewHolder`)

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

## Implémentation du RecyclerViewAdapter

<aside class="positive">

**Rappel**: l'Adapter gère le recyclage des cellules (`ViewHolder`): il en `inflate` juste assez pour remplir l'écran (coûteux) puis change seulement les données quand on scroll (peu coûteux)

</aside>

Dans le `TaskListAdapter`, implémenter toutes les méthodes requises:

**Astuce**: Pré-remplissez votre adapter en cliquant sur le nom de votre classe (qui doit être pour l'instant soulignée en rouge) et cliquez sur l'ampoule jaune ou tapez `Alt` + `ENTER` (sinon, `CTRL` + `O` n'importe où dans la classe)

- `getItemCount` doit renvoyer la taille de la liste de tâche à afficher
- `onCreateViewHolder` doit retourner un nouveau `TaskViewHolder`
  en générant un `itemView`, à partir du layout `item_task.xml`:

```kotlin
val itemView = LayoutInflater.from(parent.context).inflate(R.layout.item_task, parent, false)
```

- `onBindViewHolder` doit insérer la donnée dans la cellule (`TaskViewHolder`) en fonction de sa `position` dans la liste en utilisant la méthode `bind()` que vous avez créée dans `TaskViewHolder` (elle ne fait rien pour l'instant)
- Implémentez maintenant `bind()` qui doit récupérer une référence à la `TextView` dans `item_task.xml` et y insérer le texte récupéré en argument
- Lancez l'app: vous devez voir 3 tâches s'afficher 👏

## Ajout de la data class Task

- Dans un nouveau fichier, créer une `data class Task` avec 3 attributs: un id, un titre et une description
- Ajouter une valeur par défaut à la description.
- Dans le `TaskListFragment`, remplacer la liste `taskList` par

```kotlin
private var taskList = listOf(
   Task(id = "id_1", title = "Task 1", description = "description 1"),
   Task(id = "id_2", title = "Task 2"),
   Task(id = "id_3", title = "Task 3")
)
```

- Corriger et adapter votre code en conséquence afin qu'il compile de nouveau en utilisant votre `data class` à la place de simples `String`
- Ajoutez la description en dessous du titre (avec une seconde `TextView`)
- Admirez avec fierté le travail accompli 🤩

## Ajout du FAB

- Changez la root view de `fragment_task_list.xml` en ConstraintLayout en faisant un clic droit dessus en mode design
- Ouvrez le volet "Resource Manager" à gauche, cliquez sur le "+" en haut à gauche puis "Vector Asset" puis double cliquez sur le clipart du logo android et trouvez une icone "+" (en tapant "add") puis "finish" pour ajouter une icone à vos resource
- Ajouter un Floating Action Button (FAB) en bas à droite de ce layout et utilisez l'icone créée
- Par défaut l'icône est noire mais vous pourrez utiliser l'attribut `app:tint` du bouton pour la rendre blanche (tapez "white" et laissez l'IDE compléter)
- Donnez des contraintes en bas et à droite de ce bouton

<aside class="positive">

Vous pouvez configurer les contraintes à la main ou les faire deviner à l'IDE:

- quand vous déplacez le bouton (attendez de voir apparaître des lignes pointillées) avec l'icône "Aimant 🧲" activée.
- en fonction du placement actuel de vos vues dans l'outil visuel
en cliquant sur l'icône "baguette magique 🪄".

</aside>

## Ajout de tâche rapide

Utilisez `.setOnClickListener {}` sur le FAB pour ajouter une tâche à votre liste:

```kotlin
// Instanciation d'un objet task avec des données préremplies:
val newTask = Task(id = UUID.randomUUID().toString(), title = "Task ${taskList.size + 1}")
taskList = taskList + newTask
```

<aside class="negative">

⚠️ pour que votre modification s'affiche, il faut passer la nouvelle liste à votre adapter puis le **[notifier](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.Adapter#notifyDataSetChanged())** de cette nouvelle donnée.
Ce n'est pas idéal: on devrait plutôt utiliser un `ListAdapter`, c'est l'étape suivante
</aside>

## ListAdapter

Améliorer l'implémentation de `TasksListAdapter` en héritant de [`ListAdapter`](https://developer.android.com/reference/androidx/recyclerview/widget/ListAdapter) au lieu de `RecyclerView.Adapter`

Il faudra notamment: créer un `DiffUtil.ItemCallback<Task>` et le passer au constructeur parent, supprimer la propriété `taskList` et utiliser `getItem(position)` à la place, et vous pourrez supprimer `getItemCount` qui sera déjà implémentée pour vous (cf [slides](../slides/3%20-%20RecyclerView.html#7) pour un squelette d'implémentation)

## ViewBinding

Utiliser le [`ViewBinding`](https://developer.android.com/topic/libraries/view-binding) pour `inflate` les différents layouts et supprimer les `findViewByIds` (cf [slides](../slides/2%20-%20UI.html#9) pour un squelette d'implémentation)
