import map.step


class Route():

    def __init__(self, route):
        if(type(route) == 'list'):
            self.route = route[0]
        else:
            self.route = route

    def getSteps(self):
        step_list = []
        legs = self.route['legs']
        for leg in legs:
            steps = leg['steps']
            for step in steps:
                step_list.append(map.step.Step(step))
        return step_list
