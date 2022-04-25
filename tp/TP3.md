# TP 3: L'Internet

## Avant de commencer

Les APIs qui nous allons utiliser exigent qu'une personne soit connectée, pour commencer nous allons simuler cela en passant directement un `token` dans les `headers` de nos requêtes `HTTP`:

- Rendez vous sur [https://android-tasks-api.herokuapp.com/api-docs/](https://android-tasks-api.herokuapp.com/api-docs/)
- Ce site permet de lire la documentation et d'utiliser les routes directement
- Cliquez sur `users/sign_up` puis sur "Try it out"
- Vous devriez voir un JSON prérempli dont vous devez remplir les données (vous pouvez mettre des infos bidon) avant de cliquer sur "Execute":

```json
{
  "firstname": "UN PRENOM",
  "lastname": "UN NOM",
  "email": "UN EMAIL",
  "password": "UN MDP",
  "password_confirmation": "LE MEME MDP"
}
```

- Copiez le token généré quelque part (vous pourrez le récupérer à nouveau en utilisant la route `/login`)
- Copiez votre token dans la popup du bouton "Authorize" en haut
- Maintenant que vous êtes "loggé", testez les routes disponibles (création, suppression, etc...)

## Accéder à l'internet

Afin de communiquer avec le réseau internet (wifi, ethernet ou mobile), il faut ajouter la permission dans le fichier `AndroidManifest`, juste au dessus de la balise `application`

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

## Ajout des dépendances

Dans le fichier `app/build.gradle`:

- Dans `dependencies {...}`, ajouter les dépendances qui vous manquent (mettre les versions plus récentes si l'IDE vous le propose):

```groovy
  // Retrofit
  implementation 'com.squareup.retrofit2:retrofit:2.9.0'
  implementation 'com.squareup.okhttp3:logging-interceptor:5.0.0-alpha.3'

  // KotlinX Serialization
  implementation 'org.jetbrains.kotlinx:kotlinx-serialization-json:1.3.2'
  implementation 'com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter:0.8.0'

  // Coroutines
  implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.0'
  implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.0'

  // Lifecycle
  implementation 'androidx.lifecycle:lifecycle-extensions:2.2.0'
  implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.4.0'
  implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.4.0'
```

- Tout en haut ajoutez le plugin de sérialisation:

```groovy
plugins {
    // ...
    id 'org.jetbrains.kotlin.plugin.serialization' version "$kotlin_version"
}
```

Après tout cela vous pouvez cliquer sur "Sync Now" pour que l'IDE synchronise le projet.

En cas de soucis à ce moment là, vérifiez que:

- Android Studio est à jour ("Check for updates")
- Le Plugin Kotlin est à jour (`Settings > Plugins > Installed > Kotlin`)
- votre `kotlin_version` est récente, il doit être défini en haut de `<project>/.build.gradle` comme ceci (si ce n'est pas le cas, ajoutez le):

```groovy
buildscript {
    ext {
        kotlin_version = "1.6.0"
    }
// ...
```

## Retrofit

- Créer un package `network` qui contiendra les classes en rapport avec les échanges réseaux
- Créer un `object Api` (ses membres et méthodes seront donc `static`):

```kotlin
object Api {
  private const val TOKEN = "COPIEZ_VOTRE_TOKEN_ICI"

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
    }

    // instance retrofit pour implémenter les webServices:
    Retrofit.Builder()
      .baseUrl("https://android-tasks-api.herokuapp.com/api/")
      .client(okHttpClient)
      .addConverterFactory(jsonSerializer.asConverterFactory("application/json".toMediaType()))
      .build()
    }
  }
}
```

<aside class="positive">

Ici je vous donne tout ce code de config car ce n'est pas très intéressant à chercher mais prenez quelques minutes pour lire et comprendre ce qu'il fait avant de copier-coller!

</aside>

## UserInfo

Exemple de json renvoyé par la route `/info`:

```json
{
  "email": "email",
  "firstname": "john",
  "lastname": "doe"
}
```

Créer la `data class` `UserInfo`:

```kotlin
@Serializable
data class UserInfo(
  @SerialName("email")
  val email: String,
  @SerialName("firstname")
  val firstName: String,
  @SerialName("lastname")
  val lastName: String
)
```

<aside class="positive">

Regardez bien les annotations ici (tout ce qui commence par `@`): elle servent à délimiter les éléments à parser pour la lib `KotlinX Serialization`

</aside>

## UserWebService

- Créez l'interface `UserWebService` pour requêter les infos de l'utilisateur (importez `Response` avec `alt + enter` et choisissez la version `retrofit`):

```kotlin
interface UserWebService {
  @GET("users/info")
  suspend fun getInfo(): Response<UserInfo>
}
```

<aside class="positive">

`Response` est un type qui "encapsule" une réponse HTTP: on peut y retrouver un code de réponse, un message d'erreur, etc... et un résultat: ici une instance de `UserInfo`

</aside>

- Utilisez retrofit pour créer une implémentation de ce service:

```kotlin
object Api { 
  // ...
  val userWebService : UserWebService by lazy {
    retrofit.create(UserWebService::class.java)
  }
}
```

<aside class="positive">

Ici, Retrofit va créer une implémentation de l'interface `UserWebService` pour nous, en utilisant d'une part les valeurs de base configurées dans `Api` et d'autre part les annotations qui lui donnent le type de requête (ex: `GET`), la route, les types de paramètres, etc.

</aside>

## Affichage

- Dans le layout qui contient la liste, ajoutez une `TextView` tout en haut (vous devrez probablement régler un peu les contraintes)
- Overrider la méthode `onResume` pour y récupérer les infos de l'utilisateur, en ajoutant cette ligne, une erreur va s'afficher mais ne paniquez pas, on va s'en occuper:

```kotlin
// Ici on ne va pas gérer les cas d'erreur donc on force le crash avec "!!"
val userInfo = Api.userWebService.getInfo().body()!!
```

- La méthode `getInfo()` étant déclarée comme `suspend`, vous aurez besoin de la lancer dans un `CouroutineScope` (c'est ce que dit le message d'erreur): on va utiliser directement `lifeCycleScope` qui est un `CouroutineScope` déjà défini et géré par le système dans les `Activity` et `Fragment`

```kotlin
lifecycleScope.launch {
  mySuspendMethod()
}
```

<aside class="positive">

**Remarque:** En général ce scope sert plutôt à ce qui est visuel (ex: lancer une animation)
On utilisera ensuite un autre scope: `viewModelScope` qui est fourni par android dans les `ViewModel`, mais pour l'instant on implémente tout dans les fragments comme des 🐷

</aside>

- Afficher les données dans votre `TextView`:

```kotlin
userInfoTextView.text = "${userInfo.firstName} ${userInfo.lastName}"
```

➡️ Lancez l'app et vérifiez que vos infos s'affichent !

<aside class="negative">

⚠️ Sur émulateur, à cette étape il y a parfois des crashes étranges:

- "`...EPERM (operation not permitted)...`": désinstallez l'application de l'émulateur et relancez
- L'app stoppe direct et sans stacktrace: redémarrer l'émulateur et vérifiez que son wifi est bien connecté

</aside>

## TaskListFragment

Il est temps de récupérer les tâches depuis le serveur !

Créer un nouveau service `TaskWebService`:

```kotlin
interface TasksWebService {
  @GET("tasks")
  suspend fun getTasks(): Response<List<Task>>
}
```

- Utiliser l'instance de retrofit comme précédemment pour créer une instance de `TasksWebService` dans l'objet `Api`
- Modifier `Task` pour la rendre "serializable" par KotlinX Serialization (inspirez vous de `UserInfo`)

<aside class="negative">

⚠️ Ici vous aurez probablement un soucis car on a fait hériter `Task` de `Serializable` mais une des annotations de KotlinX Serialisation s'appelle aussi `Serializable`: pour résoudre ce conflit, faites hériter explicitement de `java.io.Serializable` à la place

</aside>

## TasksListViewModel

<aside class="positive">

`ViewModel` est une classe du framework Android qui permet de gérer les données d'une vue, et dont on peut facilement créer et récupérer une instance, en général chacune associée à une `Activity` ou un `Fragment`

On va donc y déplacer une partie de la logique: dans l'idéal l'`Activity` ou le `Fragment` doit seulement s'occuper de passer les évènements (comme les clics) au VM

</aside>

Créer la classe `TasksListViewModel`, avec une liste de tâches _Observable_ grâce aux type `StateFlow` et `MutableStateFlow`:

```kotlin
class TasksListViewModel : ViewModel() {
  private val webService = Api.tasksWebService

  // privée mais modifiable à l'intérieur du VM: 
  private val _tasksStateFlow = MutableStateFlow<List<Task>>(emptyList())
  // même donnée mais publique et non-modifiable à l'extérieur afin de pouvoir seulement s'y abonner:
  public val tasksStateFlow: StateFlow<List<Task>> = _tasksStateFlow.asStateFlow()

  suspend fun refresh() {
      viewModelScope.launch {
          val response = webService.getTasks() // Call HTTP (opération longue)
          if (response.isSuccessful) { // à cette ligne, on a reçu la réponse de l'API
            Log.e("Network", "Error: ${response.message()}")
          }
          val fetchedTasks = tasksResponse.body()!!
          _tasksStateFlow.value = fetchedTasks // on modifie le flow, ce qui déclenche ses observers
      }
  }

  suspend fun create(...)
  suspend fun update(...)
  suspend fun delete(...)
}
```

## "Collecter" le Flow

Dans `TaskListFragment`, à l'aide du squelette de code plus bas:

- Ajouter en propriété une instance de `TaskListViewModel`
- Dans `onResume()`, utilisez ce VM pour rafraîchir la liste de tasks
- Dans `onViewCreated()`, "abonnez" le fragment aux changements du `StateFlow` du VM et mettez à jour la liste et l'`adapter` dans la lambda de retour

<aside class="negative">

⚠️ Attention ici au moment de choisir l'import de `.collect` sélectionnez bien celui qui est présenté avec des accolades: `collect {...}`

</aside>

```kotlin
private val viewModel: TaskListViewModel by viewModels()

// Dans onResume()
viewModel.refresh() // on demande de rafraîchir les données sans attendre le retour directement

// Dans onViewCreated()
lifecycleScope.launch { // on lance une coroutine car `collect` est `suspend`
    viewModel.tasksStateFlow.collect { newList ->
      // cette lambda est executée à chaque fois que la liste est mise à jour dans le VM
      // -> ici, on met à jour la liste dans l'adapter
    }
}
```

## Compléter TasksWebService

Modifier `TasksWebService` et ajoutez y les routes manquantes:

```kotlin
@POST("tasks")
suspend fun create(@Body task: Task): Response<Task>

@PATCH("tasks/{id}")
suspend fun update(@Body task: Task, @Path("id") id: String = task.id): Response<Task>

// Inspirez vous d'au dessus et de la doc de l'API pour compléter:
@...(...)
suspend fun delete(@...(...) id: String): Response<Unit>
```

## Suppression, Ajout, Édition

- Inspirez vous du fonctionnement de `refresh()` pour ajouter toutes les autres actions avec le serveur dans le VM, par ex pour l'édition:

```kotlin
suspend fun update(task: Task) {
    viewModelScope.launch {
      val response = ... // TODO: appel réseau
      if (!response.isSuccessful) return

      val updatedTask = response.body()!!
      _tasksStateFlow.value = _tasksStateFlow.value - task + updatedTask
    }
}
```

- Vous pouvez supprimer la `taskList` locale dans le Fragment et vérifier que vous avez bien tout remplacé par des appels au VM (et donc au serveur)
