class RoadWay:
    """
    路基断面信息
    """

    def __init__(
            self,
            l_width: float,
            r_width: float,
            l_level: float,
            r_level: float,
    ):
        self.width = (l_width, r_width)
        self.level = (l_level, r_level)