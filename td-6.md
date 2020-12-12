
# TD 6: Images

## Afficher une image distante avec Coil

- Rendez vous sur le [repository de Coil](https://coil-kt.github.io/coil/) et lisez le `ReadMe`
- Ajouter les dépendances nécessaires à `app/build.gradle`
- Ajouter une `ImageView` à coté de votre `header_text_view` qui affichera l'avatar de l'utilisateur
- Dans `onResume`, utiliser Coil pour afficher une image en passant une URL de votre choix (à défault vous pouvez utiliser `"https://goo.gl/gEgYUd"`)

```kotlin
image_view.load("VOTRE_URL")
```

- Trouvez comment afficher l'image sous la forme d'un cercle

### Nouvelle activité

- Créer un nouveau package `userinfo`
- Créez y une nouvelle activité `UserInfoActivity` et ajoutez la dans le manifest
- Remplir son layout:

```xml
<LinearLayout ...>
    <ImageView
        android:id="@+id/image_view"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <Button
        android:id="@+id/upload_image_button"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Choisir une Image" />

    <Button
        android:id="@+id/take_picture_button"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Prendre une photo" />
</LinearLayout>
```

- Lancer cette `Activity` quand on clique sur l'`ImageView` que vous venez de remplir avec `Coil`

## Demander la Permission

- `AndroidManifest`: ajouter la permission `android.permission.CAMERA`
- `UserInfoActivity` : Dans `onCreate()`, ajouter un `onClickListener` à `take_picture_button` qui appele la méthode `askCameraPermissionAndOpenCamera()`

- Prenez le temps de lire et comprendre ce pavé 🤔 :

```kotlin
private val requestPermissionLauncher =
        registerForActivityResult(RequestPermission()) { isGranted: Boolean ->
            if (isGranted) openCamera()
            else showExplanationDialog()
        }

private fun requestCameraPermission() =
        requestPermissionLauncher.launch(Manifest.permission.CAMERA)

private fun askCameraPermissionAndOpenCamera() {
    when {
        ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_GRANTED -> openCamera()
        shouldShowRequestPermissionRationale(Manifest.permission.CAMERA) -> showExplanationDialog()
        else -> requestCameraPermission()
    }
}

private fun showExplanationDialog() {
    AlertDialog.Builder(this).apply {
        setMessage("On a besoin de la caméra sivouplé ! 🥺")
        setPositiveButton("Bon, ok") { _, _ ->
            requestCameraPermission() 
        }
        setCancelable(true)
        show()
    }
}
```

➡️ C'est normal que le code ne marche pas tout de suite il manque des choses

## Ouvrir l'appareil photo

Pour l'ouverture de la caméra, on utilise la nouvelle API:

```kotlin
// create a temp file and get a uri for it
private val photoUri = getContentUri("temp")

// register
private val takePicture =
        registerForActivityResult(TakePicture()) { success ->
            if (success) handleImage(photoUri)
            else Toast.makeText(this, "Si vous refusez, on peux pas prendre de photo ! 😢", Toast.LENGTH_LONG).show()
        }

// use
private fun openCamera() = takePicture.launch(photoUri)
```

➡️ Il manque encore une brique !

## Uploader l'image capturée

- Dans l'interface `UserWebService`, ajouter une nouvelle fonction

```kotlin
@Multipart
@PATCH("users/update_avatar")
suspend fun updateAvatar(@Part avatar: MultipartBody.Part): Response<UserInfo>
```

- Ajouter une fonction pour convertir l'image afin de pouvoir l'envoyer en HTTP:

```kotlin
// convert     
private fun convert(uri: Uri) =
        MultipartBody.Part.create(uri.toFile().asRequestBody())
```

- Ajoutez une méthode `handleImage` qui utilise `updateAvatar` avec et `convert`
- Modifier la `data class UserInfo` pour ajouter un champ `avatar: String` qui est une URL renvoyée depuis le serveur
- Enfin au chargement de l'activité, afficher l'avatar renvoyé depuis le serveur:

```kotlin
    lifecycleScope.launch {
        val userInfo = ...getInfos()
        imageView.load(userInfo.avatar)
    }
```

## Uploader une image stockée

- Ajouter dans le manifest la permission `android.permission.READ_EXTERNAL_STORAGE`
- Permettez à l'utilisateur d'uploader une image enregistrée sur son téléphone

```kotlin
// register
private val pickInGallery = 
    registerForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        handleImage(uri) 
    }

// use
pickInGallery.launch("image/*")
```

## Édition infos utilisateurs

- Comme précedemment, refactorisez en utilisant un `UserInfoViewModel` et un `UserInfoRepository`
- Dans `UserInfoActivity`, permettre d'éditer et d'afficher les informations (nom, prénom, email) en respectant cette architecture
- Vous aurez besoin d'ajouter ça à `UserWebService`:

```kotlin
@PATCH("users")
suspend fun update(@Body user: UserInfo): Response<UserInfo>
```
