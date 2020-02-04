# TD 2 - RecyclerView

L'objectif de ce TD est d'implémenter un écran affichant une liste de tâches, de permettre de créer des nouvelles tâches.

⚠️ Lisez toutes les questions: souvent vous bloquez parce que vous n'avez pas fait l'étape suivante

🚀 Aidez vous de l'IDE: Android Studio fait beaucoup de travail pour vous donc utilisez l'autocompletion et les raccourcis: `Alt` + `Enter` pour des "quickfix" et `Shift, Shift + "recherche"` pour tout le reste 

## Créer un projet

- Utilisez l'IDE pour créer un projet "Empty Activity"
- Donnez lui un nom personalisé (ex: ToDoNicolasAlexandre)
- Choisissez un package name (ex: `com.nicoalex.todo`)
- Language "Kotlin"
- Minimum API Level: 6.0
- Cochez "use androidx ..."
- Initialisez un projet git et faites un commit initial
- Committez régulièrement: à chaque fois que vous avez quelque chose qui compile et qui fonctionne

## Dépendances RecyclerView
Dans le fichier `app/build.gradle`, ajouter:

```groovy
implementation "androidx.recyclerview:recyclerview:1.1.0"
```

## Gestion des fichiers

Les fichiers source Java sont rangés en "packages" (noté en haut de chaque classe: `package com.nicoalex.todo.blabla`) qui sont aussi répliqués en tant que dossiers dans le file system

Dans le volet "Projet" (à gauche d'Android Studio), vous pouvez choisir diverses visualisations de vos fichers: la plus adaptée est "Android", mais il peut parfois être pratique de passer en "Project Files" par ex

- Ouvrez l'arborescence de fichiers jusqu'à la racine de vos fichiers source et créez un package `tasklist`:

`app > java > com.nicoalex.todo > clic droit > New > package > "tasklist"`

Vous y mettrez tous les fichiers concernant la liste de tâches


## TaskListFragment
- Créez y un fichier kotlin `TaskListFragment.kt` qui contiendra la classe `TaskListFragment`:

```kotlin
class TaskListFragment : Fragment() {}
```

- Créer le layout associé `fragment_task_list.xml`
- Dans `TaskListFragment`, overrider (surcharger) la méthode `onCreateView(...)` (commencez à taper `onCrea...` et utilisez l'auto-completion de l'IDE pour vous aider)
- Initialisez y la `rootView` à l'aide du layout créé et retournez la

```kotlin
val rootView = inflater.inflate(R.layout.fragment_task_list, container, false)
```
- Remplacez la balise `<TextView.../>` par une balise `<fragment.../>` dans votre activité principale
- Utilisez `android:name` pour specifier la classe de votre Fragment (ex: `"com.nicoalex.todo.TaskListFragment"`)

## La liste des tâches

- Pour commencer, la liste des tâches sera simplement un tableau de `String`:

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
	   // C'est ici qu'on reliera les données et les listeners une fois l'adapteur implémenté
	}
}
```

- Créer le layout `item_task.xml` correspondant à une cellule (`TaskViewHolder`)

```xml
<LinearLayout 
  xmlns:android="http://schemas.android.com/apk/res/android"
  android:orientation="horizontal" 
  android:layout_width="match_parent"
  android:layout_height="wrap_content">

  <TextView
      android:id="@+id/task_title"
      android:background="@android:color/holo_blue_bright"
      android:layout_width="match_parent"
      android:layout_height="wrap_content" />
</LinearLayout>
```


- Dans `TaskListFragment`, overrider `onViewCreated` et récupérer la `RecyclerView` du layout en utilisant un "synthetic" ou un `findViewbyId`
- Donnez lui un `layoutManager`: `LinearLayoutManager(activity)`
- Donnez lui un `adapter`: `TaskListAdapter(taskList)` (ne marche pas pour l'instant)

**Rappel**: l'Adapteur gère le recyclage des cellules (`ViewHolder`): il en `inflate` juste assez pour remplir l'écran (coûteux) puis change seulement les données quand on scroll (peu coûteux)

## Implémentation du RecyclerViewAdapter

Dans le `TaskListAdapter`, implémenter toutes les méthodes requises:

**Astuce**: Utilisez l'IDE pour faciliter l'implémentation des méthodes en cliquant sur le nom de votre classe (qui doit être soulignée en rouge) et cliquez sur l'ampoule jaune ou tapez `Alt` + `ENTER` (sinon, `CTRL` + `O` n'importe où dans la classe)

- `getItemCount` qui renvoie la taille de la liste de tâche à afficher
- `onCreateViewHolder` qui returne un nouveau `TaskViewHolder`: vous aurez besoin d'un `itemView`, généré à partir du layout `item_task.xml`: 

```kotlin
val itemView = LayoutInflater.from(parent.context).inflate(R.layout.item_task, parent, false)
```

- `onBindViewHolder` qui insère la donnée dans la cellule (`TaskViewHolder`) en fonction de la position dans la liste.

- Lancez l'app: vous devez voir 3 tâches s'afficher 👏

## Ajout de la data class Task

- Dans un nouveau fichier, créer une `data class Task` avec 3 attributs: un id, un titre et une description. 
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

- Changez la root view de `fragment_task_list.xml` en ConstraintLayout en faisant un clic droit dessus en mode design (si ce n'est pas déjà le cas)
- Ouvrez le volet "Resource Manager" à gauche, cliquez sur le "+" en haut à gauche puis "Vector Asset" puis double cliquez sur le clipart du logo android et selectionnez une icone + (en cherchant "add" dans la barre de recherche) puis "finish" pour ajouter une icone à vos resource
- Par défaut l'icône est noire mais vous pouvez utiliser l'attribut `android:tint` du bouton pour la rendre blanche (tapez "white" et laissez l'IDE compléter)
- Ajouter un Floating Action Button (FAB) en bas à droite de ce layout et utilisez l'icone créée 
- Donnez des contraintes en bas et à droite de ce bouton
- Transformer votre liste de taches `taskList` en `mutableListOf(...)` afin de pouvoir la modifier 
- Utilisez `.setOnClickListener {}` sur le FAB pour ajouter une tâche à votre liste:

```kotlin
// Instanciation d'un objet task avec des données préremplies:
Task(id = UUID.randomUUID().toString(), title = "Task ${taskList.size + 1}")
```

- Dans cette callback, **notifier l'adapteur** (aidez vous des suggestions de l'IDE) pour que votre modification s'affiche
