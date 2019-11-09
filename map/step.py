from constants.maneuver import get_by_key


class Step():
    """
    ルートの各ステップを表現するクラス
    """

    def __init__(self, step):
        self.step = step

    def get_distance_meter(self):
        return float(self.step['distance']['value'])

    def get_duration_second(self):
        return float(self.step['duration']['value'])

    def get_start_location(self):
        return self.step['start_location']

    def get_end_location(self):
        return self.step['end_location']

    def get_maneuver(self):
        """
        動作タイプを取得

        Returns
        -------------
        maneuver: Maneuver
            動作タイプenum
        """
        if 'maneuver' in self.step:
            return get_by_key(self.step['maneuver'])
        else:
            return ""
