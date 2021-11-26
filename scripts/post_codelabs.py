import os
import glob


def add_text_to_files(pattern, text):
    """Iterates over files matching *pattern* 
    in the directory and appends *text* to the end of the file.
    """
    for fname in glob.glob(pattern):
        with open(fname, 'a') as f:
            f.write(text)


add_text_to_files(
    "codelabs/*/index.html",
    """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById("arrow-back").href="/formation-android/codelabs/";
            document.getElementById("done").href="/formation-android/codelabs/";
        }, false);
    </script>

    """
)
