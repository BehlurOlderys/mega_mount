from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from .device_service import DeviceService
from .config import getDriverInstance


class SimpleTelescopeService(DeviceService):
    @get(_path="/api/v1/{device_type}/{device_number}/alignmentmode", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def alignment_mode(self, device_type, device_number):
        super().get_resource(device_type, device_number, "alignment_mode")

    @get(_path="/api/v1/{device_type}/{device_number}/altitude", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def altitude(self, device_type, device_number):
        super().get_resource(device_type, device_number, "altitude")

    @get(_path="/api/v1/{device_type}/{device_number}/aperturearea", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def aperture_area(self, device_type, device_number):
        super().get_resource(device_type, device_number, "aperture_area")

    @get(_path="/api/v1/{device_type}/{device_number}/aperturediameter", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def aperture_diameter(self, device_type, device_number):
        super().get_resource(device_type, device_number, "aperture_diameter")

    @get(_path="/api/v1/{device_type}/{device_number}/athome", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def at_home(self, device_type, device_number):
        super().get_resource(device_type, device_number, "at_home")

    @get(_path="/api/v1/{device_type}/{device_number}/atpark", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def at_park(self, device_type, device_number):
        super().get_resource(device_type, device_number, "at_park")

    @get(_path="/api/v1/{device_type}/{device_number}/azimuth", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def azimuth(self, device_type, device_number):
        super().get_resource(device_type, device_number, "azimuth")

    @get(_path="/api/v1/{device_type}/{device_number}/canfindhome", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_find_home(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_find_home")

    @get(_path="/api/v1/{device_type}/{device_number}/canpark", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_park(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_park")

    @get(_path="/api/v1/{device_type}/{device_number}/canpulseguide", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_pulse_guide(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_pulse_guide")

    @get(_path="/api/v1/{device_type}/{device_number}/cansetdeclination_rate", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_set_declination_rate(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_set_declination_rate")

    @get(_path="/api/v1/{device_type}/{device_number}/cansetguiderates", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_set_guide_rates(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_set_guide_rates")

    @get(_path="/api/v1/{device_type}/{device_number}/cansetpierside", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_set_pier_side(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_set_pier_side")

    @get(_path="/api/v1/{device_type}/{device_number}/cansetrightascensionrate", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_set_right_ascension_rate(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_set_right_ascension_rate")

    @get(_path="/api/v1/{device_type}/{device_number}/cansettracking", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_set_tracking(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_set_tracking")

    @get(_path="/api/v1/{device_type}/{device_number}/canslew", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_slew(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_slew")

    @get(_path="/api/v1/{device_type}/{device_number}/canslewaltaz", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_slew_alt_az(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_slew_alt_az")

    @get(_path="/api/v1/{device_type}/{device_number}/canslewaltazasync", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_slew_alt_az_async(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_slew_alt_az_async")

    @get(_path="/api/v1/{device_type}/{device_number}/canslewasync", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_slew_async(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_slew_async")

    @get(_path="/api/v1/{device_type}/{device_number}/cansync", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_sync(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_sync")

    @get(_path="/api/v1/{device_type}/{device_number}/cansyncaltaz", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_sync_alt_az(self, device_type, device_number):
        super().get_resource(device_type, device_number, "can_sync_alt_az")

    @get(_path="/api/v1/{device_type}/{device_number}/declination", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def declination(self, device_type, device_number):
        super().get_resource(device_type, device_number, "declination")

    @get(_path="/api/v1/{device_type}/{device_number}/declinationrate", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def declination_rate(self, device_type, device_number):
        super().get_resource(device_type, device_number, "declination_rate")

    @get(_path="/api/v1/{device_type}/{device_number}/doesrefraction", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def does_refraction(self, device_type, device_number):
        super().get_resource(device_type, device_number, "does_refraction")

    @get(_path="/api/v1/{device_type}/{device_number}/equatorialsystem", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def equatorial_system(self, device_type, device_number):
        super().get_resource(device_type, device_number, "equatorial_system")

    @get(_path="/api/v1/{device_type}/{device_number}/focallength", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def focal_length(self, device_type, device_number):
        super().get_resource(device_type, device_number, "focal_length")

    @get(_path="/api/v1/{device_type}/{device_number}/guideratedeclination", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def guide_rate_declination(self, device_type, device_number):
        super().get_resource(device_type, device_number, "guide_rate_declination")

    @get(_path="/api/v1/{device_type}/{device_number}/guideraterightascension", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def guide_rate_right_ascension(self, device_type, device_number):
        super().get_resource(device_type, device_number, "guide_rate_right_ascension")

    @get(_path="/api/v1/{device_type}/{device_number}/ispulseguiding", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def is_pulse_guiding(self, device_type, device_number):
        super().get_resource(device_type, device_number, "is_pulse_guiding")

    @get(_path="/api/v1/{device_type}/{device_number}/rightascension", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def right_ascension(self, device_type, device_number):
        super().get_resource(device_type, device_number, "right_ascension")

    @get(_path="/api/v1/{device_type}/{device_number}/rightascensionrate", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def right_ascension_rate(self, device_type, device_number):
        super().get_resource(device_type, device_number, "right_ascension_rate")

    @get(_path="/api/v1/{device_type}/{device_number}/sideofpier", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def side_of_pier(self, device_type, device_number):
        super().get_resource(device_type, device_number, "side_of_pier")

    @get(_path="/api/v1/{device_type}/{device_number}/siderealtime", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def sidereal_time(self, device_type, device_number):
        super().get_resource(device_type, device_number, "sidereal_time")

    @get(_path="/api/v1/{device_type}/{device_number}/siteelevation", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def site_elevation(self, device_type, device_number):
        super().get_resource(device_type, device_number, "site_elevation")

    @get(_path="/api/v1/{device_type}/{device_number}/sitelatitude", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def site_latitude(self, device_type, device_number):
        super().get_resource(device_type, device_number, "site_latitude")

    @get(_path="/api/v1/{device_type}/{device_number}/sitelongitude", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def site_longitude(self, device_type, device_number):
        super().get_resource(device_type, device_number, "site_longitude")

    @get(_path="/api/v1/{device_type}/{device_number}/slewing", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def slewing(self, device_type, device_number):
        super().get_resource(device_type, device_number, "slewing")

    @get(_path="/api/v1/{device_type}/{device_number}/slewsettletime", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def slew_settle_time(self, device_type, device_number):
        super().get_resource(device_type, device_number, "slew_settle_time")

    @get(_path="/api/v1/{device_type}/{device_number}/targetdeclination", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def target_declination(self, device_type, device_number):
        super().get_resource(device_type, device_number, "target_declination")

    @get(_path="/api/v1/{device_type}/{device_number}/targetrightascension", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def target_right_ascension(self, device_type, device_number):
        super().get_resource(device_type, device_number, "target_right_ascension")

    @get(_path="/api/v1/{device_type}/{device_number}/tracking", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def tracking(self, device_type, device_number):
        super().get_resource(device_type, device_number, "tracking")

    @get(_path="/api/v1/{device_type}/{device_number}/trackingrate", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def tracking_rate(self, device_type, device_number):
        super().get_resource(device_type, device_number, "tracking_rate")

    @get(_path="/api/v1/{device_type}/{device_number}/trackingrates", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def tracking_rates(self, device_type, device_number):
        super().get_resource(device_type, device_number, "tracking_rates")

    @get(_path="/api/v1/{device_type}/{device_number}/utcdate", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def utc_date(self, device_type, device_number):
        super().get_resource(device_type, device_number, "utc_date")

    @get(_path="/api/v1/{device_type}/{device_number}/axisrates", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def axis_rates(self, device_type, device_number):
        axis = super().get_query_argument_for_get_request("Axis")
        super().get_resource(device_type, device_number, "axis_rates", int(axis))

    @get(_path="/api/v1/{device_type}/{device_number}/canmoveaxis", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def can_move_axis(self, device_type, device_number):
        axis = super().get_query_argument_for_get_request("Axis")
        super().get_resource(device_type, device_number, "can_move_axis", int(axis))

    @get(_path="/api/v1/{device_type}/{device_number}/destinationsideofpier", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def destination_side_of_pier(self, device_type, device_number):
        super().get_resource(device_type, device_number, "destination_side_of_pier")


    #####################
    # PUT METHODS: TODO TODO TODO !!!!!!!!!!
    #####################

    @put(_path="/api/v1/{device_type}/{device_number}/declinationrate", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def set_declination_rate(self, device_type, device_number):
        super().set_one_float_resource(device_type, device_number, "DeclinationRate", "declination_rate")


    # @declinationrate.setter
    # def declination_rate(self, value):
    #     self.__declinationrate = value
    #
    # @doesrefraction.setter
    # def doesrefraction(self, value):
    #     self.__doesrefraction = value
    #
    # @guideratedeclination.setter
    # def guideratedeclination(self, value):
    #     self.__guideratedeclination = value
    #
    # @guideraterightascension.setter
    # def guideraterightascension(self, value):
    #     self.__guideraterightascension = value
    #
    # @rightascensionrate.setter
    # def rightascensionrate(self, value):
    #     self.__rightascensionrate = value
    #
    # @sideofpier.setter
    # def sideofpier(self, value):
    #     self.__sideofpier = value
    #
    # @siteelevation.setter
    # def siteelevation(self, value):
    #     self.__siteelevation = value
    #
    # @sitelatitude.setter
    # def sitelatitude(self, value):
    #     self.__sitelatitude = value
    #
    # @sitelongitude.setter
    # def sitelongitude(self, value):
    #     self.__sitelongitude = value
    #
    # @slewsettletime.setter
    # def slewsettletime(self, value):
    #     self.__slewsettletime = value
    #
    # @targetdeclination.setter
    # def targetdeclination(self, value):
    #     self.__targetdeclination = value
    #
    # @targetrightascension.setter
    # def targetrightascension(self, value):
    #     self.__targetrightascension = value
    #

    @put(_path="/api/v1/{device_type}/{device_number}/tracking", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def set_tracking(self, device_type, device_number):
        super().set_one_boolean_resource(device_type, device_number, "Tracking", "tracking")

    @put(_path="/api/v1/{device_type}/{device_number}/trackingrate", _types=[str, str],
         _produces=mediatypes.APPLICATION_JSON)
    def set_tracking_rate(self, device_type, device_number):
        super().set_one_integer_resource(device_type, device_number, "TrackingRate", "tracking_rate")
    #
    # @utcdate.setter
    # def utcdate(self, value):
    #     self.__utcdate = value
    #
    @put(_path="/api/v1/{device_type}/{device_number}/abortslew", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def abortslew(self, device_type, device_number):
        super().standard_response_for_put(device_type, device_number, lambda driver: driver.abortslew())
    #
    # def findhome(self):
    #     # TODO
    #     pass

    @put(_path="/api/v1/{device_type}/{device_number}/moveaxis", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def move_axis(self, device_type, device_number):
        [axis, rate] = super().get_string_values_from_put_request("Axis", "Rate")
        super().standard_response_for_put(device_type, device_number, lambda driver: driver.moveaxis(axis, rate))

    # def park(self):
    #     # TODO:
    #     pass
    #
    # def pulseguide(self, direction, duration):
    #     # TODO
    #     pass
    #
    # def setpark(self):
    #     # TODO
    #     pass
    #
    # def slewtoaltaz(self, altitude, azimuth):
    #     # TODO
    #     pass
    #
    # def slewtoaltazasync(self, altitude, azimuth):
    #     # TODO
    #     pass
    #
    # def slewtocoordinates(self, right_ascension, declination):
    #     # TODO
    #     pass
    #
    # def slewtocoordinatesasync(self, right_ascension, declination):
    #     # TODO
    #     pass
    #
    # def slewtotarget(self):
    #     # TODO
    #     pass
    #
    # def slewtotargetasync(self):
    #     # TODO
    #     pass
    #
    # def synctoaltaz(self, altitude, azimuth):
    #     # TODO
    #     pass
    #
    # def synctocoordinates(self, right_ascension, declination):
    #     # TODO
    #     pass
    #
    # def synctotarget(self):
    #     # TODO
    #     pass
    #
    # def unpark(self):
    #     # TODO
    #     pass


# def alignment_mode(self):
# def altitude(self):
# def aperture_area(self):
# def aperture_diameter(self):
# def at_home(self):
# def at_park(self):
# def azimuth(self):
# def can_find_home(self):
# def can_park(self):
# def can_pulse_guide(self):
# def can_set_declination_rate(self):
# def can_set_guide_rates(self):
# def can_set_pier_side(self):
# def can_set_right_ascension_rate(self):
# def can_set_tracking(self):
# def can_slew(self):
# def can_slew_alt_az(self):
# def can_slew_alt_az_async(self):
# def can_slew_async(self):
# def can_sync(self):
# def can_sync_alt_az(self):
# def declination(self):
# def declination_rate(self):
# def does_refraction(self):
# def equatorial_system(self):
# def focal_length(self):
# def guide_rate_declination(self):
# def guide_rate_right_ascension(self):
# def is_pulse_guiding(self):
# def right_ascension(self):
# def right_ascension_rate(self):
# def side_of_pier(self):
# def sidereal_time(self):
# def site_elevation(self):
# def site_latitude(self):
# def site_longitude(self):
# def slewing(self):
# def slew_settle_time(self):
# def target_declination(self):
# def target_right_ascension(self):
# def tracking(self):
# def tracking_rate(self):
# def tracking_rates(self):
# def utc_date(self):
# def axis_rates(self):
# def can_move_axis(self, axis_number):
# def destination_side_of_pier(self):
#


# def alignmentmode(self):
# def altitude(self):
# def aperturearea(self):
# def aperturediameter(self):
# def athome(self):
# def atpark(self):
# def azimuth(self):
# def canfindhome(self):
# def canpark(self):
# def canpulseguide(self):
# def cansetdeclinationrate(self):
# def cansetguiderates(self):
# def cansetpierside(self):
# def cansetrightascensionrate(self):
# def cansettracking(self):
# def canslew(self):
# def canslewaltaz(self):
# def canslewaltazasync(self):
# def canslewasync(self):
# def cansync(self):
# def cansyncaltaz(self):
# def declination(self):
# def declinationrate(self):
# def doesrefraction(self):
# def equatorialsystem(self):
# def focallength(self):
# def guideratedeclination(self):
# def guideraterightascension(self):
# def ispulseguiding(self):
# def rightascension(self):
# def rightascensionrate(self):
# def sideofpier(self):
# def siderealtime(self):
# def siteelevation(self):
# def sitelatitude(self):
# def sitelongitude(self):
# def slewing(self):
# def slewsettletime(self):
# def targetdeclination(self):
# def targetrightascension(self):
# def tracking(self):
# def trackingrate(self):
# def trackingrates(self):
# def utcdate(self):
# def axisrates(self):
# def canmoveaxis(self, axisnumber):
# def destinationsideofpier(self):