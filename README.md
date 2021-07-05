## SemLink's WordNet-FrameNet Mappings

This is a script for extracting the WordNet-FrameNet Mappings from [SemLink](https://github.com/cu-clear/semlink).

### Download:
* `git clone --recurse-submodules https://github.com/nu11us/SemLink-WN-FN-Mappings`

### Configuration:
* Create a virtual environment: `python -m venv venv`
* Enter virtual environment: `source venv/bin/activate`
* `pip install -r requirements.txt`
* In Python:
    * `import nltk`
    * `nltk.download('wordnet')`
    * `nltk.download('framenet_v17')`

### To Extract Mapping to CSV
* Default: `python mapper.py`
* To a given output: `python mapper.py <output>`
* To a given output with a custom VerbNet and Semlink directory: `python mapper.py <output> <verbnet> <semlink>`

### Citations
Please cite the following:
* Karin Kipper, Anna Korhonen, Neville Ryant, Martha Palmer, A Large-scale Classification of English Verbs, Language Resources and Evaluation Journal, 42(1), pp. 21-40, Springer Netherland, 2008.
* Kevin Stowe, Jenette Preciado, Kathryn Conger, Susan Brown, Ghazaleh Kazeminejad, James Gung, and Martha Palmer, SemLink 2: Chasing Lexical Resources, IWCS, 2021