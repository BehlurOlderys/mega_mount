from .MyDeviceDriver import MyDeviceDriver


class SimpleEQMountDriver(MyDeviceDriver):
    def __init__(self, config):
        super().__init__("SimpleEQMountDriver", "minimal equatorial mount")
        self.__config = config
        self.__tracking_rates = [0]
        self.__is_pulse_guiding = False
        self.__declinationrate = 1.0
        self.__doesrefraction = False
        self.__guideratedeclination = 1.0
        self.__guideraterightascension = 1.0
        self.__rightascensionrate = 1.0
        self.__sideofpier = 0
        self.__siteelevation = 0.0
        self.__sitelatitude = 0.0
        self.__sitelongitude = 0.0
        self.__slewsettletime = 0.0
        self.__targetdeclination = 0.0
        self.__targetrightascension = 0.0
        self.__tracking_rate = 0
        self.__utcdate = ""

    @property
    def alignment_mode(self):
        return 0

    @property
    def altitude(self):
        return 0.0

    @property
    def aperture_area(self):
        return 0.0

    @property
    def aperture_diameter(self):
        return 0.0

    @property
    def at_home(self):
        return False

    @property
    def at_park(self):
        return False

    @property
    def azimuth(self):
        return 0.0

    @property
    def can_find_home(self):
        return False

    @property
    def can_park(self):
        return False

    @property
    def can_pulse_guide(self):
        return True

    @property
    def can_set_declination_rate(self):
        return False

    @property
    def can_set_guide_rates(self):
        return False

    @property
    def can_set_pier_side(self):
        return False

    @property
    def can_set_right_ascension_rate(self):
        return False

    @property
    def can_set_tracking(self):
        return True

    @property
    def can_slew(self):
        return True

    @property
    def can_slew_alt_az(self):
        return False

    @property
    def can_slew_alt_az_async(self):
        return False

    @property
    def can_slew_async(self):
        return False

    @property
    def can_sync(self):
        return False

    @property
    def can_sync_alt_az(self):
        return False

    @property
    def declination(self):
        return 0.0

    @property
    def declination_rate(self):
        return self.__declinationrate

    @property
    def does_refraction(self):
        return False

    @property
    def equatorial_system(self):
        return 0

    @property
    def focal_length(self):
        return 0.0

    @property
    def guide_rate_declination(self):
        return self.__guideratedeclination

    @property
    def guide_rate_right_ascension(self):
        return self.__guideraterightascension

    @property
    def is_pulse_guiding(self):
        return self.__is_pulse_guiding

    @property
    def right_ascension(self):
        return 0.0

    @property
    def right_ascension_rate(self):
        return self.__rightascensionrate

    @property
    def side_of_pier(self):
        return -1

    @property
    def sidereal_time(self):
        return 0.0

    @property
    def site_elevation(self):
        return 0.0

    @property
    def site_latitude(self):
        return 0.0

    @property
    def site_longitude(self):
        return 0.0

    @property
    def slewing(self):
        return False

    @property
    def slew_settle_time(self):
        return 0.0

    @property
    def target_declination(self):
        return 0.0

    @property
    def target_right_ascension(self):
        return 0.0

    @property
    def tracking(self):
        return False

    @property
    def tracking_rate(self):
        return self.__tracking_rate

    @property
    def tracking_rates(self):
        return self.__tracking_rates

    @property
    def utc_date(self):
        return 0.0

    def axis_rates(self, axis):
        rates = [
                    [
                        { "Maximum": 5.0, "Minimum": 1.0}
                    ],
                    [
                        { "Maximum": 3.0, "Minimum": 2.0},
                    ]
                ]
        return rates[axis]

    def can_move_axis(self, axis_number):
        print("Can move axis: " + str(axis_number) + "?")
        return axis_number < 2

    @property
    def destination_side_of_pier(self):
        return -1

    ##################################
    # COMMANDS AND INPUTS:
    ##################################

    @declination_rate.setter
    def declination_rate(self, value):
        self.__declinationrate = value

    @does_refraction.setter
    def doesrefraction(self, value):
        self.__doesrefraction = value

    @guide_rate_declination.setter
    def guideratedeclination(self, value):
        self.__guideratedeclination = value

    @guide_rate_right_ascension.setter
    def guideraterightascension(self, value):
        self.__guideraterightascension = value

    @right_ascension_rate.setter
    def rightascensionrate(self, value):
        self.__rightascensionrate = value

    @side_of_pier.setter
    def sideofpier(self, value):
        self.__sideofpier = value

    @site_elevation.setter
    def siteelevation(self, value):
        self.__siteelevation = value

    @site_latitude.setter
    def sitelatitude(self, value):
        self.__sitelatitude = value

    @site_longitude.setter
    def sitelongitude(self, value):
        self.__sitelongitude = value

    @slew_settle_time.setter
    def slewsettletime(self, value):
        self.__slewsettletime = value

    @target_declination.setter
    def targetdeclination(self, value):
        self.__targetdeclination = value

    @target_right_ascension.setter
    def targetrightascension(self, value):
        self.__targetrightascension = value

    @tracking.setter
    def tracking(self, value):
        print(f"Base class setting tracking to {value}")

    @tracking_rate.setter
    def tracking_rate(self, value):
        self.__tracking_rate = value

    @utc_date.setter
    def utcdate(self, value):
        self.__utcdate = value

    def abortslew(self):
        print("abort slew")
        # TODO
        pass

    def findhome(self):
        print("find home")
        # TODO
        pass

    def moveaxis(self, axis, rate):
        print("Moving axis " + str(axis) + " at rate " + str(rate))
        pass

    def park(self):
        print("park")
        # TODO:
        pass

    def pulseguide(self, direction, duration):
        print("pulse guide")
        # TODO
        pass

    def setpark(self):
        print("set park")
        # TODO
        pass

    def slewtoaltaz(self, altitude, azimuth):
        print("slew to alt/az")
        # TODO
        pass

    def slewtoaltazasync(self, altitude, azimuth):
        print("slew to alt/az async")
        # TODO
        pass

    def slewtocoordinates(self, right_ascension, declination):
        print("slew to ra/dec")
        # TODO
        pass

    def slewtocoordinatesasync(self, right_ascension, declination):
        print("slew to ra/dec async")
        # TODO
        pass

    def slewtotarget(self):
        print("slew to target")
        # TODO
        pass

    def slewtotargetasync(self):
        print("slew to target async")
        # TODO
        pass

    def synctoaltaz(self, altitude, azimuth):
        print("sync to alt/az")
        # TODO
        pass

    def synctocoordinates(self, right_ascension, declination):
        print("sync to ra/dec")
        # TODO
        pass

    def synctotarget(self):
        print("sync to target")
        # TODO
        pass

    def unpark(self):
        print("unparking")
        # TODO
        pass
