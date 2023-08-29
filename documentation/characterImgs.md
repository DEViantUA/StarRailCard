## Argument usage examples: characterImgs




1. In this way we are passing image links:
```py
characterImgs = {"Name_charter_1": "image link", "charter_id": "image link", ...}
```

<br>


2. In this method, we specify the path to the file on your device:
```py
characterImgs = {"Name_charter_1": "сomputer/image/charter1.png", "charter_id": "сomputer/image/charter2.png", ...}
```

<br>

3. In this method, we are passing the open image through Pillow:
```py
from PIL import Image

image = Image.open("сomputer/image/charter2.png")
characterImgs = {"Name_charter_1": image, ...}
```


## Where to use?

* The argument is used in the class: [MiHoMoCard](https://github.com/DEViantUA/StarRailCard/wiki/MiHoMoCard)
* ``charter_id`` | ``Name_charter_n`` - The key can be either the name of the character or its ID.   ( I recommend using id )



## Example:

```py
from starrailcard import honkaicard

railCard = MiHoMoCard(characterImgs = {"Name_charter_1": "image link", "Name_charter_2": "image link", ...})

```
