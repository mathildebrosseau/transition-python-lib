<!-- The fact that the library and the app have the same names is confusing.. -->
# Transition
Transition is a Python package designes to interact with the public API of the transit planning application Transition. It allows users to retrieve and request geographic and routing data from the app.

## Install and import Transition
To install Transition, use the following command :
<!-- -[//]:#(probably something like pip install transition)- -->
```
```
After installing Transition, it may be imported into Python code like :
```python
import Transition
```
## Usage
All methods in Transition are static methods. It provides the following :
### set_url :
This method allows to set the base URL that will be used for the API calls. By default, it is set to the development URL.\
**Parameters :**&emsp;***url***&ensp;:&ensp;*string*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;The URL used for API calls.
<!-- http://localhost:8080, should we hard code this as a value or ask the user to specify it upon login ? -->

### get_paths :
This method allows to fetch all paths which are currently loaded in the Transition application. In case of a successful request, the paths are returned in GeoJSON format.

### get_nodes :
This method allows to fetch all nodes which are currently loaded in the Transition application. In case of a successful request, the nodes are returned in GeoJSON format.

### get_scenarios :
This method allows to fetch all scenarios which are currently loaded in the Transition application. In case of a successful request, the scenarios are returned in JSON format. The scenarios are needed in order to request calculations for new routes or accessibilite maps.

### get_routing_modes :
This method allows to fetch all routing modes which are currently loaded in the Transition application. In case of a successful request, a list of routing modes is returnes. The routing modes are needed in order to request calculations for new routes and currently include transit, driving, and walking.

### get_routing_result:
This method allows to send calculation details to the Transition server to request a new route. In case of a successful request, the new route is returned in JSON format.\
**Parameters :**&emsp;***modes*** : *list*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;The transit modes for which to calculate the routes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***origin***&ensp;:&ensp;*GeoJSON* \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;The origin coordinates.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***destination***&ensp;:&ensp;*GeoJSON* \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;The destination coordinates.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***scenario_id***&ensp;:&ensp;*string*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;The ID of the used scenario as loaded in Transition application.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_travel_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***min_waiting_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_transfer_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_access_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***departure_or_arrival_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***departure_or_arrival_label***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_first_waiting_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***with_geojson***&ensp;:&ensp;*bool*\

**returns :**&emsp;***result*** : *JSON*