import matplotlib.pyplot as plt
import seaborn as sns


def heatmap(data):
    """
    Simple heatmap with the values overlaid
    :param data: pandas dataframe
    """
    sns.set()
    f, ax = plt.subplots(figsize=(20, 10))
    sns.heatmap(data, linewidths=0.2, ax=ax, annot=True, fmt=".0f")
