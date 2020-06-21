class AuxPowMixin(object):
    AUXPOW_START_HEIGHT = 0
    AUXPOW_CHAIN_ID = 0x0001
    BLOCK_VERSION_AUXPOW_BIT = 0

    @classmethod
    def is_auxpow_active(cls, header) -> bool:
        height_allows_auxpow = header['block_height'] >= cls.AUXPOW_START_HEIGHT
        version_allows_auxpow = header['version'] & cls.BLOCK_VERSION_AUXPOW_BIT
        return height_allows_auxpow and version_allows_auxpow