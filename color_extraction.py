import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, Birch


def rgb_to_hex(rgb):
    def fill_zero(val):
        return f'0{val}' if len(val) < 4 else val
    return'#{}{}{}'.format(*[fill_zero(hex(c)) for c in rgb]).replace(
        '0x', ''
    )


class ColorExtractor:
    def __init__(
        self,
        algo='kmeans',
        n_colors=4,
        random_state=0,
        batch_size=100,
        init='k-means++',
        max_iter=100,
        verbose=0,
        compute_labels=True,
        tol=0.0,
        max_no_improvement=10,
        init_size=None,
        n_init=3,
        reassignment_ratio=0.01,
        threshold=0.5,
        branching_factor=50,
        copy=True
    ):
        if algo == 'birch':
            self.extractor = BirchColorExtractor(
                n_colors=n_colors,
                threshold=threshold,
                branching_factor=branching_factor,
                compute_labels=compute_labels,
                copy=copy
            )
        else:
            self.extractor = KmeansColorExtractor(
                n_colors=n_colors,
                random_state=random_state,
                batch_size=batch_size,
                init=init,
                max_iter=max_iter,
                verbose=verbose,
                compute_labels=compute_labels,
                tol=tol,
                max_no_improvement=max_no_improvement,
                init_size=init_size,
                n_init=n_init,
                reassignment_ratio=reassignment_ratio
            )

    def extract(self, colormap):
        cmap = plt.get_cmap(colormap)
        return self.extractor.extract(cmap)


class KmeansColorExtractor:
    def __init__(
        self,
        n_colors=4,
        random_state=0,
        batch_size=100,
        init='k-means++',
        max_iter=100,
        verbose=0,
        compute_labels=True,
        tol=0.0,
        max_no_improvement=10,
        init_size=None,
        n_init=3,
        reassignment_ratio=0.01
    ):
        self.kmeans = MiniBatchKMeans(
            n_clusters=n_colors,
            random_state=random_state,
            batch_size=batch_size,
            init=init,
            max_iter=max_iter,
            verbose=verbose,
            compute_labels=compute_labels,
            tol=tol,
            max_no_improvement=max_no_improvement,
            init_size=init_size,
            n_init=n_init,
            reassignment_ratio=reassignment_ratio
        )

    def extract(self, cmap):
        image_array = np.array(
            [cmap(i)[:3] for i in range(cmap.N)], dtype=np.float64)

        print("Fitting model on a small sub-sample of the data")
        # manually fit on batches
        self.kmeans.fit(image_array)

        # Get labels for all points
        print("Predicting color indices on the full image (k-means)")
        labels = self.kmeans.labels_

        main_color_array = 255 * self.kmeans.cluster_centers_
        return [
            rgb_to_hex(color) for color in main_color_array.astype(int)
        ]


class BirchColorExtractor:
    def __init__(
        self,
        n_colors=None,
        threshold=0.5,
        branching_factor=50,
        compute_labels=True,
        copy=True
    ):
        self.birch = Birch(
            n_clusters=n_colors,
            threshold=threshold,
            branching_factor=branching_factor,
            compute_labels=compute_labels,
            copy=copy
        )

    def extract(self, cmap):
        image_array = np.array(
            [cmap(i)[:3] for i in range(cmap.N)], dtype=np.float64)

        print("Fitting model on a small sub-sample of the data")
        # manually fit on batches
        self.birch.fit(image_array)

        # Get labels for all points
        print("Predicting color indices on the full image (birch)")
        labels = self.birch.labels_

        main_color_array = 255 * self.birch.subcluster_centers_
        return [
            rgb_to_hex(color) for color in main_color_array.astype(int)
        ]
