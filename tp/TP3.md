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

Afin de communiquer avec le réseau internet (wifi, ethernet ou mobile), il faut ajouter la permission dans le fichier `AndroidManifest`, juste après la balise `manifest`

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

## Ajout des dépendances

Dans le fichier `app/build.gradle`:

- Dans `dependencies {...}`, ajouter les dépendances qui vous manquent (mettre les versions plus récentes si l'IDE vous le propose):

```groovy
  // Retrofit
  implementation 'com.squareup.retrofit2:retrofit:2.+'
  implementation 'com.squareup.okhttp3:logging-interceptor:5.+'

  // KotlinX Serialization
  implementation "org.jetbrains.kotlinx:kotlinx-serialization-json:1.+"
  implementation 'com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter:0.8.+'

  // Coroutines
  implementation "org.jetbrains.kotlinx:kotlinx-coroutines-core:1.+"
  implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.+"

  // Lifecycle
  implementation "androidx.lifecycle:lifecycle-extensions:2.+"
  implementation "androidx.lifecycle:lifecycle-runtime-ktx:2.+"
  implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.+"
```

<aside class="negative">

L'IDE va râler, et à raison, car on devrait utiliser des versions spécifiques (ex: `2.1.0`) mais c'est pour être sûr d'avoir les dernières versions majeures disponibles chaque année
</aside>

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
- votre `kotlin_version` est récente (doit être défini en haut de `<project>/.build.gradle`, à l'heure où j'écris c'est `1.5.31`)

## Retrofit

- Créer un package `network` qui contiendra les classes en rapport avec les échanges réseaux
- Créer un `object Api` (ses membres et méthodes seront donc `static`):

```kotlin
object Api {

  // constantes qui serviront à faire les requêtes
  private const val BASE_URL = "https://android-tasks-api.herokuapp.com/api/"
  private const val TOKEN = "COPIEZ_VOTRE_TOKEN_ICI"

  // client HTTP
  private val okHttpClient by lazy {
    OkHttpClient.Builder()
      .addInterceptor { chain ->
        // intercepteur qui ajoute le `header` d'authentification avec votre token:
        val newRequest = chain.request().newBuilder()
          .addHeader("Authorization", "Bearer $TOKEN")
          .build()
        chain.proceed(newRequest)
      }
      .build()
  }

  // sérializeur JSON: transforme le JSON en objets kotlin et inversement
  private val jsonSerializer = Json {
      ignoreUnknownKeys = true
      coerceInputValues = true
  }

  // instance de convertisseur qui parse le JSON renvoyé par le serveur:
  private val converterFactory =
      jsonSerializer.asConverterFactory("application/json".toMediaType())

  // permettra d'implémenter les services que nous allons créer:
  private val retrofit = Retrofit.Builder()
    .baseUrl(BASE_URL)
    .client(okHttpClient)
    .addConverterFactory(converterFactory)
    .build()
}
```

<aside class="positive">

Ici je vous donne tout ce code de config car ce n'est pas très intéressant à chercher mais prenez quelques minutes pour lire et comprendre ce qu'il fait
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

Créer la `data class` `UserInfo` avec des annotations de KotlinX Serialization pour récupérer ces données:

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

## UserWebService

- Créez l'interface `UserWebService` pour requêter les infos de l'utilisateur (importez `Response` avec `alt + enter` et choisissez la version `retrofit`):

```kotlin
interface UserWebService {
  @GET("users/info")
  suspend fun getInfo(): Response<UserInfo>
}
```

- Utilisez retrofit pour créer une implémentation de ce service:

```kotlin
object Api {
  // ...
  val userWebService by lazy {
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

- La méthode `getInfo()` étant déclarée comme `suspend`, vous aurez besoin de la lancer dans un `CouroutineScope` (c'est ce que dit le message d'erreur):

  on va utiliser directement `lifeCycleScope` qui est un `CouroutineScope` déjà défini et géré par le système dans les `Activity` et `Fragment`

```kotlin
lifecycleScope.launch {
  mySuspendMethod()
}
```

- Afficher les données dans votre `TextView`:

```kotlin
userInfoTextView.text = "${userInfo.firstName} ${userInfo.lastName}"
```

<aside class="negative">

⚠️ Sur émulateur, à cette étape il y a parfois des crashes étranges:

- "`...EPERM (operation not permitted)...`": désinstallez l'application de l'émulateur et relancez
- L'app stoppe direct et sans stacktrace: redémarrer l'émulateur et vérifiez que son wifi est bien connecté

</aside>

➡️ Lancez l'app et vérifiez que vos infos s'affichent !

<aside class="positive">

**Remarque:** Un autre scope est fourni par android: `viewModelScope`, mais pour l'instant on implémente tout dans les fragments comme des 🐷
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
- Modifier `Task` pour la rendre lisible par KotlinX Serialization (i.e. faire comme pour `UserInfo`)

## TasksRepository

Le but d'un Repository est d'exposer des data venant d'une ou plusieurs sources de données (ex: DB locale et API distante)

Créer la classe `TasksRepository`:

```kotlin
class TasksRepository {
  private val tasksWebService = Api.tasksWebService

  // Ces deux variables encapsulent la même donnée:
  // [_taskList] est modifiable mais privée donc inaccessible à l'extérieur de cette classe
  private val _taskList = MutableLiveData<List<Task>>()
  // [taskList] est publique mais non-modifiable:
  // On pourra seulement l'observer (s'y abonner) depuis d'autres classes
  public val taskList: LiveData<List<Task>> = _taskList

  suspend fun refresh() {
      // Call HTTP (opération longue):
      val tasksResponse = tasksWebService.getTasks()
      // À la ligne suivante, on a reçu la réponse de l'API:
      if (tasksResponse.isSuccessful) {
          val fetchedTasks = tasksResponse.body()
          // on modifie la valeur encapsulée, ce qui va notifier ses Observers et donc déclencher leur callback
          _taskList.value = fetchedTasks
      }
  }
}

```

## LiveData

Dans `TaskListFragment`:

- Ajouter en propriété une instance de `TasksRepository`
- Dans `onViewCreated()`, "abonnez" le fragment à la `LiveData` du repository
- Mettez à jour la liste et l'`adapter` avec le résultat (importer le `Observer` de la lib `lifecycle`)
- Dans `onResume()`, utilisez le repository pour rafraîchir la liste de tasks

```kotlin
private val tasksRepository = TasksRepository()

// Dans onViewCreated()
tasksRepository.taskList.observe(viewLifecycleOwner) { list ->
  // mettre à jour la liste dans l'adapteur
}

// Dans onResume()
lifecycleScope.launch {
  tasksRepository.refresh()
}
```

## Compléter TasksWebService

Modifier `TasksWebService` et ajoutez y les routes suivantes:

```kotlin
@DELETE("tasks/{id}")
suspend fun deleteTask(@Path("id") id: String?): Response<Unit>

@POST("tasks")
suspend fun createTask(@Body task: Task): Response<Task>

@PATCH("tasks/{id}")
suspend fun updateTask(@Body task: Task, @Path("id") id: String? = task.id): Response<Task>
```

## Suppression, Ajout, Édition

- Inspirez vous du fonctionnement de `refresh()` pour ajouter toutes les autres actions avec le serveur dans le Repository, par ex pour l'édition (les autres sont plus simples):

```kotlin
suspend fun updateTask(task: Task) {
  // TODO appel réseau et récupérationd de la tache:
  val updatedTask = ...
  // version "mutable" de la liste actuelle:
  val mutableList = _tasksList.value.orEmpty().toMutableList()
  // position actuelle de l'élément:
  val position = editableList.indexOfFirst { updatedTask.id == it.id }
  // modification de la liste mutable:
  editableList[position] = updatedTask
  // mise à jour de la livedata pour notifier les observers:
  _tasksList.value = editableList
}
```

- Utilisez les méthodes du repository dans le Fragment, par ex pour la suppression:

```kotlin
adapter.onClickDelete = { task ->
  lifecycleScope.launch {
      tasksRepository.delete(task)
  }
}
```
