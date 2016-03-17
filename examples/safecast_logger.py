#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log measurements to Safecast open-data API (https://api.safecast.org).

Require the SafecastPy packages:
    https://github.com/MonsieurV/SafecastPy
You'll also need a Safecast API key:
    https://api.safecast.org/en-US/users/sign_up

Released under MIT License. See LICENSE file.

By Yoan Tournade <yoan@ytotech.com>
"""
from PiPocketGeiger import RadiationWatch
import time
import datetime
import SafecastPy

# Safecast API key.
API_KEY = 'your_api_key'
# Log on production or development instance.
SAFECAST_INSTANCE = SafecastPy.DEVELOPMENT_API_URL
# Radiation Watch Pocket Geiger is registered:
# - As device id 90 on developement instance
#   http://dev.safecast.org/en-US/devices/90
# - As device id 145 on production instance
#   https://api.safecast.org/en-US/devices/145
DEVICE_ID = 90

# Your location name.
MY_LOCATION_NAME = "(A Rue du Grand Ferré, Compiègne, France)"
# Your exact location.
MY_LOCATION = {
    'latitude': 49.418683,
    'longitude': 2.823469
}

# Period for publishing on Safecast API, in minutes.
# Five minutes is fine for background monitoring.
LOGGING_PERIOD = 5

if __name__ == "__main__":
    print("Logging each {0} minutes.".format(LOGGING_PERIOD))
    safecast = SafecastPy.SafecastPy(api_key=API_KEY, api_url=SAFECAST_INSTANCE)
    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            # Sleep first so we can sample enough data to stabilize results.
            time.sleep(LOGGING_PERIOD)
            try:
                readings = radiationWatch.status()
                print("Logging... {0}.".format(readings))
                measurement = safecast.add_measurement(json={
                    'latitude': MY_LOCATION['latitude'],
                    'longitude': MY_LOCATION['longitude'],
                    'value': readings['uSvh'],
                    'unit': SafecastPy.UNIT_USV,
                    'captured_at': datetime.datetime.utcnow().isoformat() + '+00:00',
                    'device_id': DEVICE_ID,
                    'location_name': MY_LOCATION_NAME
                })
                print("Ok. Measurement published with id {0}".format(
                    measurement['id']))
            except Exception as e:
                # A catch-all to keep the thing alive even if we have transient
                # network or service errors.
                print(e)
