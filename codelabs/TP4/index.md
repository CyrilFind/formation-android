---
id: TP4
source: tp/TP4.md
duration: 0

---

# TP 4: ViewModel




## Refactorisation avec TaskListViewModel



Inclure trop de logique dans le fragment est une mauvaise pratique, on va donc refactoriser notre code pour améliorer notre architecture en s'inspirant de:

*  [MVVM: Model-View-ViewModel](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel) pour la "Presentation Layer"
*  [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) pour le reste
*  [Android Architecture Components](https://developer.android.com/topic/libraries/architecture) pour nous aider des outils spécifiques Android

⚠️ Lisez bien tout le sujet, suivez les étapes et aidez vous du squelette de code plus bas !

Pour résumer, on va déplacer la logique de la gestion de la liste hors du Fragment et dans le ViewModel, qui va simplement interroger le Repository

* Créer une classe `TaskListViewModel` qui hérite de `ViewModel` et qui va gérer:

* Les `LiveData` qui étaient dans le Repository
* Le `repository` qui sert de source de données
* Les coroutines avec `viewModelScope`
* Dans `TaskListAdapter`: Si vous ne l'avez pas fait à ce stade, transformez votre `RecyclerView.Adapter` pour hériter de `ListAdapter` (cf fin du TP 1)
* Dans `TaskListFragment`:

* Récupérer le `viewModel` grâce à `by viewModels()`
* Supprimer le `repository` et la `taskList`
* Observer la valeur de `viewModel.taskList` et mettre à jour la liste de l'`adapter`
* Dans `TasksRepository`, déplacez les `LiveData` dans le `ViewModel`
* Procéder petit à petit et inspirez vous de ce squelette (NE COPIEZ PAS TOUT!) pour refactoriser votre app (commencez juste par le chargement de la liste):

```language-kotlin
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

    fun loadTasks() {
        viewModelScope.launch { ... }
    }
    fun deleteTask(task: Task) {...}
    fun addTask(task: Task) {...}
    fun editTask(task: Task) {...}
}

// Le Fragment observe la LiveData et met à jour la liste de l'adapter:
class TaskListFragment: Fragment() {
    val adapter = TaskListAdapter()
    // On récupère une instance de ViewModel
    private val viewModel: TasksViewModel by viewModels() 

    // On écoute l'objet LiveData du ViewModel ici:
    override fun onViewCreated(...) {
        viewModel.taskList.observe(viewLifecycleOwner) { newList ->
            // utliser la liste
        }
    }

    override fun onResume(...) {
        viewModel.loadTasks()
    }
}
```

* Vérifier que ça fonctionne !
* Permettre la suppression, l'ajout et l'édition des tasks du serveur avec cette archi


