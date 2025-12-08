# TP 1 - Classic Views

## Objectif

implémenter un écran affichant une liste de tâches et permettre de créer des nouvelles tâches.

<aside class="negative">

⚠️ Lisez toutes les questions: souvent vous bloquez simplement parce que vous n'avez pas encore regardé l'étape suivante ou le sujet dans son ensemble.

**Sinon, demandez moi!!**

</aside>

<aside class="positive">

Remarque: si vous n'avez pas bien paramétré votre IDE, relisez le début du TP0

</aside>

<aside class="negative">

Si vous remarquez des erreurs, des fautes de frappe ou des oublis de ma part, n'hésitez pas à me le signaler SVP !

</aside>

## Créer un projet

Vous allez créer un unique projet que vous mettrez à jour au fur à mesure des TPs:

- Créer un nouveau projet avec une `Empty VIEWS Activity` (⚠️ pas `Empty Activity` SVP ⚠️)
- Donnez lui un nom personnalisé comme `TodoNicolasAlexandre` (⚠️ pas `TP1` SVP ⚠️)
- Choisissez un package name unique de ce genre: `com.something.todo` (ce sera la racine de tous vos packages et sert d'identifiant unique d'application)
- Minimum API Level: laissez la valeur proposée par défaut
- Initialisez un projet git et faites un commit initial

<aside class="negative">

⚠️ Le projet va évoluer au cours des TP donc faites des commits régulièrement: à chaque étape et au minimum à la fin de chaque TP

Comme dans un vrai projet professionnel, vous allez parfois supprimer et remplacer des parties de code: ne commentez pas votre code dans tous les sens car les commits garderons l'historique et je noterai la "propreté" du code à la fin !

</aside>

## Image Asset Studio

Créez une icône d'application personnalisée avec l'outil intégré **Image Asset Studio**: ouvrez le **Resource Manager** à gauche, près du volet projet puis cliquez sur le `+` en haut à gauche et choisissez `Image Asset`: ici vous pouvez choisie une couleur de fond, une image: icône système ou personnalisée avec un SVG ou un "clipart" (bibliotheque d'icones en cliquant sur la petite icon android) et générer automatiquement les différentes tailles nécessaires pour les différentes version d'Android.

<aside class="negative">

N'y passez pas trop de temps, mais profitez en pour réfléchir à votre projet perso et si vous ave une idée, faites une icône en rapport !

</aside>

Vérifiez que l'icône est bien prise en compte dans le `AndroidManifest.xml` (attribut `android:icon` de la balise `application`) et en lançant l'app.

## Gestion des fichiers

📁 Les fichiers source Java ou Kotlin sont rangés en "packages":

- notés en haut de chaque classe: `package com.nicoalex.todo.nomdupackage`
- répliqués en tant que dossiers dans le filesystem: `com/nicoalex/todo/nomdupackage`

<aside class="positive">

Dans le volet "Projet" à gauche, vous pouvez choisir diverses visualisations de vos fichiers: la plus adaptée pour nous est "Android" qui affiche facilement le Manifest, les fichiers source, les fichier resources (`res`), compacte les dossiers vides ensemble (`com.nicoalex.todo`): tout ce qui est utile spécifiquement pour Android...

Mais il peut parfois être pratique de passer en "Project Files" par ex pour voir l'arborescence réelle et certains fichiers qui sont cachés en vue "Android".

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

- Créer le layout associé `fragment_task_list.xml` dans `res/layout`

<aside class="positive">

vous pouvez aussi utiliser Android Studio pour créer les 2 fichiers à la fois: `Clic droit sur le package > New > Fragment > Fragment (Blank)`, mais la classe sera remplie de plein de code inutile -> supprimez-le

</aside>

- Dans `TaskListFragment`, overrider la méthode `onCreateView(...)`: commencez à taper `onCrea...` et utilisez l'auto-completion de l'IDE pour vous aider (vous pouvez supprimer la ligne `super.onCreateView(...)`)
- On aura besoin ensuite d'overrider `onViewCreated(...)` aussi, faites le maintenant de la même façon, vous devriez avoir quelque chose comme ça:

```kotlin
class TaskListFragment : Fragment() {
    override fun onCreateView(...): View {
       // ici on crée la vue et on la retourne (regardez le type de retour: `View`), on ne fait rien d'autre.
    }

    override fun onViewCreated(...) {
       // ici la vue est créée, on peut récupérer des références aux vues et les manipuler
    }
}
```

- Cette méthode vous demande de **retourner** la `rootView` à afficher: créez la à l'aide de votre nouveau layout comme ceci:

```kotlin
val rootView = inflater.inflate(R.layout.fragment_task_list, container, false)
```

<aside class="negative">

⚠️ Si vous exécutez du code **avant** cette ligne `inflate`, il va crasher ou ne rien faire car votre vue n'existera pas encore

</aside>

<aside class="positive">

`R` est un raccourci signifiant "Resource": c'est une classe générée automatiquement à partir des dossiers et fichiers créés dans `res` qui s'utilise comme ceci: `R.string.app_name`, `R.drawable.app_icon`, etc... afin de récupérer des ID que l'on utilise dans les fonctions du framework Android (`getString`, `getDrawable`, etc...) grace aux noms des resources (pour les fichiers ce sera toujours le nom du fichier sans l'extension)

</aside>

- Pour l'instant, la liste des tâches sera simplement une liste de `String` locale, ajoutez la en tant que propriété de votre classe `TaskListFragment`:

```kotlin
private val taskList = listOf("Task 1", "Task 2", "Task 3")
```

<aside class="positive">

↳ Ici le **Typage Statique Inféré** de Kotlin nous permet de ne pas préciser le type de `taskList`: le compilateur le devine tout seul (et l'IDE devrait vous l'afficher en grisé)

</aside>

## MainActivity

Cette activity va servir de conteneur de fragments:

Dans `activity_main.xml`, remplacez la balise `TextView` par celle ci et adaptez:

```xml
 <androidx.fragment.app.FragmentContainerView
    android:name="com.nicoalex.todo.list.TaskListFragment"
    android:id="@+id/fragment_container"
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

⚠️ C'est normal que l'IDE nous signale un problème ici, on le réglera plus tard

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

- ajoutez lui un `id`: soit en mode visuel soit en mode code, en vous aidant de l'auto-complétion `android:id="@+id/id_de_votre_recycler_view`

- Dans `TaskListFragment`, overridez `onViewCreated` pour y récupérez une référence à la `RecyclerView` du layout en utilisant `findViewById`:

```kotlin
val recyclerView = view.findViewById<RecyclerView>(R.id.id_de_votre_recycler_view)
```

- Pour fonctionner, `recyclerView` a une propriété `adapter` qui doit être connectée à l'adapter que vous avez créé (`null` par défaut)

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
private val taskList = listOf(
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

Retournez dans le code, récupérez une référence à votre nouveau bouton et utilisez `.setOnClickListener {}` pour ajouter une tâche à votre liste à chaque fois qu'on clique dessus:

```kotlin
// Instanciation d'un objet task avec des données préremplies:
val newTask = Task(id = UUID.randomUUID().toString(), title = "Task ${taskList.size + 1}")
taskList = taskList + newTask
```

<aside class="negative">

↳ vous allez devoir changer `taskList` en `var` car actuellement le `val` signifie que la variable est immuable (ne peut pas être réassignée) donc ça ne compilera pas.

On pourrait aussi garder `val` mais utiliser une structure de données mutable: `MutableList`, dans ce cas la variable ne change pas mais c'est son **contenu** qui change.

</aside>

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

## Scroll

- Faites maintenant une liste de 100 éléments pour tester le scroll:

```kotlin
private val taskList = List(100) { index ->
    Task(id = "id_$index", title = "Task $index")
}
```

- Vous pouvez tester avec 1000 ou 10.000 éléments aussi: ça doit rester fluide !
- remettez 100 éléments pour la suite: mainteant si vous ajoutez un élément, vous ne le verrez pas forcément !
- faites en sorte que le `RecyclerView` scrolle automatiquement en bas à chaque ajout de tâche: `recyclerView.scrollToPosition(...)`

## ViewBinding

Utiliser le `ViewBinding` ([documentation](https://developer.android.com/topic/libraries/view-binding) / [slides](../../slides/3%20-%20Views.html#9)) dans `TaskListFragment`:

- changez le `inflate` pour récupérer une instance de type `XxxBinding`
- remplacez les `findViewByIds` par des calls direct du genre `binding.myViewId`

Puis faites pareil pour les `ViewHolder`: c'est un peu plus complexe, il faudra changer le constructeur pour qu'il prenne un `val binding: ItemTaskBinding` afin d'y avoir accès dans le corps de la classe et passer `binding.root` au constructeur parent.

## Suppression d'une tache

Dans le layout de vos item, ajouter un `ImageButton` qui servira à supprimer la tâche associée. Vous pouvez utiliser par exemple l'icône `@android:drawable/ic_menu_delete`

<aside class="positive">

🧑‍🏫 Une [lambda](https://kotlinlang.org/docs/reference/lambdas.html) est un type de variable qui contient un bloc de code pouvant prendre des arguments et retourner un résultat

C'est donc une fonction que l'on peut utiliser comme une variable !

</aside>

Aidez vous des lignes de code plus bas pour réaliser un "Click Listener" à l'aide d'une lambda en suivant ces étapes:

- Dans l'adapter, ajouter une propriété `onClickDelete` de type lambda qui prends en arguments une `Task` et ne renvoie rien: `(Task) -> Unit` et l'initier à `{}` (elle ne fait rien par défaut)
- Utilisez cette lambda dans le `onClickListener` du bouton supprimer
- Dans le fragment, accéder à `onClickDelete` depuis l'adapter et implémentez là: donnez lui comme valeur une lambda qui va supprimer la tache passée en argument de la liste

- Déclaration de la variable lambda dans l'adapter, par défaut elle ne fait rien (`{}`):

```kotlin
var onClickDelete: (Task) -> Unit = {}
```

- Utilisation de la lambda dans le ViewHolder, quand on clique sur le bouton:

```kotlin
onClickDelete(task)
```

- "implémentation" de la lambda dans le fragment, pour que la lambda aie un effet on lui écrit un comportement et on l'assigne à la variable:

```kotlin
myAdapter.onClickDelete = { task ->
    // Supprimer la tâche
}
```

## DetailFragment

- Créez un formulaire simple dans `DetailFragment` en utilisant un `ConstraintLayout` (vous pouvez "convert" dans le menu du clic droit sur la root view) avec deux `EditText` (pour le titre et la description) et un `Button` de validation
- Dans `DetailFragment`, récupérez les références aux vues et implémentez le clic
- Personnalisez un peu l'UI si vous le souhaitez

<aside class="positive">

En haut à droite de votre éditeur, il devrait y avoir trois icônes qui permettent d'alterner entre mode texte, mode visuel, et les 2 ensemble: "Split", je sais qu'on aime le code 🤓 mais je vous conseille le mode visuel qui est plus simple pour manipuler les contraintes ou au moins le mode Split pour afficher la Preview sans avoir à relancer l'app à chaque fois.

![split](/assets/editor_modes.png)

</aside>

## Ajout de tâche complet

<aside class="positive">

Afin de récupérer un résultat de cette nouvelle Activity, nous allons utiliser le fragmentManager qui permet de naviguer et communiquer entre fragments.

Il fonctionne à base de "transactions" qui permettent d'effectuer plusieurs actions à la fois et de les "commiter" (valider) en une seule fois

Ici on utilisera une version simplifiée avec `commit { ... }` fournie par fragment-KTX qui permet d'avoir automatiquement le commit à la fin de la lambda de transaction.

</aside>

- vérifiez que vous avez les dépendances nécessaires (les dernières versions au moment où j'écris sont les suivantes):

- Dans `app/build.gradle.kts` > `dependencies {...}`, ajoutez les dépendances qui vous manquent (mettre les versions plus récentes si l'IDE vous le propose, il vous proposera également de facilement les passer dans le fichier centralisé `libs.versions.toml`):

```gradle
implementation("androidx.fragment:fragment:1.8.9")
implementation("androidx.fragment:fragment-ktx:1.8.9")
```

- Faire en sorte de lancer le nouveau fragment depuis le bouton + du 1er

```kotlin
parentFragmentManager.commit {
    replace<DetailFragment>(R.id.fragment_container)
    addToBackStack(null)
}
```

- Afin de pouvoir recevoir le résultat de `DetailFragment`, créez un `FragmentResultLauncher` dans `TaskListFragment`:

- Vérifiez que vous naviguez bien vers l'écran en cliquant sur + et qu'il s'affiche correctement

```kotlin
class DetailFragment : Fragment() {
    override fun onViewCreated(...) {
        // ...
        parentFragmentManager.setFragmentResultListener(REQUEST_KEY) { _, bundle ->
            val result = bundle.getString(RESULT_KEY)
            // Utilisez le résultat ici
        }
    }

    companion object { // pour définir des membres "statiques", ici des constantes:
        const val REQUEST_KEY = "request_key"
        const val RESULT_KEY = "result_key"
    }
```

- Sur votre bouton de validation créez une nouvelle task:

```kotlin
val newTask = Task(id = UUID.randomUUID().toString(), title = "New Task !")
```

- et passez la en résultat au fragment parent avant de fermer le fragment:

```kotlin
parentFragmentManager.setFragmentResult(BlankFragment.REQUEST_KEY, Bundle().apply {
  putString(BlankFragment.RESULT_KEY, newTask)
})
parentFragmentManager.popBackStack() // retour au fragment précédent
```

- ça ne compilera pas car `Task` ne fait pas partie des types de base autorisés dans un bundle !
- L'un de ces types est `Serializable`: Faites donc hériter `Task` de `java.io.Serializable`, comme c'est une `data class`, il n'y a rien à implémenter !

- Dans le FragmentResultListener de votre 1er fragment, récupérez cette task:

```kotlin
val task = result.data?.getSerializableExtra("task") as Task?
```

- et ajoutez la à la liste, comme vous le faisiez avec le bouton d'ajout précédemment

<aside class="negative">

La syntaxe `as Task` permet de **"caster"** un objet récupéré en tant que `Task`: c'est à dire qu'on force l'objet à être considéré de type `Task`, qui est (depuis l'étape précédente) un sous-type de `Serializable` (retourné par `getSerializableExtra`)

ici on utilise `as Task?` (équivalent à `as? Task`) pour récupérer un **nullable** et éviter d'avoir une exception si le cast ne fonctionne pas en retournant `null` à la place

</aside>

- Vérifiez que la nouvelle tache s'affiche dans la liste

- Pour l'instant notre Task est créée avec des données "en dur", modifiez le code de `DetailFragment` pour récupérer les valeurs entrées par l'utilisateur dans les `EditText` et les utiliser pour créer la nouvelle tâche

## Édition d'une tâche

<aside class="positive">

🧑‍🏫 L'avantage des Fragments est qu'on peut les initialiser avec des arguments contrairement aux Activity (car celles ci doivent être instanciées par le système)

</aside>

Ajoutez un argument taskId de type String?, `null` par défaut (pour garder le cas d'ajout de nouvelle tâche) à `DetailFragment` pour identifier la tâche à éditer, vous pourrez ensuite faire:

```kotlin
parentFragmentManager.commit {
    replace(R.id.fragmentContainerView, DetailFragment(taskId))
    addToBackStack(null)
}
```

Inspirez vous de ce que vous avez fait pour le bouton "supprimer" et le bouton "ajouter" pour créer un bouton "éditer" permettant de modifier chaque tâche en ouvrant l'activité `DetailFragment` pré-remplie avec les informations de la tâche en question.

## Interface et délégation

Pour l'instant on a utilisé des lambda mais une façon plus classique de gérer les clicks d'un item est de définir une interface que l'on implémentera dans le 1er Fragment, mettez à jour votre code pour utiliser cette méthode:

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
    override fun onClickDelete(task: Task) {...}
    override fun onClickEdit(task: Task) {...}
  }
  val adapter = TaskListAdapter(adapterListener)
}
```

## Partager

- En modifiant `AndroidManifest.xml`, ajouter la possibilité de partager du texte **depuis les autres applications** (par ex en surlignant un texte dans un navigateur puis en cliquant sur "partager") et ouvrir le formulaire de création de tâche avec une description pré-remplie ([Documentation](https://developer.android.com/training/sharing/receive))

<aside class="negative">

⚠️ Attention l'Activity concernée devra avoir l'attribut `exported="true"` dans le manifest

</aside>

- En utilisant un `Intent` **implicite**, ajouter la possibilité de partager du texte **vers les autres applications** (avec un `OnLongClickListener` sur les tâches par ex ou bien avec un bouton dans la vue formulaire) ([Documentation](https://developer.android.com/training/sharing/send))

## Changements de configuration

Que se passe-t-il pour votre liste si vous tournez votre téléphone pour passer en mode paysage ? 🤔

- Une façon de régler ce soucis est d'overrider la méthode `onSaveInstanceState`
- Il faudra utiliser `putSerializable` (un peu comme précédemment avec `putExtra`) pour sauvegarder la liste
- Puis pour récupérer cette liste, la méthode `getSerializable` dans `onCreateView` ou `onViewCreated`, sur le paramètre `savedInstanceState`
