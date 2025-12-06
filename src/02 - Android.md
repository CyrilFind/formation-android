---
marp: true
---

<!-- headingDivider: 2 -->

# Android

![bg](../assets/jetpack.svg)

## Intro

![bg right:30% 50%](../assets/android.svg)

- Nombreux utilisateurs
- Devices très différents
- Versions d’OS anciennes
- Play Store
- Puissance limitée
- Phone, Tablet, TV, Watch, Auto, Chrome, Windows, ...
- Dev natif en Kotlin et Java

## Android Studio

![bg right:50% 100%](../assets/android_studio.png)

- IDE dédié
- Développé par Jetbrains (IntelliJ)
- Navigation projet
- "Sync Now"
- Logcat
- Émulateurs
- SDK Manager
- strings.xml
- Refactoring
- RAM 🔥

## Éléments d'une app Android

![bg right:40% 80%](../assets/android_elements.png)

- Scripts Gradle: build logic
  - minSdk, compileSdk, targetSdk
  - implementations, libs TOML
  - versionCode, versionName
- AndroidManifest.xml
- App
- Activity
- Fragment
- Layouts XML
- Components

## App Components

![bg right:40% 160%](../assets/app_components.png)

- Activity / Fragments ➡ Screen Controller
- Service ➡ Headless Controller
- Broadcast Receiver ➡ Event Listener
- ContentProvider ➡ Shared Data API

## Android Studio: Démo

![bg right:50% 100%](../assets/android_studio.png)

## iOS

![bg right:40% 80%](../assets/apple.svg)

- Beaucoup d'utilisateurs aux US
- Plus de 💰 dépensés
- Moins de devices différents
- OS mis à jour plus rapidement
- App Store
- Swift (interop Objective-C)
- XCode 💩
- Simulator

## Xcode: Démo

![bg right:40% 80%](../assets/xcode.png)

## Composants et Cross-Platform

![bg right:30% 90%](../assets/react.png)
![bg right:30% 70%](../assets/flutter.svg)

- Permet de coder une seule fois
- Souvent à base de "Components" (à la React)
- Désavantage: performances, UX, possibilités spécifiques ou récentes des OS
- Xamarin, ReactNative, NativeScript, Ionic, ...
- Dart: Flutter (iOS, Android, Desktop, Web) par Google

## Composants natifs

![bg right:30% 90%](../assets/compose.png)
![bg right:30% 75%](../assets/swiftui.png)

- Swift: SwiftUI par Apple
- Kotlin: Jetpack Compose sur Android, Desktop, Web et même iOS par JetBrains et Google
