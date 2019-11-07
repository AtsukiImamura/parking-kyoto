import util.api_util
import env
import map.route

res = util.api_util.get(
    "https://maps.googleapis.com/maps/api/directions/json", {
        'origin': '35.00369, 135.75967',
        'destination': '35.00192, 135.76259',
        'key': env.API_KEY(),
        'language': 'ja'
    })

path = './test.txt'

with open(path, mode='w', encoding="utf-8") as f:
    routes = res['routes']
    route = map.route.Route(routes[0])
    print(str(route))
    steps = route.getSteps()
    print(str(steps))
    print(len(steps))
    for step in steps:
        print(str(step.get_maneuver()))
    # for route in routes:
    #     legs = route['legs']
    #     for leg in legs:
    #         steps = leg['steps']
    #         for step in steps:
    #             # detail_steps = step['steps']
    #             f.write("\n\n")
    #             f.write(str(step))
    #             # for detail_step in detail_steps:
    #             #     f.write("\n")
    #             #     f.write(str(detail_step))

   # for item in res:
   #     f.write(str(item))
