# learning-outcome-analysis

A CLI tool for analysing the learning outcomes (LOs) of a curriculum, within a given taxonomy, e.g. Blooms taxonomy.
The tool parses LOs using the spaCy nlp toolkit to identify verbs and gives a breakdown of the taxonomy categories reached by each LO, in json form.
Use a Blooms-based provided taxonomy to analyse your curricula or create your own custom ones.

# Installation
```
pip install -r requirements.txt
```
# Usage
The tool comprises 3 scripts: 1) building a taxonomy, 2) building a curriculum 3) anlysing your curriculum with a taxonomy. 

1) You need to have a text file ready with all the verbs of your taxonomy. Verbs should be comma-separated and verb categories line-separated, as in the blooms.txt file in the fixtures directory. Then run 
```
python -m main.build_taxonomy 
```
Choose a taxonomy name and give the path of the verb text file, relative to the project directory, e.g. if you want to use the provided text file, enter fixtures/blooms.txt Then enter the names of the verb categories, e.g. knowledge, comprehension etc..
When finished, you should see 2 new taxonomy files in the project directory, with .pickle and .json extensions.

2) You need to have a text file ready with all the LOs of your curriculum. LOs should be line-separated. If there are different LO modules/strands, these should be separated by a blank line in the file, as in the CS.txt in the fixtures directory, which represents an Irish computer science curriculum with 3 LO strands: "core concepts", "practices and principles" and "applied learning tasks". Then run
```
python -m main.build_curriculum
```
Choose a curriculum name and give the path of the LO text file, relative to the project directory, e.g. if you want to use the provided text file, enter fixtures/CS.txt. Then enter the names of the LO strands.
When finished, you should see 2 new curriculum files project directory, with .pickle and .json extensions.

3) Choose a curriculum and taxonomy whose pickle files you will provide as arguments to the analysis script. 
For example, using the CS and BLOOMS pickle files provided in the fixtures, then run
```
python -m main.analyse_curriculum -C fixtures/CS.curriculum.pickle -T fixtures/BLOOMS.tax.pickle
```
You should see a new CS-BLOOMS.count.json file in the main project directory with a breakdown of all taxonomy category hit counts across all the learning outcomes.

# Tests
```
python -m unittest discover -s tests 
```
