## Argument usage examples: characterName

1. In this example, we will get only 1 character:
```py
characterName= "1209"
```

2. In this example, we will get only 3 character:
```py
characterName= "1209,Seele,1208"
```

## Where to use?

* The argument is used in the class: [MiHoMoCard](https://github.com/DEViantUA/StarRailCard/wiki/MiHoMoCard)
* ``charter_id`` | ``Name_charter_n`` - The key can be either the name of the character or its ID.   ( I recommend using id )
* character identifiers must be comma-separated as a string.



## Example:

```py
from starrailcard import honkaicard

railCard = MiHoMoCard(characterName= "1209,Seele,1208")

```


   
