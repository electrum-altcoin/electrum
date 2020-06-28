class StakeMixin(object):
    POS_START_HEIGHT = 0
    MIN_POS_WORK_LIMIT = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    @classmethod
    def is_pos_active(cls, header) -> bool:
        if cls.POS_START_HEIGHT is None:
            return False

        return header['block_height'] >= cls.POS_START_HEIGHT