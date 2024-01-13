class cycle_set(set):
    def __init__(self, include_rotations=True, include_reflections=True):
        self.exclude_rotations = include_rotations
        self.exclude_reflections = include_reflections
        self.exclude_both = include_rotations and include_reflections
        super().__init__()

    def __enumerate_rotations(self, cycle):
        for i in range(len(cycle)):
            yield cycle[i:] + cycle[:i]
    def __enumerate_reflections(self, cycle):
        yield cycle
        yield cycle[::-1]

    def add(self, elem):
        should_add = True
        if self.exclude_both:
            for rotation in self.__enumerate_rotations(elem):
                for reflection in self.__enumerate_reflections(rotation):
                    if reflection in self:
                        should_add = False
                        break
        elif self.exclude_rotations:
            for rotation in self.__enumerate_rotations(elem):
                if rotation in self:
                    should_add = False
                    break
        elif self.exclude_reflections:
            for reflection in self.__enumerate_reflections(elem):
                if reflection in self:
                    should_add = False
                    break

        if should_add:
            super().add(elem)


    def update(self, elems):
        for elem in elems:
            self.add(elem)
    def __contains__(self, elem):
        if self.exclude_both:
            for rotation in self.__enumerate_rotations(elem):
                for reflection in self.__enumerate_reflections(rotation):
                    if super().__contains__(reflection):
                        return True
        elif self.exclude_rotations:
            for rotation in self.__enumerate_rotations(elem):
                if super().__contains__(rotation):
                    return True
        elif self.exclude_reflections:
            for reflection in self.__enumerate_reflections(elem):
                if super().__contains__(reflection):
                    return True
        else:
            return super().__contains__(elem)
