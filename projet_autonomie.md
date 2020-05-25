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
- Nommez le projet et le package en fonction de votre binome (cf td-2.md)
- Utilisez git tout de suite et commitez régulièrement (cf td-2.md)
- Essayez de coder "proprement" (pour la syntaxe: <kbd>cmd + alt + L</kbd>)
- Vous pouvez vous mettre par 2 (mais ne vous faites trop carry !) 
- N'oubliez pas de commit régulièrement pour pouvoir toujours revenir à une version qui marche ;)

## Étapes pour l'appli de base: 
- Commencez par une liste linéaire moche avec juste les noms et seulement la première page de l'API
- Changez en grille avec une même image par défaut pour toutes les cellules (une pokéball par ex)
- Ajoutez la vue détail: vous devrez faire une requête pour chaque espèce
- Afficher les bonnes images dans la liste (en observant le format de l'url dans la réponse de la requête de détails)
- Afficher les infos de base dans la liste: un peu compliqué car on est obligés de faire une requête pour chaque espèce (ce qui est lourd dans une liste mais améliorable plus tard)
- Vous pouvez utilisez les ViewModel partagés (cf fin du td-7.md <sup>(*)</sup> ) pour éviter de multiplier certaines requête HTTP

## Aller plus loin:
- Essayez de faire quelque chose de joli cette fois: [Un exemple pour vous inspirer](https://www.instagram.com/p/Bx86mp2hWT-/)
- Ajoutez la pagination avec les [PagedList](https://developer.android.com/topic/libraries/architecture/paging/ui) de la [Paging Library](https://developer.android.com/topic/libraries/architecture/paging)
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
