from geojson import Point

class PointUtil:
    def convert_point(self, coordinate):
        try:
            point = list()
            coordinate = coordinate.split(',')
            point.append([float(i) for i in coordinate])
            return Point(point[0])
        except:
            return Point((-3.68,40.41,25.14,10.34)) # point invalid
