# TD 5: ViewModel

On va faire un peu de ménage !

## Refactorisation avec TaskListViewModel

Mettre toute la logique dans le fragment est une mauvaise pratique: les `ViewModel` permettent d'en extraire une partie.

⚠️ Lisez bien tout le sujet et suivez les étapes en vous aidant du squelette de code plus bas !

- Créer une classe `TaskListViewModel` qui hérite de `ViewModel` qui va gérer:  
    - La `taskListLiveData` qui contient la donnée de type `List<Task>` sous forme de `LiveData` et donc *observable*
    - Le `repository` qui sert de source de données
    - Les coroutines avec `viewModelScope`

- Dans `TaskListAdapter`
    - Rendez la `taskList` publique
    - Donnez lui une valeur par défaut: `emptyList()`

- Dans `TaskListFragment`:
    - Récupérer le `viewModel` grâce à `ViewModelProvider`
    - Supprimer le `repository` et la `taskList`
    - Observer la valeur de `viewModel.taskListLiveData` et mettre à jour la liste de l'`adapter`

- Dans `TasksRepository`, 
    - Supprimer les fonctions qui utilisent `coroutineScope`
    - Garder seulement celles qui sont `suspend` et les rendre publiques

- Procéder par étapes et inspirez vous de ce squelette (NE COPIEZ PAS TOUT!) pour refactoriser votre app (commencez juste par le chargement de la liste):

```kotlin
// Repository simplifié, avec seulement des méthodes "suspend"
class TasksRepository {
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
  val taskListLiveData = MutableLiveData<List<Task>?>()
  private val repository = TasksRepository()
  
    fun loadTasks() { 
        viewModelScope.launch { 
            val taskList = repository.loadTasks()
            taskListLiveData.postValue(taskList)
        }
    }
    
    fun editTask(task: Task) {
    viewModelScope.launch { 
            val newTask = repository.updateTask(task)
            if (newTask != null) {
                val newList = taskListLiveData.value.orEmpty().toMutableList()
                val position = newList.indexOfFirst { it.id == newTask.id }
                newList[position] = newTask
                taskListLiveData.postValue(newList)
            }
        }
    } 
    
    fun deleteTask(task: Task) {...} 
    fun addTask(task: Task) {...} 
}

// Le Fragment observe la LiveData et met à jour la liste de l'adapter:
class TaskListFragment: Fragment() {
  val adapter = TaskListAdapter()
  // On récupère une instance de ViewModel
  private val viewModel by lazy {
    ViewModelProvider(this).get(TasksViewModel::class.java)
  }

  // On "abonne" le Fragment aux modifications de l'objet LiveData du ViewModel
  override fun onViewCreated(...) {
    viewModel.taskListLiveData.observe(this, Observer { newList -> 
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
