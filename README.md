# SQLiteKG for pyRDF2Vec

SQLiteKG implements the `KG` class from [pyRDF2Vec](https://github.com/IBCNServices/pyRDF2Vec),
which is a popular library to train the RDF2Vec model for knowledge graphs. It
aims to be less memory hungry than constructing a KG from scratch using pyRDF2Vec,
or running a local/remote triplestore. 

SQLiteKG creates a local SQLite database, and all the statements of a knowledge
graph gets loaded into one big SQL table. The neighbours and hops for nodes in
the knowledge graph get gathered with simple SQL queries.

## Usage

```python
import sqlitekg

from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec
from pyrdf2vec.walkers import RandomWalker

with sqlitekg.open_from_pykeen_dataset('dbpedia50', combined=True) as kg:
    transformer = RDF2VecTransformer(
        Word2Vec(epochs=100),
        walkers=[RandomWalker(max_walks=200,
                              max_depth=4,
                              random_state=133,
                              with_reverse=False,
                              n_jobs=4)],
        verbose=1
    )
    # train RDF2Vec
    ent = kg.entities()
    embeddings, _ = transformer.fit_transform(kg, ent)
```

### Create from PyKeen dataset

[PyKeen](https://github.com/pykeen/pykeen) is a popular library for knowledge
graph embeddings, and it specifies a number of datasets that are commonly
referenced in scientific literature. An SQLite KG can be constructed from a
PyKeen dataset by specifying the name of the dataset or passing the dataset
instance.

In the following code snippet, the `db100k` dataset, which is a subsampling of
DBpedia, is used to construct an SQLite KG.

```python
import sqlitekg

with sqlitekg.open_from_pykeen_dataset('db100k', combined=True) as kg:
    # ...
    pass
```

**Parameters:**

* *combined* - `False` if only the training set of a dataset shall be used for
  the training of RDF2Vec. `True` if all the sets (training, testing and
  validation) shall be used. It is `False` by default.

### Create from TSV file

In order to save memory for big knowledge graphs, it might be a good idea to
load the statements of such a knowledge graph from a TSV file into a SQLite KG.
All the rows in the TSV file must have three columns, where the first column is
the subject, the second is the predicate, and the last column is the object.

The following code snippet creates a new SQLite KG instance from the statements
of the specified TSV file, which has been compressed using GZIP.

```python
import sqlitekg

with sqlitekg.open_from_tsv_file('statements.tsv.gz', compression='gzip') as kg:
    # ...
    pass
```

**Parameters:**

* *skip_header* - `True` if the first row shall be skipped, because it is a
  header row for example. `False` if it shouldn't be skipped. It is `False` by
  default.
* *compression* - specifies the compression type of source TSV file. The default
  value is `None`, which means that the source isn't compressed. At the moment,
  only `'gzip'` is supported as compression type.

### Create from Pandas dataframe

A knowledge graph can be represented in a Pandas dataframe, and this method
allows to create an SQLite KG from a dataframe. While the dataframe can have
more than three columns, the three columns representing the subject, predicate
and object must be specified in this particular order.

The following code snippet creates a new SQLite KG instance from a dataframe.

```python
import sqlitekg

with sqlitekg.open_from_dataframe(df,
                                  column_names=('subj', 'pred', 'obj')) as kg:
    # ...
    pass
```

**Parameters:**

* *column_names* - a tuple of three indices for the dataframe, which can be an
  integer or string. The first entry of the tuple shall point to the subject,
  the second to the predicate, and the third one to the object. `(0, 1, 2)` are
  the default indices.

## Contact

* Kevin Haller - [contact@kevinhaller.dev](mailto:contact@kevinhaller.dev)