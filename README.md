

# nodely >>> putMORE Node.js into Python



[![](http://www.gnu.org/graphics/lgplv3-88x31.png)](
  https://gnu.org/licenses/lgpl.html)
[![](https://img.shields.io/pypi/pyversions/nodely.svg)](
  https://python.org)
[![](https://img.shields.io/pypi/v/nodely.svg)](
  https://pypi.python.org/pypi/nodely)
[![](https://img.shields.io/pypi/dd/nodely.svg)](
  https://pypi.python.org/pypi/nodely)



[![](https://travis-ci.org/zimmermanncode/nodely.svg)](
  https://travis-ci.org/zimmermanncode/nodely)



* [**Embed**](#Embed-node_modules/-in-Python-environments)
  **`node_modules/` in Python environments**
* [**`require`**](#require_node_modules-in-setup.py)**`_node_modules`
  in setup.py** 
* [**Run**](#Run-installed-Node.js-tools-from-Python)
  **installed Node.js tools from Python**



### Setup



Use [pip](http://pip-installer.org) to install the latest [release](
  https://pypi.python.org/pypi/nodely) from [PyPI](https://pypi.python.org):

> `pip install nodely`

And don't forget to install [Node.js](https://nodejs.org) ;)



### Embed `node_modules/` in Python environments




```python
>>> import nodely
```


Many great tools are written with JavaScript in [Node.js](https://nodejs.org).
It makes sense to use them in Python instead of reinventing the wheel.
`nodely` provides an API for managing local `node_modules/` in Python environments
and running the installed Node.js tools from Python



If the root directory of the current Python environment is:




```python
>>> import sys
>>> 
>>> sys.prefix
'C:\\Users\\Zimmermann\\Miniconda3\\envs\\nodely'
```



Then `nodely` will create:




```python
>>> nodely.NODE_MODULES_DIR
Path('C:\\Users\\Zimmermann\\Miniconda3\\envs\\nodely\\node_modules')
```



_Please don't modify the above constant, except you exactly know what you are doing ;)_



Let's say you want to use the [CoffeeScript](http://coffeescript.org) compiler...
Just install the Node.js package:




```python
>>> nodely.install('coffee-script')
```

```
npm http GET https://registry.npmjs.org/coffee-script
npm http 304 https://registry.npmjs.org/coffee-script
coffee-script@1.12.7 node_modules\coffee-script
```


It provides the `coffee` executable. If you want to know its absolute path:




```python
>>> nodely.which('coffee')
Path('C:\\Users\\Zimmermann\\Miniconda3\\envs\\nodely\\node_modules\\.bin\\coffee.CMD')
```



And if you want to run it, for example with the `--version` flag:




```python
>>> nodely.call('coffee', ['--version'])
0
```

```
CoffeeScript version 1.12.7
```



For the case that you want to get rid of the package again,
just `nodely.uninstall('coffee-script')` it



### `require_node_modules` in setup.py



Instead of installing Node.js packages during runtime,
you can also define them as dependencies of your Python package:



```python
from setuptools import setup

setup(
    ...
    setup_requires=['nodely', ...],
    require_node_modules=['coffee-script', ...],
    ...
)
```



So they get implicitly installed during the installation of the Python package,
just like the Python dependencies defined in `install_requires`



### Run installed Node.js tools from Python



The `nodely.call` function additionally supports `subprocess.call` options:




```python
>>> from subprocess import DEVNULL
>>> 
>>> nodely.call('coffee', ['--version'], stdout=DEVNULL)
0
```



And instead of a simple `nodely.call`,
you can also create a process instance,
and give any `subprocess.Popen` options to it:




```python
>>> from subprocess import PIPE
>>> 
>>> process = nodely.Popen('coffee', ['--version'], stdout=PIPE,
...                        universal_newlines=True)
```



```python
>>> process.communicate()[0].split()[-1]
'1.12.7'
```



A more object-oriented approach is provided by:




```python
>>> import nodely.bin
```


It lets you introspect all installed executables with interactive auto-completion
and creates `nodely.bin.Command` instances:




```python
>>> coffee = nodely.bin.coffee
```


`nodely.bin['coffee']` returns the same.
And that `nodely.bin.Command` instance provides its own `.call` and a `.Popen` methods,
and can also be called directly instead of using its `.call` method:




```python
>>> coffee(['--version'])
0
```

```
CoffeeScript version 1.12.7
```
