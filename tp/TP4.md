# TP 4: Refactorisation avec ViewModel

## Principe

Inclure trop de logique dans le fragment est une mauvaise pratique, on va donc refactoriser notre code pour améliorer notre architecture en s'inspirant de:

- [MVVM: Model-View-ViewModel](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel) pour la "Presentation Layer"
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) pour le reste
- [Android Architecture Components](https://developer.android.com/topic/libraries/architecture) pour nous aider des outils spécifiques Android

<aside class="negative">

⚠️ Lisez bien tout le sujet, suivez les étapes et surtout aidez vous du squelette de code plus bas !
</aside>

<aside class="positive">

Pour résumer, on va déplacer la logique de la gestion de la liste du Fragment vers le ViewModel, qui va pour sa part simplement interroger le Repository et gérer son `StateFlow`.
</aside>

## Instructions

- Créer une classe `TaskListViewModel` qui hérite de `ViewModel` et qui va gérer:

  - Les `StateFlow` qui étaient dans le Repository
  - Le `repository` qui sert de source de données
  - Les coroutines avec `viewModelScope`

- Dans `TaskListAdapter`: Si vous ne l'avez pas fait à ce stade, transformez votre `RecyclerView.Adapter` pour hériter de `ListAdapter` (cf fin du TP 1)

- Dans `TaskListFragment`:

  - Récupérer le `viewModel` grâce à `by viewModels()`
  - Supprimer le `repository` et la `taskList`
  - Observer la valeur de `viewModel.taskList` et mettre à jour la liste de l'`adapter`

- Dans `TasksRepository`, déplacez les `StateFlow` dans le `ViewModel`

- Procéder petit à petit et inspirez vous de ce squelette (NE COPIEZ PAS TOUT!) pour refactoriser votre app (commencez juste par le chargement de la liste):

## Squelette de code

```kotlin
// Le Repository récupère les données
class TasksRepository {
    // Le web service requête le serveur
    private val webService = Api.tasksWebService

    suspend fun refresh(): List<Task>? {
        val response = webService.getTasks()
        if (!response.isSuccessful) {
            Log.e("TasksRepository", "Error while fetching tasks: ${response.message()}")
            return null
        }
        return response.body()
    }

    suspend fun delete(task: Task) : Boolean {}
    suspend fun createOrUpdate(task: Task) : Task? {}
}

// Le ViewModel met à jour la liste de task qui est un StateFlow
class TaskListViewModel: ViewModel() {
    private val repository = TasksRepository()
    private val _taskList = MutableStateFlow<List<Task>>(emptyList())
    public val taskList: StateFlow<List<Task>> = _taskList

    fun refresh() {
        viewModelScope.launch { ... }
    }
    fun delete(task: Task) {...}
    fun addOrEdit(task: Task) {...}
}

// Le Fragment observe la StateFlow et met à jour la liste de l'adapter:
class TaskListFragment: Fragment() {
    val adapter = TaskListAdapter()
    // On récupère une instance de ViewModel
    private val viewModel: TasksViewModel by viewModels()

    // On écoute l'objet StateFlow du ViewModel ici:
    override fun onViewCreated(...) {
        lifecycleScope.launch {
            viewModel.taskList.collect { newList ->
                // utliser la liste
            }
        }
    }

    override fun onResume(...) {
        viewModel.refresh()
    }
}
```

## Pour terminer

- Vérifier que ça fonctionne !
- Permettre la suppression, l'ajout et l'édition des tasks du serveur avec cette archi

<!-- garder le repo pareil, passer le flow au VM (+ faire un orderBy ?, ServiceLocator pour virer les activityForResult -->