from .models import Address, Coordinate, Distance
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal
import math

class MAP_Func:
    # def __init__(self):
    #     super().__init__()

    @classmethod
    def saveAddress(cls, address:str, long:Decimal, lat:Decimal)-> Address:
        try:
            addr = Address.objects.get(address=address)
        except ObjectDoesNotExist:
            addr = None
        if addr:
            return addr
        try:
            addr = Address.objects.create(address=address, longitude=long, latitude=lat)
        except DatabaseError:
            return None
        return addr
    
    @classmethod
    def twoPointsDistance(cls, point_A: Coordinate,point_B: Coordinate)-> Decimal:
        
        try:
            distance = Distance.objects.get(point_A=point_A,point_B=point_B)
        except ObjectDoesNotExist:
            distance = None
        return distance.distance
    
    @classmethod
    def twoPointsDistance(cls, new_point: [],exist_p: Coordinate)-> Decimal:
        
        lat1, lon1 = new_point
        lat1 = Decimal(lat1)
        lon1 = Decimal(lon1)
        lat2, lon2 = exist_p.latitude, exist_p.longitude
        return math.sqrt( (lat1 - lat2)**2 + (lon1 - lon2)**2 )

        # R = 6372800  # Earth radius in meters
        # a = math.sin(dphi/2)**2 + \
        # math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        # return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a)) #Unit: meters

    @classmethod
    def findNearPointAndSave(cls, point: Address, max_radius=50 )-> Coordinate:
        
        # 1° = 111 km  (or 60 nautical miles)
        # 0.1° = 11.1 km 
        # 0.001° =111 m 
        # 0.00001° = 1.11 m 
        # 0.000001° = 0.11 m (7 decimals, cm accuracy)

        degree = max_radius/111*0.001 #Meters to Degree

        all_coors = Coordinate.objects.all()
        lat, lon = point.latitude, point.longitude
        found = None
        for coor in all_coors:
            distance = MAP_Func.twoPointsDistance([lat,lon], coor)
            if distance < max_radius:
                found =coor
                break
        if not found:
            coor = Coordinate.objects.create(longitude= lon, latitude=lat)
            found =coor
        point.idCoordinate = found
        point.save()
        return found

    @classmethod
    def saveDistance(cls, point_A: Coordinate,point_B: Coordinate, distance:Decimal):
        Distance.objects.create(point_A=point_A, point_B=point_B, distance=distance)       
        return


