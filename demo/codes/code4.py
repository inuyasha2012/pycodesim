class AB(object):
    def cd(self, ij, ef):
        if len(ij) <= 1:
            return False
        gh = {}
        for _ in range(len(ij)):
            if ij[_] in gh:
                return [gh[ij[_]], _]
            else:
                gh[ef - ij[_]] = _