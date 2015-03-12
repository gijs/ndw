from django.db import models


class MonitoringLocation(models.Model):
    ROAD_SIDE_CHOICES = (
        ('L', 'Left road side'),
        ('R', 'Right road side')
    )

    id_code = models.CharField(max_length=100, null=False, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    lanes_number = models.IntegerField(default=1)
    #for travel time monitoring location
    end_latitude = models.FloatField(null=True)
    end_longitude = models.FloatField(null=True)
    length_affected = models.FloatField(null=True)

    road_code = models.CharField(null=True, max_length=100)
    road_side = models.CharField(null=True, max_length=1, choices=ROAD_SIDE_CHOICES)

    vild_location_id = models.IntegerField(default=0)
    vild_location_offset = models.IntegerField(default=0)


class VehicleClass(models.Model):
    code = models.CharField(max_length=100, null=False, unique=True)
    length_from = models.FloatField()
    length_to = models.FloatField()


class LocationCapability(models.Model):
    LANE_TYPES = (
        ('1', 'Lane 1'),
        ('2', 'Lane 2'),
        ('3', 'Lane 3'),
        ('4', 'Lane 4'),
        ('5', 'Lane 5'),
        ('6', 'Lane 6'),
        ('7', 'Lane 7'),
        ('8', 'Lane 8'),
        ('9', 'Lane 9'),
        ('B', 'Bus lane'),
        ('CR', 'Central reservation lane'),
        ('HS', 'Hard shoulder lane'),
        ('RH', 'Rush hour lane'),
        ('TF', 'Tidal flow lane'),
        ('AL', 'All lanes complete carriageway')
    )

    DB_TO_XML_LOCATION_TYPES = {
        'B': 'busLane',
        'CR': 'centralReservation',
        'HS': 'hardShoulder',
        'RH': 'rushHourLane',
        'TF': 'tidalFlowLane',
        'AL': 'allLanesCompleteCarriageway'
    }

    MEASUREMENT_TYPE_CHOICES = (
        ('trafficSpeed', 'Traffic Speed'),
        ('trafficFlow', 'Traffic Flow'),
        ('travelTimeInformation', 'Travel time information')
    )

    location = models.ForeignKey(MonitoringLocation)
    lane_type = models.CharField(max_length=2, choices=LANE_TYPES)
    capability_index = models.IntegerField()
    measurement_type = models.CharField(max_length=32, choices=MEASUREMENT_TYPE_CHOICES, null=False)
    vehicle_length_from = models.FloatField(null=True)
    vehicle_length_to = models.FloatField(null=True)
    period = models.IntegerField(default=60)
    accuracy = models.FloatField(default=100)

    @staticmethod
    def get_xml_lane_type(db_val):
        if int(db_val) > 0 and int(db_val) < 10:
            return 'lane' + db_val

        if db_val in LocationCapability.DB_TO_XML_LOCATION_TYPES:
            return LocationCapability.DB_TO_XML_LOCATION_TYPES[db_val]

        return ''

    @staticmethod
    def get_db_lane_type(xml_type):
        xml_to_db = {y:x for x,y in LocationCapability.DB_TO_XML_LOCATION_TYPES.iteritems()}

        if 'lane' in xml_type:
            return xml_type[4:]

        if xml_type in xml_to_db:
            return xml_to_db[xml_type]

        return ''


class MeasuredValue(models.Model):
    location_capability = models.ForeignKey(LocationCapability)
    value = models.FloatField()
    input_values_number = models.IntegerField(null=True)
    standard_deviation = models.FloatField(null=True)
    time = models.DateTimeField()