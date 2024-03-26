<!-- The fact that the library and the app have the same names is confusing.. -->
# Transition
Transition is a Python package designed to interact with the public API of the transit planning application Transition. It allows users to retrieve and request geographic and routing data from the app.

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
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;URL used for API calls.

**Raises :**&emsp;**&emsp;**&emsp;***ValueError***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If the parameter is empty.
<!-- http://localhost:8080, should we hard code this as a value or ask the user to specify it upon login ? -->

### set_username :
This method allows to set the base URL that will be used for the API calls. By default, it is set to the development URL.\
**Parameters :**&emsp;***username***&ensp;:&ensp;*string*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;username associated to the cucrrently used token.

**Raises :**&emsp;**&emsp;**&emsp;***ValueError***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If the parameter is empty.

### get_paths :
This method allows to fetch all paths which are currently loaded in the Transition application. In case of a successful request, the paths are returned in JSON format.

**Returns :**&emsp;&emsp;&ensp;***result*** : *GeoJSON*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;All paths currently loaded in the Transition app in GeoJSON format

**Raises :**&emsp;**&emsp;**&emsp;***RequestException***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If response code is not 200.

### get_nodes :
This method allows to fetch all nodes which are currently loaded in the Transition application. In case of a successful request, the nodes are returned in JSON format.

**Returns :**&emsp;&emsp;&ensp;***result*** : *GeoJSON*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;All nodes currently loaded in the Transition app in GeoJSON format

**Raises :**&emsp;**&emsp;**&emsp;***RequestException***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If response code is not 200.

### get_scenarios :
This method allows to fetch all scenarios which are currently loaded in the Transition application. In case of a successful request, the scenarios are returned in JSON format. The scenarios are needed in order to request calculations for new routes or accessibility maps.

**Returns :**&emsp;&emsp;&ensp;***result*** : *JSON*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;All scenarios currently loaded in the Transition app in JSON format

**Raises :**&emsp;**&emsp;**&emsp;***RequestException***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If response code is not 200.

### get_routing_modes :
This method allows to fetch all routing modes which are currently loaded in the Transition application. In case of a successful request, a list of routing modes is returned. The routing modes are needed in order to request calculations for new routes.

**Returns :**&emsp;&emsp;&ensp;***result*** : *list*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;All routing modes currently loaded in the Transition app.

**Raises :**&emsp;**&emsp;**&emsp;***RequestException***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If response code is not 200.

### get_accessibility_map
This method allows to send accessibility map parameters to the Transition server to request a new accessibility map. In case of a successful request, the accessibility map is returned in JSON format.\
**Parameters :**&emsp;***coord_latitude*** : *float*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Latitude of the starting point of the accessibility map.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***coord_longitude***&ensp;:&ensp;*float*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Longitude of the starting point of the accessibility map.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***scenario_id***&ensp;:&ensp;*string*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;ID of the used scenario as loaded in Transition application.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***departure_or_arrival_choice***&ensp;:&ensp;*string* \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Specifies whether the used time is "Departure" or "Arrival".\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***departure_or_arrival_time***&ensp;:&ensp;*Time* \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Departure or arrival time of the trip.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***n_polygons***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Number of polygons to be calculated\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***delta_minutes***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Baseline delta used for average accessibility map calculations.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***delta_interval_minutes***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Interval used between each calculation.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***place_name***&ensp;:&ensp;*string*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Name of the place (?) <!-- Not sure about this one -->\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_total_travel_time_minutes***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Maximum travel time, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***min_waiting_time_minutes***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Minimum waiting time, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_access_egress_travel_time_minutes***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Maximum access time, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_transfer_travel_time_minutes***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Maximum transfer time, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_first_waiting_time_minutes***&ensp;:&ensp;*bool*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Maximum wait time at first transit stop, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***walking_speed_kmh***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Walking speed, in km/h\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***with_geojson***&ensp;:&ensp;*bool*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If True, the returned JSON file will contain geometry information for the strokes and polygons of the accessibility map.

**Returns :**&emsp;&emsp;&ensp;***result*** : *JSON*
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Accessibility map information in JSON format.\

**Raises :**&emsp;**&emsp;**&emsp;***RequestException***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;If response code is not 200.

### get_routing_result:
This method allows to send calculation parameters to the Transition server to request a new route. The request can be mode for different transit modes. In case of a successful request, the new route is returned in JSON format.\
**Parameters :**&emsp;***modes*** : *list*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Transit modes for which to calculate the routes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***origin***&ensp;:&ensp;*list* \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Origin coordinates. Must be sent as [longitude, latitude]\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***destination***&ensp;:&ensp;*list* \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Destination coordinates. Must be sent as [longitude, latitude]\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***scenario_id***&ensp;:&ensp;*string*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;ID of the used scenario as loaded in Transition application.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***departure_or_arrival_choice***&ensp;:&ensp;*string*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Specifies whether the used time is "Departure" or "Arrival".\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***departure_or_arrival_time***&ensp;:&ensp;*Time*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Departure or arrival time of the trip.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_travel_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Maximum travel time including access, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***min_waiting_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Minimum waiting time, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_transfer_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Maximum transfer time, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_access_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Maximum access time, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***max_first_waiting_time***&ensp;:&ensp;*int*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Maximum wait time at first transit stop, in minutes.\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;***with_geojson***&ensp;:&ensp;*bool*\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;If True, the returned JSON file will contain the "pathsGeojson" key for each mode, which contains the GeoJSON geometry.

**Returns :**&emsp;&emsp;&ensp;***result*** : *JSON*
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Route for each transit mode in JSON format.

**Raises :**&emsp;***RequestException***\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;If response code is not 200.
