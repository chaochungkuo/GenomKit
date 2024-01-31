from genomkit.genomic_region_set import Coordinate, Coordinates


class ParserBED:
    def __init__(self):
        pass

    def load(self, filename):
        res = Coordinates()
        with open(filename, 'r') as file:
            for line in file:
                if not line.startswith("#"):
                    infos = line.strip().split()
                    res.add(Coordinate(sequence=infos[0],
                                       start=int(infos[1]), end=int(infos[2]),
                                       orientation=infos[5],
                                       name=infos[3], score=infos[4]))
        return res
