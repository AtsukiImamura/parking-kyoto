import env
import map.route
import util.api_util


def route(origin, destination):
    """
    ルートを求めてサマリーを得る

    Parameters
    -----------------
    origin: float[2]
        起点の座標
    destination: float[2]
        終点の座標

    Returns
    -----------------
    info: 
        {'distance': float 総距離(m), 'time': float 所要時間(min), 'steps': Step[] ルート情報 }
    """

    res = util.api_util.get(
        "https://maps.googleapis.com/maps/api/directions/json", {
            'origin': ', '.join(origin), # float=>strで怒られるかも
            'destination': ', '.join(destination),
            'key': env.API_KEY(),
            'language': 'ja'
        })
    routes = res['routes']
    if routes == None:
        return
    route = map.route.Route(routes[0])
    steps = route.getSteps()
    distance = 0
    time = 0
    for step in steps:
        distance += step.get_distance_meter()
        time += step.get_duration_second()
    return {
        'distance': distance,
        'time': time,
        'steps': steps
    }
