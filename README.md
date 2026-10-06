# czml3
[![pypi](https://img.shields.io/pypi/v/czml3)](https://pypi.org/project/czml3/)
[![conda](https://img.shields.io/conda/vn/conda-forge/czml3?label=conda)](https://anaconda.org/conda-forge/czml3)
![Python](https://img.shields.io/pypi/pyversions/czml3)
[![codecov](https://codecov.io/gh/Stoops-ML/czml3/graph/badge.svg?token=EF8SIL2JBV)](https://codecov.io/gh/Stoops-ML/czml3)
![pypi-downloads](https://img.shields.io/pepy/dt/czml3?label=pypi%20downloads)
![conda-downloads](https://img.shields.io/conda/dn/conda-forge/czml3?label=conda%20downloads)
![workflow-status](https://img.shields.io/github/actions/workflow/status/Stoops-ML/czml3/workflow.yml)
[![Documentation Status](https://readthedocs.org/projects/czml3/badge)](https://czml3.readthedocs.io/en)

From the official [CZML Guide](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CZML-Guide):
> CZML is a JSON format for describing a time-dynamic graphical scene, primarily for display in a web browser running Cesium. It describes lines, points, billboards, models, and other graphical primitives, and specifies how they change with time.

czml3 aims to make the process of writing CZML files in Python easy by:
- Type checking properties
- Coercion of data to their required format
- Forbidding unrecognised properties
- Creating minimal CZML files
- Fast JSON serialization

## Installation
You can install czml3 using pip:
```
pip install czml3
```

or conda:
```
conda install czml3 --channel conda-forge
```

## Examples

### Creating a document
A CZML document is a list of *packets*, which have several properties. Recreating the blue box from Cesium sandcastle's [CZML Box](https://sandcastle.cesium.com/?src=CZML%20Box.html&label=CZML):

```python
from czml3 import (
    Box,
    BoxDimensions,
    Color,
    Document,
    Material,
    Packet,
    Position,
    SolidColorMaterial,
)

packet_box = Packet(
    id="my_id",
    position=Position(cartographicDegrees=[-114.0, 40.0, 300000.0]),
    box=Box(
        dimensions=BoxDimensions(cartesian=[400000.0, 300000.0, 500000.0]),
        material=Material(
            solidColor=SolidColorMaterial(color=Color(rgba=[0, 0, 255, 255]))
        ),
    ),
)
doc = Document(packets=[packet_box])
print(doc)
```

<details>
<summary>Output</summary>

```bash
[
    {
        "id": "document",
        "name": "document",
        "version": "1.0"
    },
    {
        "id": "my_id",
        "position": {
            "cartographicDegrees": [
                -114.0,
                40.0,
                300000.0
            ]
        },
        "box": {
            "dimensions": {
                "cartesian": [
                    400000.0,
                    300000.0,
                    500000.0
                ]
            },
            "material": {
                "solidColor": {
                    "color": {
                        "rgba": [
                            0,
                            0,
                            255,
                            255
                        ]
                    }
                }
            }
        }
    }
]
```

</details>

### The document packet
`Document` adds the required preamble packet (`id="document"`) when you don't supply one. To name the document or set its clock, pass your own preamble packet first:

```python
from czml3 import CZML_VERSION, Document, Packet

doc = Document(
    packets=[
        Packet(id="document", name="My scene", version=CZML_VERSION),
        packet_box,
    ]
)
```

### Imports
The most common classes can be imported from `czml3` directly; everything else lives in `czml3.properties`, `czml3.types` and `czml3.enums`.

### Data coercion
czml3 uses [pydantic](https://docs.pydantic.dev/latest/) for all classes, so it is able to [coerce data to their right type](https://docs.pydantic.dev/latest/why/#json-schema).

Plain lists are converted to the matching CZML value type, so `BoxDimensions(cartesian=[...])` is equivalent to `BoxDimensions(cartesian=Cartesian3Value(values=[...]))`.

Arrays are coerced too. For example, the following creates a Position property of doubles using a numpy array of integer type:
```python
import numpy as np
from czml3.properties import Position

print(Position(cartographicDegrees=np.array([-114, 40, 300000], dtype=int)))
```
```bash
{
    "cartographicDegrees": [
        -114.0,
        40.0,
        300000.0
    ]
}
```

### Saving and loading
```python
doc.save("scene.czml")
doc = Document.load("scene.czml")
```

### Viewing a document
In Jupyter, displaying a `Document` renders it in an interactive Cesium viewer.

Outside notebooks, write the same viewer as a standalone page:
```python
doc.save_html("scene.html")
```
- `ion_token=` uses Cesium ion imagery and terrain.
- `cesium_version=` chooses the CesiumJS release.

Browsers block Cesium's web workers on pages opened straight from disk (`file://`), so serve the file over HTTP and open `http://localhost:8000/scene.html`:
```bash
python -m http.server
```

## Contributing
You want to contribute? Awesome! There are lots of [CZML properties](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet) and validations that we still did not implement, which can be found [here](https://czml3.readthedocs.io/en/latest/user/contributing.html).

All ideas welcome!
