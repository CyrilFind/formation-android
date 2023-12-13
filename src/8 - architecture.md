---
marp: true
---

<!-- headingDivider: 2 -->

# Architecture

![bg right:65% 100%](../assets/jetpack.svg)

## MVC

Model View Controller

![bg right:60% 95%](../assets/mvc.png)

## MVP

Model View Presenter
![bg right:60% 95%](../assets/mvp.png)

## Dependency Rule

![bg right:60% 95%](../assets/dependency.png)

## Clean Architecture

![bg right:70% 95%](../assets/clean_arch.png)

# MVVM

Model View ViewModel
![bg right:60% 90%](../assets/mvvm.png)

## MVI

Model View Intent
![bg right:60% 90%](../assets/mvi.png)

⚠️ Ici `Intent` n'est pas le type spécifique à Android

💡 Ceci s'adapte encore plus directement avec Jetpack Compose

## Google Architecture

![bg right:70%](../assets/google_arch.png)

## ViewModel

- Formate les données pour l'UI
- Survis aux configuration changes
- Peut aussi partager des données entre Fragments
- Fait partie lifecycle library
- Ne pas passer de Context (si besoin, étendre AndroidViewModel)

Analogie: Serveur

## Repository

- Pas un Architecture Components mais une bonne pratique
- Récupère les données d'une ou plusieurs `DataSource`
- Choisis la source en fonction des circonstances
- Synchronise les sources
- Présente les données

Analogie: Cuisine

## Compose

https://developer.android.com/jetpack/compose/architecture