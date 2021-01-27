from .MyDeviceDriver import MyDeviceDriver


class SimpleEQMountDriver(MyDeviceDriver):
    def __init__(self, config):
        super().__init__("SimpleEQMountDriver", "minimal equatorial mount")
        self.__config = config
        self.__tracking = False
        self.__tracking_rate = 0
        self.__tracking_rates = [0]
        self.__is_pulse_guiding = False

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
        return False

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
        return 0.0

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
        return 0.0

    @property
    def guide_rate_right_ascension(self):
        return 0.0

    @property
    def is_pulse_guiding(self):
        return self.__is_pulse_guiding

    @property
    def right_ascension(self):
        return 0.0

    @property
    def right_ascension_rate(self):
        return 0.0

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
        return self.__tracking

    @property
    def tracking_rate(self):
        return self.__tracking_rate

    @property
    def tracking_rates(self):
        return self.__tracking_rates

    @property
    def utc_date(self):
        return 0.0

    @property
    def axis_rates(self):
        return [
            { "Maximum": 0, "Minimum": 0},
            { "Maximum": 0, "Minimum": 0},
            { "Maximum": 0, "Minimum": 0}
        ]

    def can_move_axis(self, axis_number):
        print("Can move axis: " + str(axis_number) + "?")
        return axis_number < 2

    @property
    def destination_side_of_pier(self):
        return -1

    @tracking.setter
    def tracking(self, value):
        self.__tracking = value

    @tracking_rate.setter
    def tracking_rate(self, value):
        self.__tracking_rate = value
