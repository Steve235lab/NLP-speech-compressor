# NLP-speech-compressor
This speech compressor can record your speech, transform it into texts and then compress (delete all the meaningless 
parts like repeats and modal verbs) to make the words more friendly to readers.

## Usage
* Setup
  * Install python 3.7 
  * Switch to the repository directory
  * Start a new python venv and install the packages 
    ```shell
    pip install -r .\requirements.txt
    ```
* Run with Qt GUI
    ```shell
    python .\src\main_window.py
    ```
* Run in terminal
    ```shell
    python .\src\local_main.py
    ```
    * Start inputting audio and transforming audio into text simultaneously
        ```
        >>>start
        ```
    * Stop inputting audio
        ```
        >>>cut
        ```
    * Compress the text
        ```
        >>>compress
        ```
    * Print the original text
        ```
        >>>print original text
        ```
    * Print segmented text
        ```
        >>>print original words
        ```
    * Print compressed text
        ```
        >>>print compressed text
        ```
    * Check is the app recording
        ```
        >>>is recording
        ```
  
