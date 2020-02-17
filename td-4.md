# TD 4: L'Internet

## Avant de commencer

Les APIs qui nous allons utiliser exigent qu'une personne soit connectée, dans ce TD nous allons simuler que la personne est connectée, en passant un `token` dans les `headers` de nos requêtes HTTP.

- Nous allons utiliser ce site: [https://android-tasks-api.herokuapp.com/api-docs/index.html](https://android-tasks-api.herokuapp.com/api-docs/index.html)
- Lisez la documentation de l'API: le site permet d'utiliser ses routes directement
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

- Copiez le token généré quelquepart (vous pourrez le récuperer à nouveau en utilisant la route `/login`)
- Copiez votre token dans la popup du bouton "Authorize" en haut
- Maintenant que vous êtes "loggés", testez les routes disponibles (création, suppression, etc...)


## Accèder à l'internet

Afin de communiquer avec le réseau internet (wifi, ethernet ou mobile), il faut ajouter la permission dans le fichier `AndroidManifest`, juste après la balise `<manifest...>`

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

## Ajout des dépendances

Dans le fichier `app/build.gradle`, ajouter : 

```groovy
  implementation "com.squareup.retrofit2:retrofit:2.6.2"
  implementation 'com.squareup.retrofit2:converter-moshi:2.6.2'
  implementation "com.squareup.moshi:moshi:1.8.0"
  implementation "com.squareup.moshi:moshi-kotlin:1.8.0"
  implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.2.0-rc03"
  implementation "org.jetbrains.kotlinx:kotlinx-coroutines-core:1.3.2"
  implementation "androidx.lifecycle:lifecycle-runtime-ktx:2.2.0-rc03"
  implementation "org.jetbrains.kotlin:kotlin-reflect:1.1.0"
```

## Retrofit

- Vous pouvez créer un package `network` qui contiendra les classes en rapport avec les échanges réseaux
- Créer un `object` `Api` (ses membres et méthodes seront donc `static`)
- Ajoutez y les constantes qui serviront à faire les requêtes:

```kotlin
object Api {
  private const val BASE_URL = "https://android-tasks-api.herokuapp.com/api/"
  private const val TOKEN = "COPIEZ_VOTRE_TOKEN_ICI"
}
```

- Créer une instance de [Moshi](https://github.com/square/moshi) pour parser le JSON renvoyé par le serveur:

```kotlin
object Api {
  // ...
  private val moshi = Moshi.Builder().build()
}
```

- Créer le client HTTP en ajoutant un intercepteur pour ajouter le `header` d'authentification avec votre `Token`:

```kotlin
object Api {
  // ...
  private val okHttpClient by lazy {
    OkHttpClient.Builder()
      .addInterceptor { chain ->
        val newRequest = chain.request().newBuilder()
          .addHeader("Authorization", "Bearer $TOKEN")
          .build()
        chain.proceed(newRequest)
      }
      .build()
  }
}
```

- Créer une instance de retrofit qui permettra d'implémenter les interfaces que nous allons créer ensuite:

```kotlin
object Api {
  // ...
  private val retrofit = Retrofit.Builder()
    .baseUrl(BASE_URL)
    .client(okHttpClient)
    .addConverterFactory(MoshiConverterFactory.create(moshi))
    .build()
}
```

### UserService

- Créez l'interface `UserService` pour requêter les infos de l'utilisateur (importez `Response` avec <kbd>alt + enter</kbd> et choisissez la version `retrofit`):

```kotlin
interface UserService {
    @GET("users/info")
    suspend fun getInfo(): Response<UserInfo>
}
```

- Utilisez retrofit pour créer une implémentation de ce service (grace aux annotations):

```kotlin
object Api {
  // ...
  val userService: UserService by lazy { retrofit.create(UserService::class.java) }
}

```

### UserInfo

Exemple de json renvoyé par la route `/info`:

```json
{
  "email": "email",
  "firstname": "john",
  "lastname": "doe"
}
```

Créer la `data class` `UserInfo` avec des annotations Moshi pour récupérer ces données:

```kotlin
data class UserInfo(
    @field:Json(name = "email")
    val email: String,
    @field:Json(name = "firstname")
    val firstName: String,
    @field:Json(name = "lastname")
    val lastName: String
)
```

### Affichage

- Dans `fragment_task_list.xml`, ajoutez une `TextView` au dessus de la liste de tâche si vous n'en avez pas
- Overrider la méthode `onResume` pour y récuperer les infos de l'utilisateur, une erreur va s'afficher mais ne paniquez pas, on va s'en occuper:

```kotlin
// Ici on ne va pas gérer les cas d'erreur donc on force le crash avec "!!"
val userInfo = Api.userService.getInfo().body()!! 
```

- La méthode `getInfo()` étant déclarée comme `suspend`, vous aurez besoin de la lancer dans un `couroutineScope`.
Pour cela on peut utiliser `GlobalScope`, mais une meilleure façon est d'en créer un "vrai" pour pouvoir le `cancel()` après:

```kotlin
// Création:
private val coroutineScope = MainScope()
// Utilisation:
coroutineScope.launch {...}
// Suppression dans onDestroy():
coroutineScope.cancel()
```

- Afficher les données dans votre `TextView`

```kotlin
    my_text_view.text = "${userInfo.firstName} ${userInfo.lastName}"
```

- Lancez l'app et vérifiez que vos infos s'affichent ! 

#### Remarques:
- En réalité, vous n'avez pas besoin de faire la création et la suppression, si vous utiliser directement `lifeCycleScope`
-  Un autre scope est fourni par android: `viewModelScope`, mais pour l'instant on implémente tout dans les fragments comme des 🐷

## TaskListFragment

Il est temps de récuperer les tâches depuis le serveur !

- Créer un nouveau service `TaskWebService`

```kotlin
interface TasksWebService {
    @GET("tasks")
    suspend fun getTasks(): Response<List<Task>>
}
```

- Utiliser l'instance de retrofit comme précédemment pour créer une instance de `TasksWebService` dans l'objet `Api`

- Modifier `Task` pour la rendre lisible par Moshi (i.e. faire comme pour `UserInfo`)

## TasksRepository

Le Repository va chercher des data dans une ou plusieurs sources de données (ex: DB locale et API distante)

Créer la classe `TasksRepository`avec:

- une propriété `tasksWebService` pour les requêtes avec `Retrofit`
- une propriété `taskList` *publique* de type `LiveData<List<Task>>`: représente une liste de tâche *Observable* (on peut donc s'*abonner* à ses modifications)
- une propriété `_taskList` *privée* de type `MutableLiveData<List<Task>>` qui représente la même donnée mais modifiable donc utilisable à l'intérieur du repository
- une méthode publique `refresh` qui requête la liste et met à jour la `LiveData`


```kotlin
class TasksRepository {
    private val tasksWebService = Api.tasksWebService 
    
    private val _taskList = MutableLiveData<List<Task>>()
    public val taskList: LiveData<List<Task>> = _taskList

    suspend fun refresh() {
        val tasksResponse = taskWebService.getTasks()
        if (tasksResponse.isSuccessful) {
            val fetchedTasks = tasksResponse.body()
            tasks.postValue(fetchedTasks)
        }
    }

```

## LiveData
 Dans `TaskListFragment`:
- Ajouter en propriété une instance de `TasksRepository`
- Dans `onViewCreated()`, "abonnez" le fragment à la  `LiveData` du repository
- Mettez à jour la liste et l'`adapter` avec le résultat (importer le `Observer` de la lib `lifecycle`)
- Dans `onResume()`, utilisez le repository pour rafraîchir la liste de tasks


```kotlin
private val tasksRepository = TasksRepository()
private val tasks = mutableListOf<Task>()

// Dans onViewCreated()
tasksRepository.taskList.observe(this, Observer {
	  tasks.clear()
	  tasks.addAll(it)
	  adapter.notifyDataSetChanged()
})

// Dans onResume()
lifecycleScope.launch {
    tasksRepository.refresh()
}
```

## Compléter TasksWebService

Modifier `TasksWebService` et ajoutez y les routes suivantes:

```kotlin
@DELETE("tasks/{id}")
suspend fun deleteTask(@Path("id") id: String?): Response<String>

@POST("tasks")
suspend fun createTask(@Body task: Task): Response<Task>

@PATCH("tasks/{id}")
suspend fun updateTask(@Body task: Task, @Path("id") id: String? = task.id): Response<Task>
```

## Suppression, Ajout, Édition

- Inspirez vous du fonctionnement de `refresh()` pour ajouter toutes les autres actions avec le serveur dans le Repository, par ex pour l'édition:

```kotlin
 todoRepository.updateTask(task)?.let { task ->
    val editableList = _tasksListLiveData.value.orEmpty().toMutableList()
    val position = editableList.indexOfFirst { task.id == it.id }
    editableList[position] = task
    _tasksListLiveData.value = editableList
}
```

- Utilisez les dans le Fragment, par ex pour la suppression:

```kotlin
adapter.onDeleteClickListener = { task ->
    lifecycleScope.launch {
        tasksRepository.delete(task)
    }
}
```
