from game import saveSystem

class LevelNode:
    def __init__(self, name, level, id, position):
        self.name = name
        self.level = level

        self.id = id
        self._unlocked = False
        self._completed = False

        self.position = position
    
    @property
    def unlocked(self):
        if self._unlocked:
            return True
        
        levelCleared = saveSystem.saveData.get("levelCleared", 0)
        if levelCleared >= self.id - 1:
            self._unlocked = True

        return self._unlocked

    @property
    def completed(self):
        if self._completed:
            return True

        levelCleared = saveSystem.saveData.get("levelCleared", 0)
        if levelCleared >= self.id:
            self._completed = True

        return self._completed