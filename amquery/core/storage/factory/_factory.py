from amquery.core.storage import VpTree


class Factory:
    @staticmethod
    def create(config):
        """
        :param config: Config
        :return: Storage
        """
        return VpTree()
