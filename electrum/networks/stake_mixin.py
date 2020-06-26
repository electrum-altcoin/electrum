class StakeMixin(object):
    POS_START_HEIGHT = 0
    MIN_POS_WORK_LIMIT = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    @classmethod
    def is_pos_active(cls, header) -> bool:
        return cls.POS_START_HEIGHT and header['block_height'] >= cls.POS_START_HEIGHT