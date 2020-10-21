# TD 5: ViewModel

On va faire un peu de ménage !

## Refactorisation avec TaskListViewModel

Inclure trop de logique dans le fragment est une mauvaise pratique, on va donc refactoriser notre code pour améliorer notre architecture en s'inspirant de:

- [MVVM: Model-View-ViewModel](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel) pour la "Presentation Layer"
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) pour le reste
- [Android Architecture Components](https://developer.android.com/topic/libraries/architecture) pour nous aider des outils spécifiques Android

⚠️ Lisez bien tout le sujet, suivez les étapes et aidez vous du squelette de code plus bas !

Pour résumer, on va déplacer la logique de la gestion de la liste hors du Fragment et dans le ViewModel, qui va simplement interroger le Repository

- Créer une classe `TaskListViewModel` qui hérite de `ViewModel` qui va gérer:  
  - Les `LiveData` qui étaient dans le Repository
  - Le `repository` qui sert de source de données
  - Les coroutines avec `viewModelScope`

- Dans `TaskListAdapter`
  - Rendez la `taskList` publique
  - Donnez lui une valeur par défaut: `emptyList()`

- Dans `TaskListFragment`:
  - Récupérer le `viewModel` grâce à `by viewModels()`
  - Supprimer le `repository` et la `taskList`
  - Observer la valeur de `viewModel.taskList` et mettre à jour la liste de l'`adapter`

- Dans `TasksRepository`, déplacez les `LiveData` dans le `ViewModel`

- Procéder par étapes et inspirez vous de ce squelette (NE COPIEZ PAS TOUT!) pour refactoriser votre app (commencez juste par le chargement de la liste):

```kotlin
// Le Repository récupère les données
class TasksRepository {
    // Le web service requête le serveur
    private val webService = Api.tasksWebService

    suspend fun loadTasks(): List<Task>? {
        val response = webService.getTasks()
        return if (response.isSuccessful) response.body() else null
    }

    suspend fun removeTask(task: Task) {...}
    suspend fun createTask(task: Task) {...}
    suspend fun updateTask(task: Task) {...}
}

// Le ViewModel met à jour la liste de task qui est une LiveData
class TaskListViewModel: ViewModel() {
    private val repository = TasksRepository()
    private val _taskList = MutableLiveData<List<Task>>()
    public val taskList: LiveData<List<Task>> = _taskList

    fun loadTasks() {...}
    fun deleteTask(task: Task) {...}
    fun addTask(task: Task) {...}
    fun editTask(task: Task) {...}
}

// Le Fragment observe la LiveData et met à jour la liste de l'adapter:
class TaskListFragment: Fragment() {
    val adapter = TaskListAdapter()
    private val viewModel: TasksViewModel by viewModels() // On récupère une instance de ViewModel

    // On "abonne" le Fragment aux modifications de l'objet LiveData du ViewModel
    override fun onViewCreated(...) {
        viewModel.taskList.observe(this, Observer { newList ->
            adapter.list = newList.orEmpty()
            adapter.notifyDataSetChanged()
        })
    }

    override fun onResume(...) {
        viewModel.loadTasks()
    }
}

// On donne une valeur par défaut à la liste et on peut la retirer du constructeur:
class TaskListAdapter() : ... {
    var list: List<Task> = emptyList()
}
```

- Vérifier que ça fonctionne
- Pour être sur de ne jamais oublier de notifier l'`adapter`, vous pouvez retirer la ligne du fragment et utiliser une propriété observable:

```kotlin
// L'adapter se notifie automatiquement lui même à chaque fois qu'on modifie sa liste:
var list: List<Task> by Delegates.observable(emptyList()) {_, _, _ ->
    notifyDataSetChanged()
}
```

- Permettre la suppression, l'ajout et l'édition des tasks du serveur avec cette archi
