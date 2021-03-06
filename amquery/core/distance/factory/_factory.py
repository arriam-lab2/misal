from amquery.core.distance import SamplePairwiseDistance, distances, WEIGHTED_UNIFRAC


class Factory:
    @staticmethod
    def create(config):
        """
        :param config: Config
        :return: PairwiseDistance 
        """
        method = config.get('distance', 'method')
        return SamplePairwiseDistance(distances[method](config))

    @staticmethod
    def load(config):
        """
        :param config: Config
        :return: PairWiseDistance 
        """
        return SamplePairwiseDistance.load(config)
