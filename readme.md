Copyright &copy; 2015, [Brendan Doms](http://www.bdoms.com/)  
Licensed under the [MIT license](http://www.opensource.org/licenses/MIT)


GAE Graph DB creates network graphs of a Google App Engine datastore.

### Dependencies

It depends on graphviz and pydot:

```bash
sudo apt-get install graphviz
pip install pydot
```

### Command Line Use

To use from the command line just supply the path to a model file and an output image file:

```bash
python gae_graph "path/to/model/file" "output.png"
```

### Use as a Module

To use from a Python script, first analyze the model file to get out lists of models:

```python
edges, inheritences, nodes = analyzeModels("path/to/model/file")
```

Then you can write out the graph image:

```python
writeGraph(edges, inheritences, nodes, "output.png")
```

Additionally, `writeGraph` takes two optional parameters:

 * `method` - the graphviz program to use when creating the image
 * `parent_childs` - a list of tuples, e.g. [('Parent', 'Child')]

Parent child relationships must be entered manually this way
because they are established at run time and therefore can't be detected automatically.
