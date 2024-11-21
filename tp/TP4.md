# TP 4: Images, Permissions, Stockage

## Coil

<aside class="positive">

La lib `Coil` permet d'afficher des images depuis une URL de façon efficace en gérant la taille, le cache, etc... (`Picasso` et `Glide` sont également souvent utilisées et assez similaires)

</aside>

- Parcourez rapidement la [documentation de Coil](https://coil-kt.github.io/coil/)
- Ajouter les dépendances nécessaires à `app/build.gradle`: on aura besoin de la lib de base et et de l'extension spécifique pour Jetpack Compose
- Ajouter une `ImageView` qui affichera l'avatar de l'utilisateur dans le layout de la liste (à coté de votre `TextView` par ex)
- Dans `onResume`, récupérez une référence à cette vue puis utilisez Coil pour afficher une image en passant une URL de votre choix, par exemple:

```kotlin
imageView.load("https://goo.gl/gEgYUd")
```

## UserActivity

- Créer un nouveau package `user`
- Créez y une nouvelle activité `UserActivity` et ajoutez la dans le manifest
- Créez son UI en `Compose`:

```kotlin
setContent {
    var bitmap: Bitmap? by remember { mutableStateOf(null) }
    var uri: Uri? by remember { mutableStateOf(null) }
    Column {
        AsyncImage(
            modifier = Modifier.fillMaxHeight(.2f),
            model = bitmap ?: uri,
            contentDescription = null
        )
        Button(
            onClick = {},
            content = { Text("Take picture") }
        )
        Button(
            onClick = {},
            content = { Text("Pick photo") }
        )
    }
}
```

- Lancer cette `Activity` quand on clique sur l'`ImageView` du premier écran (pas besoin de launcher ici car on attends pas de résultat: `startActivity(intent)`)

## Caméra: ActivityResult

<aside class="positive">

Afin de demander au système d'exploitation de prendre une photo, on veut récupérer un ["Activity Result"](https://developer.android.com/training/basics/intents/result), comme précédemment pour la création/édition de tâches, mais cette fois avec un Intent [**implicite**](https://developer.android.com/guide/components/intents-filters#ExampleSend)

Pour les cas d'utilisations très courants, il existe [plusieurs "contrats" prédéfinis](https://developer.android.com/reference/androidx/activity/result/contract/ActivityResultContracts) qui simplifient et cachent l'utilisation des intents, et on peut également [définir nos propres contrats](https://developer.android.com/training/basics/intents/result#custom)

</aside>

- On va donc ici utiliser un nouveau launcher dans le contexte compose (donc la syntaxe est un peu différente) et avec `TakePicturePreview` qui retourne un `Bitmap` (c'est à dire une image stockée dans une variable, pas dans un fichier, donc en qualité limitée):

```kotlin
val takePicture = rememberLauncherForActivityResult(TakePicturePreview()) {
    bitmap = it
}
```

- Utilisez ce launcher quand on clique sur le premier bouton (il y a un import à faire pour l'utiliser sans argument)

## Uploader l'image capturée

- Dans l'interface `UserWebService`, ajouter une nouvelle méthode (cette route n'est pas documentée à ma connaissance donc c'est cadeau):

```kotlin
@Multipart
@POST("sync/v9/update_avatar")
suspend fun updateAvatar(@Part avatar: MultipartBody.Part): Response<User>
```

- Créez une [extension](https://kotlinlang.org/docs/extensions.html) qui va convertir l'image en `MultipartBody.Part` qui permet d'envoyer des fichiers en HTTP:

```kotlin
private fun Bitmap.toRequestBody(): MultipartBody.Part {
    val tmpFile = File.createTempFile("avatar", "jpg")
    tmpFile.outputStream().use { // *use*: open et close automatiquement
        this.compress(Bitmap.CompressFormat.JPEG, 100, it) // *this* est le bitmap ici
    }
    return MultipartBody.Part.createFormData(
        name = "avatar",
        filename = "avatar.jpg",
        body = tmpFile.readBytes().toRequestBody()
    )
}
```

- Dans la callback de `takePicture`, envoyez l'image au serveur avec `updateAvatar`, en convertissant `bitmap` avec `toRequestBody` avant

<aside class="negative">

⚠️ Quand vous n'avez pas accès à `lifecycleScope`, vous pouvez utilisez un scope propre à Compose: `val composeScope = rememberCoroutineScope()`)

</aside>

- Enfin, dans les `onResume` de `TaskListFragment`, afficher l'avatar renvoyé depuis le serveur afin de le voir sur l'écran principal:

```kotlin
imageView.load(user.avatar) {
    error(R.drawable.ic_launcher_background) // image par défaut en cas d'erreur
}
```

## Stockage: Accéder et uploader

On va maintenant permettre à l'utilisateur d'uploader une image enregistrée sur son téléphone

Pour simplifier on utilisera [PhotoPicker](https://developer.android.com/training/data-storage/shared/photopicker)

- Gérez l'uri alors récupérée quasiment comme pour la caméra, vous aurez besoin d'une variante de l'extension précédente pour l'URI:

```kotlin
private fun Uri.toRequestBody(): MultipartBody.Part {
    val fileInputStream = contentResolver.openInputStream(this)!!
    val fileBody = fileInputStream.readBytes().toRequestBody()
    return MultipartBody.Part.createFormData(
        name = "avatar",
        filename = "avatar.jpg",
        body = fileBody
    )
}
```

<aside class="negative">

⚠️ Si vous utilisez un device sur Android 9 ou plus ancien, ça ne va pas fonctionner tout de suite, passez à l'étape suivante

</aside>

## Permissions

Jusqu'ici, vous avez probablement utilisé un Android en version 10 ou plus récente: la gestion de l'accès aux fichiers est simplifiée tant qu'on utilise les dossiers partagés (Images, Videos, etc)
Mais pour gérer les versions plus anciennes, il faut demander la permission `READ_EXTERNAL_STORAGE` avant d'accéder au fichiers:

- ajoutez la permission au `Manifest.xml`:

```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

<!-- new permissions android 13 ! -->

- ajoutez un `launcher` avec le contrat `RequestPermission()`
- utilisez le au click du bouton (avec `Manifest.permission.READ_EXTERNAL_STORAGE`) et dans sa callback, utilisez le launcher précédent
- pour tester, créez temporairement un émulateur en API 9 ou moins, sur les autres devices, cela ne doit pas changer le fonctionnement

## Amélioration de la caméra

Actuellement, la qualité d'image récupérée de l'appareil photo est très faible (car passée en `Bitmap` dans la RAM), pour changer cela il faut utiliser le contrat `TakePicture` qui écrit dans un fichier passé au launcher par une `Uri`

```kotlin
// propriété: une URI dans le dossier partagé "Images"
private val captureUri by lazy {
    contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, ContentValues())
}

// launcher
val takePicture = rememberLauncherForActivityResult(TakePicture()) { success ->
    if (success) uri = capturedUri
}

// utilisation
takePicture.launch(captureUri)
```

## Refactor

- Comme précédemment, re-factorisez un peu en créant un `UserViewModel`: il ne doit plus y avoir de calls API directement dans `UserActivity`

## Édition infos utilisateurs

- Dans `UserActivity`, permettre d'afficher et éditer le nom d'utilisateur
- Vous aurez besoin d'ajouter une méthode à `UserWebService`:

```kotlin
@PATCH("sync/v9/sync")
suspend fun update(@Body commands: List<Commands>): Response<Unit>
```

- Référez vous à la [documentation](https://developer.todoist.com/sync/v9/#user) car ce n'est pas une API REST donc on ne passe pas simplement l'objet `User`: il faut créer un objet `Commands` de type `user_update`

## Gérer le refus

<aside class="positive">

Il y a tout une gestion [assez compliquée](https://developer.android.com/training/permissions/requesting#workflow_for_requesting_permissions) notamment dans le cas où l'utilisateur _refuse_ une permission

</aside>

- Modifiez votre code pour suivre les recommendations de google en vous aidant de ceci:

```kotlin
private fun pickPhotoWithPermission() {
    val storagePermission = Manifest.permission.READ_EXTERNAL_STORAGE
    val permissionStatus = checkSelfPermission(storagePermission)
    val isAlreadyAccepted = permissionStatus == PackageManager.PERMISSION_GRANTED
    val isExplanationNeeded = shouldShowRequestPermissionRationale(storagePermission)
    when {
        isAlreadyAccepted -> // lancer l'action souhaitée
        isExplanationNeeded -> // afficher une explication
        else -> // lancer la demande de permission et afficher une explication en cas de refus
    }
}

private fun showMessage(message: String) {
    Snackbar.make(findViewById(android.R.id.content), message, Snackbar.LENGTH_LONG).show()
}
```

Pour faire encore mieux, vous pouvez aussi afficher un message avec AlertDialog en Compose et continuer le flow en fonction de la réponse de l'utilisateur
