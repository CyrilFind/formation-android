# TP 3: L'Internet

## Mise en place

L'API de Todoist nécessite qu'une personne soit connectée, pour commencer nous allons simuler cela en passant directement un `token` dans les `headers` de nos requêtes `HTTP`:

- Rendez vous sur [todoist.com](https://todoist.com/app)
- Créez un compte, allez dans `Paramètres > Intégrations > Clé API` et copiez la quelque part
- lisez un peu [la doc de l'API](https://developer.todoist.com), il y en a en fait 2: REST (ex: [tasks](https://developer.todoist.com/rest/v2/#tasks)) et Sync (ex: [user](https://developer.todoist.com/sync/v9/#user))
- En utilisant la clé copiée et les exemples de la documentation testez de créer un tache avec `curl` (ou Postman, [httpie](https://httpie.io/), ...)

## Accéder à l'internet

Afin de communiquer avec le réseau internet (wifi, ethernet ou mobile), il faut ajouter la permission dans le fichier `AndroidManifest`, juste au dessus de la balise `application`

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

<aside class="positive">

C'est ici une "install-time permission", car elle n'est pas critique, et donc il n'y a pas besoin de la demander explicitement à l'utilisateur, elle est acceptée à l'installation.

</aside>

## Ajout des dépendances

Dans le fichier `app/build.gradle.kts` (celui du module):

- Dans `dependencies {...}`, ajouter les dépendances qui vous manquent (mettre les versions plus récentes si l'IDE vous le propose, il vous permet également de facilement les passer dans le `libs.versions.toml`):

```groovy
// Retrofit
implementation("com.squareup.retrofit2:retrofit:2.11.0")
implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

// KotlinX Serialization
implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
implementation("com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter:1.0.0")

// Coroutines
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
```

- Tout en haut ajoutez le plugin de sérialisation:

```groovy
plugins {
    id("org.jetbrains.kotlin.plugin.serialization") version "2.0.0"
}
```

- Après tout cela vous pouvez cliquer sur "Sync Now" pour que l'IDE télécharge les dépendances, etc.
- Passez toutes ces dépendances dans libs.versions.toml en vous aidant de l'IDE
- Faites pareil pour le plugin, en utilisant `version.ref = "kotlin"`

## Retrofit

- Créez un package `data`
- Créez y un `object Api` (ses membres et méthodes seront donc `static`):

```kotlin
object Api {
  private const val TOKEN = "COPIEZ_VOTRE_CLE_API_ICI"

  private val retrofit by lazy {
    // client HTTP
    val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.BODY))
        .addInterceptor { chain ->
          // intercepteur qui ajoute le `header` d'authentification avec votre token:
          val newRequest = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer $TOKEN")
            .build()
          chain.proceed(newRequest)
        }
        .build()

    // transforme le JSON en objets kotlin et inversement
    val jsonSerializer = Json {
        ignoreUnknownKeys = true
        coerceInputValues = true
        encodeDefaults = true
    }

    // instance retrofit pour implémenter les webServices:
    Retrofit.Builder()
      .baseUrl("https://api.todoist.com/")
      .client(okHttpClient)
      .addConverterFactory(jsonSerializer.asConverterFactory("application/json".toMediaType()))
      .build()
    }
}
```

<aside class="positive">

Ici je vous donne tout ce code de config car ce n'est pas très intéressant à chercher mais prenez quelques minutes pour lire et comprendre ce qu'il fait avant de copier-coller:

- on crée un client HTTP (avec [OkHttp](https://square.github.io/okhttp/))
- on crée un JSON serializer (avec [KotlinX Serialization](https://github.com/Kotlin/kotlinx.serialization))
- on crée une instance de [Retrofit](https://square.github.io/retrofit/) que l'on configure avec les éléments ci dessus (en adaptant le Serializer en `ConverterFactory`)

</aside>

<aside class="negative">

la syntaxe `val retrofit by lazy { ... }` permet d'initialiser la variable `retrofit` automatiquement la première fois qu'elle sera utilisée

</aside>

## User

Extrait d'un json renvoyé par la route `/sync/v9/user/`:

```json
{
  "email": "example@domain.com",
  "full_name": "john doe",
  "avatar_medium": "https://blablabla/image.jpg"
}
```

Créer la `data class User` correspondante:

```kotlin
@Serializable
data class User(
  @SerialName("email")
  val email: String,
  @SerialName("full_name")
  val name: String,
  @SerialName("avatar_medium")
  val avatar: String? = null
)
```

<aside class="positive">

Regardez bien les annotations ici (tout ce qui commence par `@`): elle servent à la lib `KotlinX Serialization` pour délimiter les éléments à parser et comment, avec les clés passées en argument

</aside>

## UserWebService

- Créez l'interface `UserWebService` pour requêter les infos de l'utilisateur (importez `Response` avec `alt + enter` et choisissez la version `retrofit`):

```kotlin
interface UserWebService {
  @GET("/sync/v9/user/")
  suspend fun fetchUser(): Response<User>
}
```

<aside class="positive">

`Response` est un type qui "encapsule" une réponse HTTP: on peut y retrouver un code de réponse, un message d'erreur, etc... et un résultat: ici une instance de `User`

</aside>

- Utilisez retrofit pour créer une implémentation de ce service:

```kotlin
object Api {
  val userWebService : UserWebService by lazy {
    retrofit.create(UserWebService::class.java)
  }
}
```

<aside class="positive">

Ici, Retrofit va créer une implémentation de l'interface `UserWebService` pour nous, en utilisant d'une part les valeurs de base configurées dans `Api` et d'autre part les annotations (`@`) qui lui donnent le type de requête (ex: `GET`), la route, les types de paramètres, etc.

Utiliser des interfaces est souvent préférables pour pouvoir interchanger facilement les implémentations: par exemple si on change une source de données, une dépendances, etc..

Typiquement dans les Tests Unitaires, on a souvent une "fausse implémentation" qui ne fait pas vraiment de requêtes mais retourne des réponses fixes directement
</aside>

## Affichage

- Dans votre Activity, ajoutez un composant `Text` pour voir les résultats de l'API:

```kotlin
// Ici on ne va pas gérer les cas d'erreur donc on force le crash avec "!!"
val user = Api.userWebService.fetchUser().body()!!
```

<aside class="negative">

⚠️ Une erreur va s'afficher car la définition de `fetchUser` contient un mot clé `suspend`:

il sert à signifier que cette fonction ne peut pas s’exécuter comme une fonction normale car elle peut potentiellement bloquer le thread courant en prenant beaucoup de temps à se terminer

Afin de compiler, il faudra donc l'appeler dans le contexte d'un `CouroutineScope` (ou dans une autre fonction `suspend`)

</aside>

- On va utiliser directement `lifeCycleScope` qui est déjà défini par le framework Android dans les `Activity` et `Fragment`:

```kotlin
lifecycleScope.launch {
  mySuspendMethod()
}
```

<aside class="positive">

**Remarque:** En général ce scope sert plutôt à ce qui est visuel (ex: lancer une animation)
On utilisera ensuite un autre scope: `viewModelScope` qui est fourni par android dans les `ViewModel`, mais pour l'instant on implémente tout au même endroit pour simplifier.

</aside>

- Afficher votre nom d'utilisateur dans le `Text`

➡️ Lancez l'app et vérifiez que vos infos s'affichent !

<aside class="negative">

⚠️ Sur émulateur, à cette étape il y a parfois des crashs étranges:

- "`...EPERM (operation not permitted)...`": désinstallez l'application de l'émulateur et relancez
- L'app stoppe direct et sans stacktrace: redémarrer l'émulateur et vérifiez que son wifi est bien connecté

</aside>

## API REST

Il est temps de récupérer les tâches depuis le serveur !

Créer un nouveau service `TaskWebService`:

```kotlin
interface TasksWebService {
  @GET("/rest/v2/tasks/")
  suspend fun fetchTasks(): Response<List<Task>>
}
```

- Utiliser l'instance de retrofit comme précédemment pour créer une instance de `TasksWebService` dans l'objet `Api`

Extrait d'un json renvoyé par la route `/rest/v2/tasks/`:

```json
[
  {
    "content": "title",
    "description": "description",
    "id": "123456789"
  }
]
```

- Modifier `Task` pour la rendre "serializable" par KotlinX Serialization (inspirez vous de `User`)

<aside class="negative">

⚠️ Ici vous aurez peut être un conflit d'imports car on a précédemment fait hériter `Task` de `Serializable`, et une des annotations de KotlinX Serialization s'appelle aussi `@Serializable`: faites hériter explicitement de `java.io.Serializable` pour lever l’ambiguïté.

</aside>

## TaskListViewModel

<aside class="positive">

`ViewModel` est une classe du framework Android qui permet de gérer les données d'une vue, et dont on peut facilement créer et récupérer une instance, en général chacune associée à une `Activity`, un `Fragment`, ou une `NavEntry`

On va donc y déplacer une partie de la logique: dans l'idéal l'`Activity` ou le `Fragment` doit seulement s'occuper de passer les évènements (comme les clics) au VM, et insérer ce que le VM lui dit d'afficher dans les vues

</aside>

Créer la classe `TaskListViewModel`, avec une liste de tâches _Observable_ grâce au `MutableStateFlow`:

```kotlin
class TaskListViewModel : ViewModel() {
  private val webService = Api.tasksWebService

  public val tasksStateFlow = MutableStateFlow<List<Task>>(emptyList())

  init {
    refresh()
  }

  fun refresh() {
      viewModelScope.launch {
          val response = webService.fetchTasks() // Call HTTP (opération longue)
          if (!response.isSuccessful) { // à cette ligne, on a reçu la réponse de l'API
            Log.e("Network", "Error: ${response.message()}")
            return@launch
          }
          val fetchedTasks = response.body()!!
          tasksStateFlow.value = fetchedTasks // on modifie le flow, ce qui déclenche ses observers
      }
  }

  // à compléter plus tard:
  fun add(task: Task) {}
  fun edit(task: Task) {}
  fun remove(task: Task) {}
}
```

## "Collecter" le Flow

- Dans `ListScreen`, ajouter en a une argument une instance de `TaskListViewModel`
- Dans `NavDisplay`, ajoutez des `entryDecorators` qui vont permettre aux ViewModels de correspondre aux `NavEntry` et créez un ViewModel à passer à `ListScreen` avec `viewModel { }`

```kotlin

NavDisplay(
    //...
    entryDecorators = listOf(
        rememberSaveableStateHolderNavEntryDecorator(),
        rememberViewModelStoreNavEntryDecorator()
    ),
    // ...
    entryProvider = entryProvider {
        entry<ListNavScreen> {
            ListScreen(
              viewModel = viewModel { TaskListViewModel() }
              // ...
            )
        }
        // ...
    }
)

fun ListScreen(
  modifier: Modifier = Modifier,
  viewModel: TaskListViewModel,
)
val tasks = viewModel.tasksStateFlow.collectAsStateWithLifecycle()
```

## Compléter TasksWebService

Modifier `TasksWebService` et ajoutez y les routes manquantes:

```kotlin
@POST("/rest/v2/tasks/")
suspend fun create(@Body task: Task): Response<Task>

@POST("/rest/v2/tasks/{id}")
suspend fun update(@Body task: Task, @Path("id") id: String = task.id): Response<Task>

// Complétez avec les méthodes précédentes, la doc de l'API, et celle de Retrofit:
@...
suspend fun delete(@... id: String): Response<Unit>
```

## Suppression, Ajout, Édition

- Inspirez vous du fonctionnement de `refresh()` pour ajouter toutes les autres actions avec le serveur dans le VM, par ex pour l'édition:

```kotlin
fun update(task: Task) {
  viewModelScope.launch {
    val response = ... // TODO: appel réseau
    if (!response.isSuccessful) {
      Log.e("Network", "Error: ${response.raw()}")
      return@launch
    }

    val updatedTask = response.body()!!
    val updatedList = tasksStateFlow.value.map {
      if (it.id == updatedTask.id) updatedTask else it
    }
    tasksStateFlow.value = updatedList
  }
}
```

- Supprimez la `taskList` locale dans l'écran de la Liste et vérifier que vous avez bien tout remplacé par des appels au VM (et donc au serveur), il ne doit rester plus qu'un seul endroit où vous mettez à jour l'adapter: dans le `.collect { }`
- Bonus: vous pouvez même adapter tout ça à votre écran "Classique" dans les `TaskListFragment` en utilisant le même ViewModel, indices pour commencer:

```kotlin
private val viewModel: TaskListViewModel by viewModels()

// Dans onResume()
viewModel.refresh() // on demande de rafraîchir les données sans attendre le retour directement

// Dans onViewCreated()
lifecycleScope.launch { // on lance une coroutine car `collect` est `suspend`
    viewModel.tasksStateFlow.collect { newList ->
      // cette lambda est exécutée à chaque fois que la liste est mise à jour dans le VM
      // -> ici, on met à jour la liste dans l'adapter
    }
}
```

## À vous de jouer

<aside class="positive">

C'est le moment d'adapter à votre projet perso, inspirez vous de ce qu'on a fait jusqu'ici et demandez moi de vous aider !

</aside>

Comme précédemment, commencez par créer encore une nouvelle Activity Compose et faites d'elle la "main" dans le Manifest.

<aside class="negative">

⚠️ Ne créez pas un nouveau projet, le but est que vous ayez un seul rendu à m'envoyer à la fin !

</aside>

Refaites également un Scaffold avec un bouton dans une TopAppBar qui retourne à `ComposeActivity`
