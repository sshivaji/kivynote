python virtualenv.py --system-site-packages drawpython
drawpython/bin/pip install setuptools --no-use-wheel --upgrade
drawpython/bin/pip install cython==0.20
drawpython/bin/pip install hg+http://bitbucket.org/pygame/pygame
drawpython/bin/pip install kivy==1.9.1
drawpython/bin/pip install git+https://github.com/kivy/buildozer.git@master
drawpython/bin/pip install git+https://github.com/kivy/plyer.git@master
drawpython/bin/pip install -U pygments docutils
