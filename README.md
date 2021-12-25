# micro utils

基于 python ，业务常用功能但未在网上找到的代码，封装为 `micro-utils`

## 主要功能

- gps 坐标得到地址信息（百度地图 api）


## 代码示例

### gps 坐标得到地址信息（百度地图 api）

```py
#!/usr/bin/env python3

from micro_utils import gps

lat = '39.9878'
lng = '116.4007'
AK = 'your_AK'
SK = 'your_SK'

address_data = gps.get_address(location=(lat, lng), ak=AK, sk=SK)
print(address_data)
```


