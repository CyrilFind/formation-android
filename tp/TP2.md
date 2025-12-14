# TP 2 - Jetpack Compose

## Compose Activity

<aside class="negative">

⚠️ Ne créez pas un nouveau projet, le but est que vous ayez un seul rendu à m'envoyer à la fin !

</aside>

- Créez une nouvelle activity "Empty Activity" (en compose cette fois) appelez la `ComposeActivity`
- L'IDE devrait automatiquement compléter `app/build.gradle.kts` pour configurer Compose (buildFeatures, dependencies, etc) et l'ajouter au `AndroidManifest.xml`
- Adaptez votre `AndroidManifest` pour en faire notre activity principale à la place de l'ancienne, et relancez l'app pour vérifier: il faut déplacer `<intent-filter>...</intent-filter>` de l'ancienne activity à la nouvelle
- Renommez `Greeting` en `ListScreen` et `GreetingPreview` en `ListPreview` et supprimez l'argument `name`

Vous devriez avoir quelque chose comme ça:

```kotlin
class ComposeActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        //...
        setContent {
            TodoTheme {
                ListScreen()
            }
        }
    }
}
```

<aside class="positive">

🧑‍🏫 `setContent` sert ici de "point d'entrée" à Compose: il va chercher une `ComposeView` dans le layout de votre `Activity`, et en créer une sinon

Ensuite `TodoTheme` est une fonction `@Composable` qui applique un thème Material Design à tout ce qui est à l'intérieur (couleurs, typographie, etc...)

Puis `ListScreen` : votre premier écran Compose, que vous allez maintenant implémenter

</aside>

- Personnalisez un peu votre Theme en fonction de votre projet perso !

<aside class="positive">

En haut à droite de votre éditeur, il devrait y avoir trois icônes qui permettent d'alterner entre mode texte, mode visuel, et les 2 ensemble: "Split", je vous conseille ce mode Split pour afficher vos `@Preview` sans avoir à relancer l'app à chaque fois.

![split](/assets/editor_modes.png)

</aside>

- affichez une liste d'éléments avec Compose (utilisez `LazyColumn` et `items`), avec des éléments, c'est légerement plus simple qu'une `RecyclerView` 🙃 :

```kotlin
LazyColumn{
    items(100) {
        Text(text = "Item #$it")
    }
}
```

- Lancez l'app et essayez de scroller la liste: attention, on ne voit pas les contours de la liste, mais elle ne prends pas toute la largeur actuellement donc le scroll ne marche que si on scroll précisément sur les textes !
- Pour régler ça, ajoutez un `Modifier.fillMaxWidth()` à la `LazyColumn`
- Ajoutez un `Modifier.padding(16.dp)` à la `LazyColumn` pour ajouter un peu d'espace autour
- Essayez à nouveau de scroller, vous devriez pouvoir le faire aussi en dehors des textes maintenant
- Espacez un peu les éléments de la liste en lui passant `verticalArrangement = Arrangement.spacedBy(8.dp)` comme argument
- Personnalisez un peu l'affichage comme vous le souhaitez (couleurs, taille de texte, ...)

<aside class="negative">

⚠️ Attention quand vous importez la class `Color` dans du Compose, il y a plusieurs choix, choisissez bien la version avec `compose` dans le nom de package et qui s'écrivent en "TitleCase" pas en "UPPERCASE":

```kotlin
val blue = Color.Blue // Compose
val green = Color.GREEN // Views
```

</aside>

## Remember

On va maintenant ajouter un peu d'interactivité sur notre liste.

- Ajoutez une variable `items` en haut de `ListScreen`:

```kotlin
var items by remember { mutableStateOf(List(100) { "Item #$it" }) }
```

- faites les imports suggérés par l'IDE

<aside class="positive">

🧑‍🏫 Il se passe pas mal de chose sur cette seule ligne:

- `remember`: Une fonction `@Composable` peut être _recomposée_ (en gros: ré-exécutée) à tout moment donc on ne peut pas utiliser de variables simples car elles seraient remises à leur valeur de départ en permanence, on utilise donc diverses formes de `remember` qui permettent à nos variables de survivre aux recompositions.
- `mutableStateOf` crée une variable de type `MutableState<T>` qui est un "wrapper" autour de la valeur initiale et qui permet d'observer les changement de valeur et de déclencher des recompositions automatiquement.
- le mot clé de _délégation_ `by` qui permet de ne pas avoir à écrire `items.value` ou `items.value = ...` partout dans le code, mais juste `items` ou `items = ...` directement, grâce à l'import des fonctions d'extension `getValue` et `setValue` définies pour `MutableState<T>`, et au fait qu'on a utilisé `var` (sinon seul le `getValue` serait délégué)

</aside>

- Modifiez la liste pour qu'elle utilise cette variable `items` au lieu de la liste statique: attention il faudrait importer une autre fonction `items` qui prend directement une `List<T>` au lieu d'un `Int` (l'IDE devrait vous proposer l'import automatiquement mais parfois il confond les 2)
- lancez l'app: ça devrait fonctionner pareil
- Remplacez vos items en `String` par des `data class Task` et ajoutez la description:

```kotlin
items(items) { task ->
  Column {
    Text(text = task.title)
    Text(text = task.description)
  }
}
```

- lancez l'app pour vérifier que tout s'affiche correctement

## Scaffold

On va utiliser des éléments de "Material Design 3" pour améliorer un peu l'interface facilement.

- Modifiez `ListScreen` pour qu'elle utilise un `Scaffold`, avec une `TopAppBar` (acceptez de "Opt-in à ExperimentalMaterial3Api") avec le titre de votre choix
- et un `FloatingActionButton` avec une icône "Add"
- passez le innerPadding du `Scaffold` à la `LazyColumn` pour que le contenu ne soit pas caché par la `TopAppBar`

```kotlin
Scaffold(
    modifier = Modifier.fillMaxSize(),
    topBar = { TopAppBar(title = { Text(/* title */) }) },
    floatingActionButton = {
        FloatingActionButton(onClick = { /* TODO */ }) {
          Icon(imageVector = Icons.Default.Add, contentDescription = "Add")
        }
    }
) {
    LazyColumn() {
        // ...
    }
}
```

<aside class="positive">

🧑‍🏫 Ici on utilise ce qu'on appelle des **Slots**: des fonctions Compose qu'on passe en argument d'autres fonctions compose via des **lambda**

Par exemple `Scaffold` permet de placer un composant en haut (topBar), un en bas (bottomBar), un bouton flottant (floatingActionButton), etc...

Et juste après on va utiliser `actions` pour ajouter un bouton dans la `TopAppBar` (qui est défini avec un `RowScope`, donc on peut y ajouter plusieurs éléments à la suite ils seront placés horizontalement).

![slots](/assets/compose_slots.png)

</aside>

- Lancez l'app pour vérifier que tout s'affiche correctement

## Ajout d'éléments

On va maintenant implémenter l'ajout d'éléments à la liste.

- Implémentez le clic sur le `FloatingActionButton` pour ajouter un nouvel élément à la liste comme précédemment mais en Compose:

```kotlin
onClick = {
    val newItem = Task(title = "Item #${items.size}")
    items = items + newItem
}
```

- Lancez l'app et testez l'ajout d'éléments: vous devriez voir la liste se mettre à jour automatiquement mais il faut scroller jusqu'en bas pour voir le nouvel élément
- Pour améliorer ça, utilisez le `LazyListState` pour scroller automatiquement jusqu'en bas:
- Ajoutez un `val listState = rememberLazyListState()` en haut de `ListScreen`
- Passez le `listState` à la `LazyColumn` avec `state = listState`
- Modifiez le `onClick` du `FloatingActionButton` pour scroller jusqu'en bas après avoir ajouté l'élément avec `listState.animateScrollToItem(items.size - 1)`

<aside class="negative">

⚠️ Une erreur va s'afficher car la définition de `animateScrollToItem` contient un mot clé `suspend`:

il sert à signifier que cette fonction ne peut pas s’exécuter comme une fonction normale car elle peut potentiellement bloquer le thread courant en prenant beaucoup de temps à se terminer

Afin de compiler, il faudra donc l'appeler dans le contexte d'un `CouroutineScope` (ou dans une autre fonction `suspend`)

</aside>

- Ajoutez un `val coroutineScope = rememberCoroutineScope()` en haut de `ListScreen`

```kotlin
coroutineScope.launch {
  // suspend function
}
```

<aside class="positive">

**Remarque:** C'est le scope qu'on va utiliser pour ce qui se passe dans l'UI Compose.
Dans une UI en Views classique on a `lifeCycleScope`

En général ce scope sert plutôt à ce qui est visuel (ici lancer une animation est un bon exemple)

On utilise souvent un autre scope: `viewModelScope` qui est fourni par android dans les `ViewModel`, pour la logique plus "intelligente" de l'app: faire des requêtes HTTP par exemple.

</aside>

- Lancez l'app et testez à nouveau l'ajout d'éléments: cette fois la liste devrait scroller automatiquement jusqu'au nouvel élément ajouté

## Suppression d'éléments

Ajoutez un bouton de suppression dans chaque élément et faites sorte qu'il fonctionne
Pour avoir un item avec le texte à gauche et le bouton tout à droite vous pouvez utiliser une `Row` avec `horizontalArrangement = Arrangement.SpaceBetween` ou bien un `Spacer(modifier = Modifier.weight(1f))` entre les 2 éléments.

## Navigation

On va d'abord permettre de naviguer vers notre ancienne `MainActivity`:

- Ajoutez une flèche dans les `actions` de la top bar:

```kotlin
IconButton(onClick = {...}) {
  Icon(
      imageVector = Icons.AutoMirrored.Filled.ArrowForward,
      contentDescription = "go to classic app"
  )
}
```

- Implémentez le clic pour naviguer vers l'ancienne `MainActivity`:

```kotlin
val intent = Intent(context, MainActivity::class.java)
context.startActivity(intent)
```

<aside class="positive">

🧑‍🏫 On crée ici un simple **Intent explicite** et on l'utilise pour naviguer

</aside>

Pour récupérer un `Context` on utilise un `CompositionLocal`:

```kotlin
val context = LocalContext.current
```

- Lancez l'app et testez la navigation vers l'ancienne activity

Maintenant on va utiliser la bibliothèque `Navigation3` pour gérer la navigation de manière plus propre:

- renseignez vous sur [la doc officielle](https://developer.android.com/guide/navigation/navigation-3)
- Ajoutez les dépendances nécessaires dans `app/build.gradle.kts`: [doc](https://developer.android.com/guide/navigation/navigation-3/get-started#project-setup)
- Créez un nouveau fichier DetailScreen.kt avec une fonction `@Composable` `DetailScreen(task: Task)` qui affiche les détails d'une tâche
- Utilisez l'IDE pour extraire `ListScreen` dans un autre fichier également
- Dans `ComposeActivity`, au lieu d'afficher directement `ListScreen`, créez et utilisez un composant `App()`:
- Gardez le Scaffold dans `ListScreen` sans la topBar: déplacez là dans un autre Scaffold que vous ajouterez dans `App()` pour qu'elle soit commune à tous les écrans
- Modifiez `ListScreen` pour qu'au clic sur un élément, on navigue vers `DetailNavScreen`

```kotlin
@Serializable
data object ListNavScreen : NavKey
@Serializable
data class DetailNavScreen(val task: Task) : NavKey

@Composable
fun App() {
    // on créé notre historique de navigation avec la liste comme écran initial
    val backStack = rememberNavBackStack(ListNavScreen)

    NavDisplay(
      backStack = backStack,
      entryProvider = entryProvider {
        entry<ListNavScreen> { ListScreen(onClickItem = {...}) }
        entry<DetailNavScreen> { key -> DetailScreen(task = key.task) }
      }
    )
}
```

- Extraire un composant `TaskItem` pour la partie qui affiche chaque item et faire en sorte qu'au clic sur un item, on remonte un event onClick qui permettra de naviguer vers l'écran détail:

```kotlin
@Composable
private fun TaskItem(
    modifier: Modifier = Modifier,
    item: Task,
    onClick: (Task) -> Unit,
    onDelete: () -> Unit,
) {...}
```

<aside class="positive">

🧑‍🏫 **Modifiers**

Par convention, chaque composant doit avoir un argument `modifier` de type `Modifier` avec comme valeur par défaut....`Modifier` !

`Modifier` est une interface dont le `companion object` implémente... `Modifier`

C'est assez simple en vérité: ça permet d'utilier `Modifier` comme point de départ et valeur par défaut: c'est un modifier qui ne fait rien.

Ensuite plein de différentes implémentations de `Modifier` existent et sont configurés de façon à pouvoir s'enchaîner comme ceci et ajouter des comportements ou des modifications visuelles:

```kotlin
Modifier.fillMaxSize(0.5f)
    .padding(8.dp)
    .clickable { }
```

⚠️ l'argument `modifier` de chaque Composant doit toujours être utilisé dans le composant "root" qui le constitue, par exemple:

```kotlin
@Composable
fun Login(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier // on insére le modifier à la racine
            .padding(8.dp) // et on peut aussi ajouter des modifiers dessus
    ) {
        TextField(/* ... */)
        TextField(/* ... */)
    }
}
```

</aside>

- Dans `App()`, faites en sorte que ce clic navigue bien:

```kotlin
// Pour naviguer vers l'écran détail, on l'ajoute à l'historique:
backStack.add(DetailNavScreen(...))
```

- Ajoutez un bouton "OK" dans `DetailScreen` qui permet de revenir en arrière:

```kotlin
// Pour revenir en arrière, on enlève le dernier écran de l'historique:
backStack.removeLastOrNull()
```
