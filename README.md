
# Brief

dicthub is a simple app indicator that helps to store dict and sentence.

# Install
```
sudo python setup.py install --record install.txt
```

# Uninstall
```
cat install.txt | xargs sudo rm -rf
```

# Platforms
Ubuntu 16.04 (Only test for now)

# Requires
  - PyGObject   
    Get help from [here](https://lazka.github.io/pgi-docs/)
  - Click   
    [Click](http://github.com/pallets/click) is a python package for creating beautiful command line interfaces   
    in a composable way with as little amount of code as necessary. 

# Components
  - app indicator
    - save selection
    - open dict web
    - dict web server actions   
    . . .
  - command line interface named `dicthub`
    - indicator actions
    - server actions

# Usage
  Select word or sentence, and then click 'Save It' menu item in app indicator.
