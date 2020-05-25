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

## Étapes: 
- Commencez par une liste linéaire moche avec juste les noms et seulement la première page de l'API
- Changez en grille avec une même image par défaut pour toutes les cellules (une pokéball par ex)
- Ajoutez la vue détail: vous devrez faire une requête pour chaque espèce
- Ajoutez la pagination avec les [PagedList](https://developer.android.com/topic/libraries/architecture/paging/ui) de la [Paging Library](https://developer.android.com/topic/libraries/architecture/paging)
- Afficher les bonnes images et les infos de base dans les cellules
- Vous pouvez utilisez les ViewModel partagés (cf fin du td-7.md <sup>(*)</sup> ) pour éviter de multiplier les requête HTTP
- Finissez par le "cochage"

## Aller plus loin:
- Essayez de faire quelque chose de joli cette fois: [Un exemple pour vous inspirer](https://www.instagram.com/p/Bx86mp2hWT-/)
- la plupart des améliorations du td-8.md peuvent aussi s'appliquer
- La BD locale peut également servir à économiser des requêtes en stockant les infos en local (sachant que les donnée ne changent pas souvent)
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
