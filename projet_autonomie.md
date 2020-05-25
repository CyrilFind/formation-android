# Projet en Autonomie

## But: 
Réutiliser ce que vous avez appris en TD pour vous l'approprier.

## Sujet: 
Créer une app "Pokédex", avec les fonctionnalités suivantes:
- Afficher une grille paginée de pokémons avec leurs infos de base: images, noms, numéro, type 1, type 2
- Afficher le détail d'un pokémon avec les autres infos: poids, description, ...(pas obligé de tout mettre)
- Permettre de "cocher" les pokémons que l'on a déjà attrapés en enregistrant l'info localement 

## Documentation:
- [Poké API](https://pokeapi.co/) (ex: GET https://pokeapi.co/api/v2/pokemon-species, GET https://pokeapi.co/api/v2/pokemon-species/27)
- [Paging Library](https://developer.android.com/topic/libraries/architecture/paging)
- [Room Database](https://developer.android.com/topic/libraries/architecture/room)
- Les slides et TDs précédents

## Instructions: 
- Nommez le projet et le package en fonction de votre binome (cf [./td-2.md])
- Utilisez git tout de suite et commitez régulièrement pour pouvoir toujours revenir à une version qui marche ;) (cf td-2.md)
- Essayez de coder "proprement" (pour la syntaxe: <kbd>cmd + alt + L</kbd>)
- Vous pouvez vous mettre par 2 (mais ne vous faites trop carry !) 

## Étapes pour l'appli de base: 
- Commencez par une liste linéaire moche avec juste les noms et seulement la première page de l'API
- Changez en grille avec une même image par défaut pour toutes les cellules (une pokéball par ex)
- Ajoutez la vue détail: vous devrez faire une requête pour chaque espèce
- Afficher les bonnes images dans la liste (en observant le format de l'url dans la réponse de la requête de détails)
- Afficher les infos de base dans la liste: un peu compliqué car on est obligés de faire une requête pour chaque espèce (ce qui est lourd dans une liste mais améliorable plus tard)
- Vous pouvez utilisez les ViewModel partagés (cf fin du td-7.md <sup>(*)</sup> ) pour éviter de multiplier certaines requête HTTP
- Essayez de faire quelque chose de joli cette fois: [Un exemple pour vous inspirer](https://www.instagram.com/p/Bx86mp2hWT-/)

# Ajouter la pagination
- Commencez par utiliser [`ListAdapter`](https://developer.android.com/reference/androidx/recyclerview/widget/ListAdapter) à la place de `RecyclerView.Adapter`: vous devrez implémenter un `ListAdapter.DiffCallback` mais cela simplifie certaines choses que l'on faisait à la main: pas besoin de `notify...Changed`, pas besoin de spécifier le nombre d''items, la liste des données est stockée dans la variable `currentList` et on utilise `adapter.submitList(newList)` pour setter les données
- Ajoutez la pagination en passant votre `ListAdapter` en `PagedListAdapter` 
- Vous devez maintenant lui passer une [PagedList](https://developer.android.com/topic/libraries/architecture/paging/ui): on va utiliser les LiveData donc on va construire cette liste avec `LivePagedListBuilder`:

```kotlin
class MyViewModel : ViewModel() {

    val pagedList = LivePagedListBuilder(object : DataSource.Factory<String, Pokemon>() {
        override fun create(): DataSource<String, Pokemon> {
            return PokemonPageKeyedDataSource(viewModelScope) as DataSource<String, Pokemon>
        }
    }, PER_PAGE).build()

    companion object {
        private const val PER_PAGE = 20
    }
}

// on pourra faire presque comme d'habitude dans le fragment ou l'activity:
viewModel.pagedList.observe(viewLifecycleOwner, Observer {
    pokemonListAdapter.submitList(it)
})
```

- Mais pour que cela fonctionne on a besoin de créer `PokemonPageKeyedDataSource`: 
```kotlin
class PokemonPageKeyedDataSource(private val scope: CoroutineScope) : PageKeyedDataSource<Int, Pokemon>() {

    override fun loadBefore(
        params: LoadParams<Int>,
        callback: LoadCallback<Int, Pokemon>
    ) {
        // on ne fait rien ici car on commence au 1er pokémon et il n'y a rien avant 
        // (ce serait utile pour un feed à la twitter ou facebook)
    }

    override fun loadInitial(
        params: LoadInitialParams<Int>,
        callback: LoadInitialCallback<Int, Pokemon>
    ) {
        // Charger la page 0, utiliser la callback avec la valeur 1 comme "key"
    }

    override fun loadAfter(params: LoadParams<Int>, callback: LoadCallback<Int, Pokemon>) {
        val currentPage = params.key
       // utiliser la valeur de "key" pour requêter la page "currentPage" et utiliser la callback avec currentPage + 1
     }
}
```

- Pour pouvoir faire des requêtes avec des pages, il faut utiliser les "query parameters" permis par l'api:

```kotlin
interface PokemonWebService {
    @GET("pokemon")
    suspend fun getPokemons(@Query("limit") limit: Int, @Query("offset") offset: Int = 0): Response<PokeListResponse>
}

// on pourra l'utiliser comme ceci:
val currentPage = params.key
val itemsPerPage = params.requestedLoadSize
pokeWebService.getPokemons(
    limit = itemsPerPage,
    offset = currentPage * itemsPerPage
)
```

## Aller plus loin:
- Stocker les réponses des requêtes pour ne pas les refaire tout le temps, sachant que les donnée ne changent pas souvent:
    - soit en RAM c'est à dire dans une variable de type `Map<Int, Pokemon>` dans un repository par ex, (plus simple)
    - soit dans une BD locale [Room](https://developer.android.com/topic/libraries/architecture/room) (plus compliqué mais de meilleur qualité car la donnée survie au kill de l'app)
- Ajoutez la possibilité de "cocher" les espèces attrapées (vous pouvez dans l'ordre de de difficulté et de qualité: en RAM, dans les SharedPreference, ou dans Room)
- la plupart des améliorations du td-8.md peuvent aussi s'appliquer
- Ajoutez des fonctionnalités si vous avez des idées, par ex:
    - Une barre de recherche
    - Un filtre par génération
    - ...

## Évaluation:
Comme précédemment, je noterai votre avancée puis je vous aiderai sur les points bloquants et je noterai votre avancement final

<br/>
<br/>
<br/>
<br/>
<sup>(*)</sup> : J'ai simplifié la récupération des ViewModel dans les énoncés:

```kotlin
// Avant
private val viewModel by lazy { ViewModelProvider(this).get(MyViewModel::class.java) }

// Maintenant
private val viewModel: MyViewModel by viewModels()
```
