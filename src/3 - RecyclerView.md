---
marp: true
---
<!-- headingDivider: 2 -->

# RecyclerView

## Fonctionnement

![bg right 70%](../assets/recyclerview.png)

Conteneur scrollable pour afficher une grande quantité de donnée de façon efficace:

- crée un nombre limité de Views
- les réutilise en remplaçant les données et les listeners (re-bind) sans les recréer
- Met à jour les données rapidement

## List layout

```xml
<android.support.v7.widget.RecyclerView
   android:id="@+id/recyclerview"
   android:layout_width="match_parent"
   android:layout_height="match_parent"
   app:layoutManager="androidx.recyclerview.widget.LinearLayoutManager" />
```

## Item layout

```xml
<LinearLayout
   android:layout_width="match_parent"
   android:layout_height="match_parent">
   <TextView
       android:id="@+id/word"
       android:layout_width="wrap_content"
       android:layout_height="wrap_content" />
</LinearLayout>
```

## RecyclerView Adapter: implementation

```kotlin
class WordListAdapter(val wordList: List<Word>) : RecyclerView.Adapter<WordListAdapter.WordViewHolder>() {
   override fun getItemCount(): Int {
      // return the number of elements in the list
   }

   override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): WordViewHolder {
      // inflate a view to create a ViewHolder instance
   }

   override fun onBindViewHolder(holder: WordViewHolder, position: Int) {
      // bind() the list element at the current position to the holder
   }

   inner class WordViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
      fun bind(word: Word) {
         // Fill a cell with data
      }  
   }
}
```

## RecyclerView Adapter: usage

```kotlin
// At fragment or activity creation:
val wordList = mutableListOf("word#1", "word #2")
val myAdapter = WordListAdapter(wordList)

// Setup when view is ready:
recyclerView.adapter = myAdapter
recyclerView.layoutManager = LinearLayoutManager(context)

// Notify when data changes
worldList.add("word #3)
myAdapter.notifyDataSetChanged()
myAdapter.notifyItemChanged(2)
```

## ListAdapter

```kotlin
object WordsDiffCallback : DiffUtil.ItemCallback<Word>() {
   override fun areItemsTheSame(oldItem: Word, newItem: Word) =
      // are they the same "entity" ? (usually same id)
   override fun areContentsTheSame(oldItem: Word, newItem: Word) =
      // do they have the same data ? (content)
}

class WordListAdapter : ListAdapter<Word, WordListAdapter.WordViewHolder>(WordsDiffCallback) {
   // use `currentList`
   override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): WordViewHolder {...}
   override fun onBindViewHolder(holder: WordViewHolder, position: Int)  {...}
}

// Usage is simpler:
val myAdapter = WordListAdapter()
recyclerView.adapter = myAdapter
myAdapter.submitList(listOf("word#1", "word #2"))
```

## iOS

![bg right 80%](../assets/ios_table.png)

In storyboard:

- UITableViewController
- UITableViewCell prototype

In code:

- UITableViewDataSource protocol implementation

[See Documentation](https://developer.apple.com/documentation/uikit/views_and_controls/table_views/filling_a_table_with_data)

## Example

```swift
var hierarchicalData = [[String]]()

class MyTableDataSource : UITableViewDataSource {

   override func numberOfSections(in tableView: UITableView) -> Int {
      return hierarchicalData.count
   }

   override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
      return hierarchicalData[section].count
   }

   override func tableView(_ tableView: UITableView,
                           cellForRowAt indexPath: IndexPath) -> UITableViewCell {
      // Ask for a cell of the appropriate type.
      let cell = tableView.dequeueReusableCell(withIdentifier: "basicStyleCell", for: indexPath)

      // Configure the cell’s contents with the row and section number.
      // The Basic cell style guarantees a label view is present in textLabel.
      cell.textLabel!.text = "Row \(indexPath.row)"
      return cell
   }
}
```

## Jetpack Compose

![bg left:30% 80%](../assets/compose.svg)

```kotlin
LazyColumn {
    items(wordList) { word ->
      Text("Object: $word")
   }
}
```

hé oui, c'est tout 🤷 

Pareil en SwiftUI : `List(elements) { element in ... }` 