# TP 1 - RecyclerView

## Objectif

implémenter un écran affichant une liste de tâches et permettre de créer des nouvelles tâches.

<aside class="negative">
⚠️ Lisez toutes les questions: souvent vous bloquez simplement parce que vous n'avez pas encore regardé l'étape suivante ou le sujet dans son ensemble.

**Sinon, demandez moi!!**

</aside>

<aside class="positive">

Remarque: si vous n'avez pas bien paramétré votre IDE, relisez le début du [TP0](./TP0)

</aside>

## Créer un projet

Vous allez créer un unique projet que vous mettrez à jour au fur à mesure des TPs:

- Créer un nouveau projet avec une `Empty VIEWS Activity` (⚠️ pas `Empty Activity` SVP ⚠️)
- Donnez lui un nom personnalisé comme `TodoNicolasAlexandre` (⚠️ pas `TP1` SVP ⚠️)
- Choisissez un package name unique de ce genre: `com.nicoalex.todo` (ce sera la racine de tous vos packages et sert d'identifiant unique d'application)
- Minimum API Level: laissez la valeur proposée par défaut
- Initialisez un projet git et faites un commit initial

<aside class="negative">

⚠️ Le projet va évoluer au cours des TP donc faites des commits régulièrement: par exemple, à chaque étape et au minimum à la fin de chaque TP

Vous allez parfois supprimer et remplacer des parties de code: ne commentez pas votre code dans tous les sens, les commits garderons l'historique.

Comme dans un vrai projet pro finalement !

</aside>

<!-- ajouter une icone ? -->

## Gestion des fichiers

📁 Les fichiers source Java ou Kotlin sont rangés en "packages":

- notés en haut de chaque classe: `package com.nicoalex.todo.nomdupackage`
- répliqués en tant que dossiers dans le filesystem: `com/nicoalex/todo/nomdupackage`

<aside class="positive">

Dans le volet "Projet" à gauche, vous pouvez choisir diverses visualisations de vos fichiers: la plus adaptée pour nous est "Android" qui affiche facilement le Manifest, les fichiers source, les fichier resources (`res`), compacte les dossiers vides ensemble (`com.nicoalex.todo`): tout ce qui est utile spécifiquement pour Android...

Mais il peut parfois être pratique de passer en "Project Files" par ex pour voir l'arborescence réelle et certains fichiers cachés autrement.

</aside>

Parcourez les différents fichiers de config, notamment les plus importants:

- `app/build.gradle.kts`: contient la configuration de module principal (`app`), notamment les versions compatibles, son propre numéro de version, etc et surtout les différentes dépendances.
- `./build.gradle.kts`: contient moins de choses, en général des plugins, mais concerne tout le projet
- `libs.versions.toml`: un catalogue de dépendances, de plugins et de versions, qui est utilisé par les fichiers précédents. Vérifiez que vous utilisez les dernières versions disponible, surtout pour `kotlin`.
- `app/src/main/AndroidManifest.xml`: contient les info de packaging de l'app comme les activités existantes, le nom de l'app, l'icône, etc.

<aside class="negative">

Les packages surlignés en vert contiennent le code de test uniquement: ne vous en occupez pas pour l'instant

</aside>

Créez un nouveau package `list` à l'intérieur votre package source de base (pas à côté !) :

`clic droit sur 'com.nicoalex.todo' > new > package > tapez 'list'`

Vous y mettrez tous les fichiers source (Kotlin) concernant la liste de tâches

## TaskListFragment

- Créez dans votre nouveau package un fichier kotlin `TaskListFragment.kt` qui contiendra la classe `TaskListFragment`:

```kotlin
class TaskListFragment : Fragment() {
   //...
}
```

- Créer le layout associé `fragment_task_list.xml` dans `res/layout`

<aside class="positive">

vous pouvez aussi utiliser Android Studio pour créer les 2 fichiers à la fois: `Clic droit sur le package > New > Fragment > Fragment (Blank)`, mais la classe sera remplie de plein de code inutile -> supprimez-le

</aside>

- Dans `TaskListFragment`, overrider la méthode `onCreateView(...)`: commencez à taper `onCrea...` et utilisez l'auto-completion de l'IDE pour vous aider (vous pouvez supprimer la ligne `super.onCreateView(...)`)

- Cette méthode vous demande de _retourner_ la `rootView` à afficher: créez la à l'aide de votre nouveau layout comme ceci:

```kotlin
val rootView = inflater.inflate(R.layout.fragment_task_list, container, false)
```

<aside class="negative">

⚠️ Si vous exécutez du code _avant_ cette ligne `inflate`, il va crasher ou ne rien faire car votre vue n'existera pas encore

</aside>

<aside class="positive">

`R` est un raccourci signifiant "Resource": c'est une classe générée automatiquement à partir des dossiers et fichiers créés dans `res` qui s'utilise comme ceci: `R.string.app_name`, `R.drawable.app_icon`, etc... afin de récupérer des `int` qui servent d'`id` à ces ressources et que l'on utilise dans les fonctions du framework Android (`getString`, `getDrawable`, etc...)

</aside>

- Pour l'instant, la liste des tâches sera simplement une liste de `String` locale, ajoutez la en tant que propriété de votre classe `TaskListFragment`:

```kotlin
private var taskList = listOf("Task 1", "Task 2", "Task 3")
```
<!-- utiliser une liste de res string pour la culture ? -->

```kotlin
<resources>
    <string name="app_name">Affirmations</string>
    <string name="task1">#1 Faire les courses</string>
    <string name="task2">#2 Faire la vaisselle</string>
    <string name="task3">#3 Faire le ménage</string>
</resources>
```
<!-- utiliser map {} ? -->
<!--         recyclerView.setHasFixedSize(true) -->

## MainActivity

Cette activity va servir de conteneur de fragments:

Dans `activity_main.xml`, remplacez la balise `TextView` par celle ci et adaptez:

```xml
 <androidx.fragment.app.FragmentContainerView
    android:name="com.nicoalex.todo.list.TaskListFragment"
    android:id="@+id/fragment_tasklist"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

## TaskListAdapter: Création

- Dans un nouveau fichier `TaskListAdapter.kt`, créez 2 nouvelles classes: `TaskListAdapter` et `TaskViewHolder`:

```kotlin
// l'IDE va râler ici car on a pas encore implémenté les méthodes nécessaires
class TaskListAdapter : RecyclerView.Adapter<TaskListAdapter.TaskViewHolder>() {

  var currentList: List<String> = emptyList()

  // on utilise `inner` ici afin d'avoir accès aux propriétés de l'adapter directement
  inner class TaskViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    fun bind(taskTitle: String) {
      // on affichera les données ici
    }
  }
}
```

<aside class="negative">

⚠️ C'est normal que l'IDE nous signale un problème ici, on le règlera plus tard

</aside>

## TaskListAdapter: Utilisation

- Dans `TaskListFragment`, créez une instance de votre nouvelle classe `TaskListAdapter` en propriété de votre fragment (comme `taskList`):

```kotlin
private val adapter = TaskListAdapter()
```

- connectez le à votre source de données dans `onCreateView`:

```kotlin
adapter.currentList = taskList
```

## RecyclerView

- Dans le layout associé à `TaskListFragment`, placez une balise `RecyclerView` (vous pouvez taper `< Recyc...` et vous aider de l'auto-complétion ou bien utilisez le mode visuel)
- ajoutez lui l'attribut `layoutManager` qui lui dit de s'afficher comme une liste (verticale par défaut):

```xml
app:layoutManager="androidx.recyclerview.widget.LinearLayoutManager"
```

<aside class="negative">

⚠️ Utilisez l'IDE pour régler le problème qu'il vous signale: seul le préfixe `android:`, correspondant au framework Android, est reconnu par défaut, et il faut donc ajouter une sorte d'équivalent de `import` mais dans le XML, pour que le préfixe `app:`, correspondant à des attributs additionnels défini par ex dans des lib (ici `recyclerview`) soit reconnu.

</aside>

- ajoutez lui un `id`: soit en mode visuel soit en mode code, en vous aidant de l'auto-complétion `android:id="@+id/....`

- Dans `TaskListFragment`, overridez `onViewCreated` pour y récupérez une référence à la `RecyclerView` du layout en utilisant `findViewById`:

```kotlin
val recyclerView = view.findViewById<RecyclerView>(R.id.id_de_votre_recycler_view)
```

- Pour fonctionner, `recyclerView` a une propriété `adapter` qui doit être connectée à l'adapter que vous avez créé (elle est nulle par défaut)

## Item View

- Créer un layout `item_task.xml` qui servira à afficher chaque cellule de la liste avec comme racine un `LinearLayout` contenant pour l'instant une seule `TextView` en enfant:

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

## TaskListAdapter: Implémentation

<aside class="positive">

**Rappel**: l'Adapter gère le recyclage des cellules (`ViewHolder`): il `inflate` un nombre suffisant de "coquilles vides" pour remplir l'écran une seule fois (coûteux) puis injecte seulement les données dedans quand on scroll (peu coûteux)

</aside>

Dans `TaskListAdapter`, implémenter toutes les méthodes requises:

**Astuce**: Pré-remplissez votre adapter en cliquant sur le nom de votre classe (qui doit être pour l'instant soulignée en rouge) et cliquez sur l'ampoule jaune ou tapez `Alt` + `ENTER` (sinon, `CTRL/CMD` + `o` n'importe où dans la classe)

- `getItemCount` doit renvoyer la taille de la liste de tâche à afficher
- `onCreateViewHolder` doit retourner un nouveau `TaskViewHolder`
  en générant un `itemView`, à partir du layout `item_task.xml`:

```kotlin
val itemView = LayoutInflater.from(parent.context).inflate(R.layout.item_task, parent, false)
```

- `onBindViewHolder` doit insérer la donnée dans la cellule (`TaskViewHolder`) en fonction de sa `position` dans la liste en utilisant la méthode `bind()` que vous avez créée dans `TaskViewHolder` (elle ne fait rien pour l'instant)
- Implémentez maintenant `bind()` qui doit récupérer une référence à la `TextView` dans `item_task.xml` et y insérer le texte récupéré en argument (pour être plus propre, déplacez cette référence en tant que propriété de votre `TaskViewHolder`)
- Lancez l'app: vous devez voir 3 tâches s'afficher 👏

## Data class

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

- Changez la root view de `fragment_task_list.xml` en `ConstraintLayout` (si ce n'est pas déjà fait) en faisant un clic droit dessus en mode design
- Ouvrez le volet `Resource Manager` à gauche, cliquez sur le `+` en haut à gauche puis `Vector Asset` puis double cliquez sur l'image du logo android et trouvez une icône `+` (en tapant `add`) puis `finish` pour ajouter une icône à vos resource
- Ajouter un `Floating Action Button` (FAB) en bas à droite de ce layout et utilisez l'icône créée
- Donnez des contraintes en bas et à droite à ce bouton

<aside class="positive">

Vous pouvez configurer les contraintes de plusieurs façons:

- soit manuellement,
- soit en activant l'icône "Aimant 🧲": déplacez le bouton, attendez de voir apparaître des lignes pointillées et relâchez le .
- soit en plaçant la vue dans l'outil visuel puis en cliquant sur l'icône "baguette magique 🪄" qui va essayer de "deviner" les contraintes qu'il faut automatiquement (ça ne marche pas toujours bien)

</aside>

## Ajout de tâche rapide

Utilisez `.setOnClickListener {}` sur le bouton d'ajout pour ajouter une tâche à votre liste à chaque fois qu'on clique dessus:

```kotlin
// Instanciation d'un objet task avec des données préremplies:
val newTask = Task(id = UUID.randomUUID().toString(), title = "Task ${taskList.size + 1}")
taskList = taskList + newTask
```

<aside class="negative">

⚠️ Votre modification de liste ne va pas s'afficher directement, il faut:

- passer la nouvelle liste à votre adapter
- puis le **[notifier](<https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.Adapter#notifyDataSetChanged()>)** que la donnée a changé

➡ créez une méthode `refreshAdapter` qui va faire les deux actions ci-dessus afin de rendre cela réutilisable

</aside>

Cette façon de "notifier" manuellement n'est pas idéale, il existe en fait une sous-classe de `RecyclerView.Adapter` qui permet de gérer cela automatiquement: `ListAdapter`

## ListAdapter

Améliorer l'implémentation de `TasksListAdapter` en héritant de [`ListAdapter`](https://developer.android.com/reference/androidx/recyclerview/widget/ListAdapter) au lieu de `RecyclerView.Adapter`

Il faudra notamment: créer un `DiffUtil.ItemCallback<Task>` et le passer au constructeur parent, supprimer `getItemCount` et la propriété `currentList` car ils sont déjà définis dans `ListAdapter`

Exemple:

```kotlin
object MyItemsDiffCallback : DiffUtil.ItemCallback<MyItem>() {
   override fun areItemsTheSame(oldItem: MyItem, newItem: MyItem) : Boolean {
      return // comparaison: est-ce la même "entité" ? => même id?
   }

   override fun areContentsTheSame(oldItem: MyItem, newItem: MyItem) : Boolean {
      return // comparaison: est-ce le même "contenu" ? => mêmes valeurs? (avec data class: simple égalité)
   }
}

class ItemListAdapter : ListAdapter<Item, ItemListAdapter.ItemViewHolder>(ItemsDiffCallback) {
   override fun onCreateViewHolder(...)
   override fun onBindViewHolder(...)
}

// Usage is simpler:
val adapter = ItemListAdapter()
recyclerView.adapter = adapter
adapter.submitList(listOf("Item#1", "Item #2"))
```

## ViewBinding

Utiliser le `ViewBinding` ([documentation](https://developer.android.com/topic/li braries/view-binding) / [slides](../../slides/3%20-%20Views.html#9)) dans `TaskListFragment`:

- changez le `inflate` pour récupérer une instance de type `XxxBinding`
- remplacez les `findViewByIds` par des calls direct du genre `binding.myViewId`

Puis faites pareil pour les `ViewHolder`: c'est un peu plus complexe, il faudra changer le constructeur pour qu'il prenne un `val binding: ItemTaskBinding` afin d'y avoir accès dans le corps de la classe et passer `binding.root` au constructeur parent.
