import lxml.etree as ET
import os, time, hashlib, glob, urllib, os.path,re
from models import MonitoringLocation, LocationCapability, MeasuredValue
from datetime import datetime

from django.core import serializers


def parse_sites_measurements(file_path="F:/django/ndw/ndw/data/trafficspeed.xml"):
    schema = '{http://datex2.eu/schema/2/2_0}'
    tags = {
        'site_measurements': schema + 'siteMeasurements',
        'measurements_site': schema + 'measurementSiteReference',
        'measurement_time': schema + 'measurementTimeDefault',
        'measured_value': schema + 'measuredValue',
        'value_error': schema + 'dataError',
        'basic_data': schema + 'basicData',
        'avg_speed': schema + 'averageVehicleSpeed',
        'speed': schema + 'speed',
        'flow_rate': schema + 'vehicleFlowRate'
    }
    ids = []

    for event, element in ET.iterparse(file_path, tag=tags['site_measurements']):
        measurements_site = element.find(tags['measurements_site'])
        id = measurements_site.attrib['id']
        location = MonitoringLocation.objects.get(id_code=measurements_site.attrib['id'])
        timestamp = datetime.fromtimestamp(time.mktime(time.strptime(element.find(tags['measurement_time']).text, '%Y-%m-%dT%H:%M:%SZ')))
        measuredValues = []
        for measurement in element.findall(tags['measured_value']):
            error = measurement.find('.//' + tags['value_error'])
            if error is not None:
                continue

            measuredValue = MeasuredValue(time=timestamp)
            basic_data = measurement.find('.//' + tags['basic_data'])
            data_type = basic_data.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
            if data_type == 'TrafficSpeed':
                avg_speed = basic_data.find(tags['avg_speed'])
                if 'standardDeviation' in avg_speed.attrib:
                    measuredValue.standard_deviation = avg_speed.attrib['standardDeviation']
                if 'numberOfInputValuesUsed' in avg_speed.attrib:
                    if int(avg_speed.attrib['numberOfInputValuesUsed']) == 0:
                        continue
                    measuredValue.input_values_number = avg_speed.attrib['numberOfInputValuesUsed']
                measuredValue.value = avg_speed.find(tags['speed']).text
            elif data_type == 'TrafficFlow':
                measuredValue.value = basic_data.find('.//' + tags['flow_rate']).text
            location_capability = LocationCapability.objects.get(
                capability_index=measurement.attrib['index'],
                location=location
            )
            if location_capability:
                measuredValue.location_capability = location_capability
                measuredValues.append(measuredValue)

        MeasuredValue.objects.bulk_create(measuredValues)


def parse_measurement_sites(file_path, process_capabilities=False, update=False):
    #F:/django/ndw/ndw/data/measurement.xml
    schema = '{http://datex2.eu/schema/2/2_0}'
    tags = {
        'location_name': schema + 'measurementSiteName',
        'vild_location_id': schema + 'specificLocation',
        'vild_location_offset': schema + 'offsetDistance',
        'vild_location_offset_direction': schema + 'alertCDirectionCoded'
    }

    directions = {}

    for event, element in ET.iterparse(file_path, tag="{http://datex2.eu/schema/2/2_0}measurementSiteRecord"):
        id = element.attrib['id']
        try:
            location = MonitoringLocation.objects.get(id_code=id)
        except MonitoringLocation.DoesNotExist:
            location = MonitoringLocation.objects.create(
                id_code=element.attrib['id'],
                latitude=element.find('.//{http://datex2.eu/schema/2/2_0}latitude').text,
                longitude=element.find('.//{http://datex2.eu/schema/2/2_0}longitude').text,
                lanes_number = element.find('.//{http://datex2.eu/schema/2/2_0}measurementSiteNumberOfLanes').text
            )

        location.vild_location_id = element.find('.//' + tags['vild_location_id']).text
        location.vild_location_offset = int(element.findall('.//' + tags['vild_location_offset'])[1].text)
        if element.find('.//' + tags['vild_location_offset_direction']).text == 'negative':
             location.vild_location_offset *= -1

        print location.vild_location_id, location.vild_location_offset

        # if direction is not None:
        #     if direction.text == 'positive':
        #         location.road_side = 'R'
        #     else:
        #         location.road_side = 'L'

        name = element.find(tags['location_name'])
        name = name.find('.//' + schema + 'value').text
        road_pattern = re.compile('\A(?P<road_code>[A-Z][0-9]{1,3})(?P<direction>[L|R|l|r])?\s')
        reg_ex_result = road_pattern.match(name)
        if reg_ex_result is not None:
            location.road_code = reg_ex_result.group('road_code')
            if reg_ex_result.group('direction'):
                location.road_side = reg_ex_result.group('direction').upper()

            print name, location.road_code, location.road_side


        location.lanes_number = element.find('.//{http://datex2.eu/schema/2/2_0}measurementSiteNumberOfLanes').text
        linear_ext = element.find('.//{http://datex2.eu/schema/2/2_0}linearExtension')

        if linear_ext is not None:
            lats = linear_ext.findall('.//{http://datex2.eu/schema/2/2_0}latitude')
            lngs = linear_ext.findall('.//{http://datex2.eu/schema/2/2_0}longitude')
            location.latitude = lats[0].text
            location.end_latitude = lats[1].text
            location.longitude = lngs[0].text
            location.end_longitude = lngs[1].text
            location.length_affected = element.find('.//{http://datex2.eu/schema/2/2_0}lengthAffected').text

        if process_capabilities:
            capabilities = []
            for spec_characteristic in element.findall('{http://datex2.eu/schema/2/2_0}measurementSpecificCharacteristics'):
                capability = LocationCapability(
                    location=location,
                    capability_index=spec_characteristic.attrib['index'],
                    measurement_type=spec_characteristic.find('.//{http://datex2.eu/schema/2/2_0}specificMeasurementValueType').text,
                    period=int(float(spec_characteristic.find('.//{http://datex2.eu/schema/2/2_0}period').text)),
                    accuracy=int(float(spec_characteristic.find('.//{http://datex2.eu/schema/2/2_0}accuracy').text))
                )

                lane_type = spec_characteristic.find('.//{http://datex2.eu/schema/2/2_0}specificLane')
                if lane_type is None:
                    lane_type = 'allLanesCompleteCarriageway'
                else:
                    lane_type = lane_type.text
                capability.lane_type = LocationCapability.get_db_lane_type(lane_type)

                vehicle_char = spec_characteristic.find('.//{http://datex2.eu/schema/2/2_0}specificVehicleCharacteristics')
                if vehicle_char.find('{http://datex2.eu/schema/2/2_0}vehicleType') is None:
                    lengths = vehicle_char.findall('{http://datex2.eu/schema/2/2_0}lengthCharacteristic')
                    if len(lengths) == 1:
                        if 'less' in lengths[0].find('{http://datex2.eu/schema/2/2_0}comparisonOperator').text:
                            capability.vehicle_length_to = lengths[0].find('{http://datex2.eu/schema/2/2_0}vehicleLength').text
                        else:
                            capability.vehicle_length_from = lengths[0].find('{http://datex2.eu/schema/2/2_0}vehicleLength').text
                    else:
                        capability.vehicle_length_from = lengths[0].find('{http://datex2.eu/schema/2/2_0}vehicleLength').text
                        capability.vehicle_length_to = lengths[1].find('{http://datex2.eu/schema/2/2_0}vehicleLength').text
                capabilities.append(capability)

            if update:
                LocationCapability.objects.bulk_create(capabilities)

        if update:
            location.save()

        element.clear()


def download_from_server():
    protocol = 'ftp'
    host = "83.247.110.3"
    files_ext = 'gz'
    file_names = [
        'trafficspeed',
        'traveltime'
    ]
    data_folder = 'F:/django/ndw/ndw/data/'

    for file_name in file_names:
        file_url = protocol + '://' + host + '/' + file_name + '.' + files_ext
        file_save_path_tmp = data_folder + 'tmp_' + file_name + '.' + files_ext

        urllib.urlretrieve(file_url, file_save_path_tmp)
        file_hash = hash_file(open(file_save_path_tmp, 'rb'), hashlib.md5())
        file_save_path = data_folder + file_name + '_' + file_hash + '.' + files_ext
        previous_file_name = get_newest_file(data_folder, file_name)
        previous_file_hash = None
        if previous_file_name is not None:
            previous_file_hash = os.path.basename(previous_file_name).split('.')[0].split('_')[1]
        if previous_file_hash is None or previous_file_hash != file_hash:
            print 'written file: %s' % (file_save_path)
            os.rename(file_save_path_tmp, file_save_path)
        else:
            print 'file for %s is already written' % (file_name)
            os.remove(file_save_path_tmp)


def hash_file(file, hashing_func, block_size=65536):
    buf = file.read(block_size)
    while len(buf) > 0:
        hashing_func.update(buf)
        buf = file.read(block_size)
    return hashing_func.hexdigest()

def get_newest_file(folder, filename):
    files = glob.iglob(folder + filename + '*.gz')
    try:
        return max(files, key=os.path.getctime)
    except:
        return None

def export_locations_json():
    #json = serializers.serialize('json', MonitoringLocation.objects.all())
    save_file = open('F:/django/ndw/ndw/data/locations.txt', 'w')
    lines = [str(location.latitude) + ';' + str(location.longitude) for location in MonitoringLocation.objects.all()]
    save_file.writelines('\n'.join(lines))
