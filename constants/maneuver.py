
from enum import Enum


def get_by_key(key):
    """
    ケバブケースの文字列から動作タイプを取得する。定義されていない場合は Maneuver.STRAIGHT を返す
    """
    for man in Maneuver:
        if key == man.to_kebab_case():
            return man
    return Maneuver.STRAIGHT


class Maneuver(Enum):
    """
    右左折などの動作タイプを定義
    """

    STRAIGHT = 0

    TURN_SLIGHT_RIGHT = 1

    TURN_RIGHT = 10

    TURN_SHARP_RIGHT = 20

    UTURN_RIGHT = 30

    RUMP_RIGHT = 40

    FORK_RIGHT = 50

    TURN_SLIGHT_LEFT = -1

    TURN_LEFT = -10

    TURN_SHARP_LEFT = -20

    UTURN_LEFT = -30

    RUMP_LEFT = -40

    FORK_LEFT = -50

    def to_string(self):
        """
        動作タイプ名称だけの文字列にして返す
        """
        return str(self).replace('Maneuver.', '')

    def to_string_lower_case(self):
        """
        小文字にして返す
        """
        return self.to_string().lower()

    def to_kebab_case(self):
        """
        ケバブケースにして返す
        """
        return self.to_string_lower_case().replace('_', '-')


# def get_by_string(str_code):
