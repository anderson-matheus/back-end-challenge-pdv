from geojson import MultiPolygon

class MultiPolygonUtil:
    def convert_multi_polygon(self, coverage_areas):
        try:
            multi_polygon = list()
            for coverage_area in coverage_areas:
                multi_polygon.append([self.format_polygon(coverage_area)])

            coordinates_multi_polygon = MultiPolygon(multi_polygon)
            return coordinates_multi_polygon
        except:
            return MultiPolygon([[[3.78, 9.28],
                [-130.91, 1.52]]]) # multi_polygon invalid

    def format_polygon(self, coverage_area):
        polygons = list()
        for d in coverage_area.split(';'):
            polygons.append([float(i) for i in  d.split(',')])
        return polygons
