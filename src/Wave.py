class Wave:
    # The size of the gap at the beginning and end of every wave piece
    WAVE_BUFFER = 2

    def __init__(self, wave: str, offset: int):
        self.wave = wave
        self.offset = offset

    # Returns a string representation of the wave that includes the current offset by cutting off the proper
    # front/back gaps
    def __repr__(self) -> str:
        start = self.offset
        end = self.offset + len(self.wave) - self.WAVE_BUFFER
        return self.wave[start:end]

    def can_move(self, direction) -> bool:
        # for left/right
        # Check if wave can move left
        # for each boat in current wave
        # find other waves holding those boats
        # repeat for any new boats added until all dependent waves are found and no more new boats are found
        # if all dependent waves can move left, move waves left and move boat left
        return False

    def move(self, direction) -> None:
        return
