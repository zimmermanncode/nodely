### 0.3.1

> 2019-07-29

* Restrict requirement `path.py` to `~= 11.5`

### 0.3.0.post0

> 2019-07-29

* Update `CHANGES` for __0.3.0__ release

### 0.3.0

> 2019-07-28

* Add `.check_call` and `.check_output` methods to `nodely.bin.Command`,
  the class of the Pythonic `nodely.bin['...']` instances for running
  installed Node.js tools
* Make `nodely.bin.Command.__call__` wrap `.check_output` instead of `.call`
  and take variable `*cmdargs` parameters instead of a single positional
  `cmdargs` sequence parameter
* Define `nodely.NodeCommandError` based on `subprocess.CalledProcessError`.
  It adds the working directory to the basic exception message and is raised
  from `nodely.bin.Command.check_call` and `.check_output`

### 0.2.0

> 2017-09-12

* Provide new setup keyword `require_node_modules`

### 0.1.0.post0

> 2017-08-27

* Updated `CHANGES` for __0.1.0__ release

### 0.1.0

> 2017-08-27

* `nodely` package with `install`, `uninstall`, `which`, `Popen`, and `call`
  functions
* `nodely.bin` proxy to `node_modules/.bin/` directory in Python environment
