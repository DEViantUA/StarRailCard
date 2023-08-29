## How the argument works: save

* The save argument saves the generated cards on your device, along the path: ``/RailCard/{uid}/{charter_name}_{data}.png``
* Date format: ``datetime.datetime.now().strftime("%d_%m_%Y %H_%M")``

## Where to use?

* The argument is used in the class: [MiHoMoCard](https://github.com/DEViantUA/StarRailCard/wiki/MiHoMoCard)

## Example:

```py
from starrailcard import honkaicard

railCard = MiHoMoCard(save= True)

```


   
