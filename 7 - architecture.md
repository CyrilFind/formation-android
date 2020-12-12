---
marp: true
---
<!-- headingDivider: 2 -->
<!-- class: invert -->

# Architecture

## MVC

![bg right:70% 95%](assets/mvc.png)

## MVP

![bg right:70% 95%](assets/mvp.png)

## Dependecy Rule

![bg right:70% 95%](assets/dependency.png)

## Clean Architecture

![bg right:70% 95%](assets/clean_arch.png)

# MVVM

![bg right:70%](assets/google_arch.png)

## ViewModel

- Formatte les données pour l'UI
- Survis aux configuration changes
- Peut aussi partager des données entre Fragments
- Fait partie lifecycle library
- Ne pas passer de Context (si besoin, étendre AndroidViewModel)

Analogie: Serveur

## Repository

- Pas un Architecture Components mais une bonne pratique
- Récupère les données d'une ou plusieurs `DataSource`
- Choisis la source en fonction des circonstantces
- Synchronise les sources
- Présente les données

Analogie: Cuisine
