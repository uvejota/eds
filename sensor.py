import logging
from homeassistant.const import POWER_KILO_WATT
from homeassistant.helpers.entity import Entity
from .api.EdistribucionAPI import Edistribucion
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=10)
FRIENDLY_NAME = 'EDS Consumo eléctrico'

DOMAIN = "edistribucion"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up platform."""
    add_entities([EDSSensor(config['username'],config['password'])])
    # Return boolean to indicate that initialization was successful.
    return True


class EDSPlatform(Entity):



    async def async_update(self):
        """Fetch new state data for the sensor."""
        edis = Edistribucion(self._usr,self._pw)
        edis.login()
        r = edis.get_cups()
        cups = r['data']['lstCups'][0]['Id']
        meter = edis.get_meter(cups)
        _LOGGER.debug(meter)
        _LOGGER.debug(meter['data']['potenciaActual'])
        attributes = {}
        attributes['CUPS'] = r['data']['lstCups'][0]['Name']
        attributes['Estado ICP'] = meter['data']['estadoICP']
        attributes['Consumo Total'] = str(meter['data']['totalizador']) + ' kWh'
        attributes['Carga actual'] = meter['data']['percent']
        attributes['Potencia Contratada'] = str(meter['data']['potenciaContratada']) + ' kW'
        self._state = meter['data']['potenciaActual']
        self._attributes = attributes

     def handle_hello(call):
        """Handle the service call."""
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set("hello_service.hello", name)

    hass.services.register(DOMAIN, "hello", handle_hello)   




class EDSSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self,usr,pw):
        """Initialize the sensor."""
        self._state = None
        self._attributes = {}
        self._usr=usr
        self._pw=pw

    @property
    def name(self):
        """Return the name of the sensor."""
        return FRIENDLY_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return "mdi:flash" 

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return POWER_KILO_WATT

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor."""
        edis = Edistribucion(self._usr,self._pw)
        edis.login()
        r = edis.get_cups()
        cups = r['data']['lstCups'][0]['Id']
        meter = edis.get_meter(cups)
        _LOGGER.debug(meter)
        _LOGGER.debug(meter['data']['potenciaActual'])
        attributes = {}
        attributes['CUPS'] = r['data']['lstCups'][0]['Id']
        attributes['Estado ICP'] = meter['data']['estadoICP']
        attributes['Consumo Total'] = str(meter['data']['totalizador']) + ' kWh'
        attributes['Carga actual'] = meter['data']['percent']
        attributes['Potencia Contratada'] = str(meter['data']['potenciaContratada']) + ' kW'
        self._state = meter['data']['potenciaActual']
        self._attributes = attributes

    def reconnect_icp(self, code=None) -> None:
        """Send reconnect ICP command."""
        edis = Edistribucion(self._usr,self._pw)
        edis.login()
        r = edis.get_cups()
        cups = r['data']['lstCups'][0]['Id']
        edis.reconnect_ICP(cups)
        