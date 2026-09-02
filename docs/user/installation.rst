Installation
============

``czml3`` requires **Python >= 3.10**.

You can install ``czml3`` using ``pip``::

   pip install czml3

or ``conda``::

   conda install czml3 --channel conda-forge

Development Installation
------------------------

To install ``czml3`` from source with all development dependencies::

   git clone https://github.com/Stoops-ML/czml3.git
   cd czml3
   uv sync

or, using ``pip`` (requires pip >= 25.1 for ``--group``)::

   pip install -e . --group dev