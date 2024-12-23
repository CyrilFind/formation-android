---
marp: true
---

<!-- headingDivider: 2 -->

# Architecture

![bg](../assets/jetpack.svg)

## MVP

Model View Presenter
![bg right:60% 95%](../assets/mvp.png)

# MVVM

Model View ViewModel
![bg right:60% 90%](../assets/mvvm.png)

## MVI

Model View Intent
![bg right:60% 90%](../assets/mvi.png)

⚠️ Ici `Intent` n'est pas le type spécifique à Android

💡 Ceci s'adapte encore plus directement avec Jetpack Compose

## Layers

![bg right:60% 95%](../assets/layers.png)

## Dependency Rule

![bg right:60% 95%](../assets/dependency.png)

## Clean Architecture

![bg right:70% 95%](../assets/clean_arch.png)

## Google Architecture

![bg right:70% 90%](../assets/google_arch.png)

## ViewModel

- Formate les données pour l'UI
- Survit aux "configuration changes"
- Peut aussi partager des données entre Fragments
- Fait partie de la "lifecycle library" mais ré-implémentable
- Ne pas passer de Context (si besoin, étendre AndroidViewModel)

Analogie: Serveur

## Repository

- Pas un Architecture Component mais une bonne pratique
- Récupère les données d'une ou plusieurs `DataSource`
- Choisis la source en fonction des circonstances
- Synchronise les sources
- Présente les données

Analogie: Cuisine

## Compose

![state bg right:30% 90%](../assets/compose_state.png)

- Similaire: MVVM / MVI
- Inspirations de React ?

[Documentation](https://developer.android.com/develop/ui/compose/architecture)
