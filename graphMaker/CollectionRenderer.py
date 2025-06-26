from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class CollectionRenderer(ABC):
    def __init__(self):
        self.base_x = 0.1
        self.base_y = 0.6
        self.box_height = 0.06
        self.box_width = 0.1

    @abstractmethod
    def render(self, ax, collection):
        pass

    @abstractmethod
    def get_collection_type(self):
        pass


class StackRenderer(CollectionRenderer):
    def render(self, ax, collection):
        ax.plot([self.base_x, self.base_x + self.box_width],
                [self.base_y, self.base_y],
                color='blue', linewidth=2, transform=ax.transAxes)

        for i, item in enumerate(collection):
            rect = plt.Rectangle(
                (self.base_x, self.base_y + i * self.box_height),
                self.box_width, self.box_height,
                facecolor='lightblue',
                edgecolor='blue',
                transform=ax.transAxes
            )
            ax.add_patch(rect)

            ax.text(
                self.base_x + self.box_width / 2,
                self.base_y + i * self.box_height + self.box_height / 2,
                str(item),
                fontsize=10,
                ha='center',
                va='center',
                color='black',
                transform=ax.transAxes
            )

        ax.text(
            self.base_x, self.base_y - 0.05,
            self.get_collection_type(),
            fontsize=10,
            weight='bold',
            color='blue',
            ha='left',
            transform=ax.transAxes
        )

    def get_collection_type(self):
        return "Stack"


class QueueRenderer(CollectionRenderer):
    def render(self, ax, collection):
        if collection:
            ax.plot([self.base_x, self.base_x + self.box_width * len(collection)],
                    [self.base_y, self.base_y],
                    color='blue', linewidth=2, transform=ax.transAxes)

            for i, item in enumerate(collection):
                rect = plt.Rectangle(
                    (self.base_x + i * self.box_width, self.base_y),
                    self.box_width, self.box_height,
                    facecolor='lightblue',
                    edgecolor='blue',
                    transform=ax.transAxes
                )
                ax.add_patch(rect)

                ax.text(
                    self.base_x + i * self.box_width + self.box_width / 2,
                    self.base_y + self.box_height / 2,
                    str(item),
                    fontsize=10,
                    ha='center',
                    va='center',
                    color='black',
                    transform=ax.transAxes
                )
        else:
            ax.plot([self.base_x, self.base_x + self.box_width],
                    [self.base_y, self.base_y],
                    color='blue', linewidth=2, transform=ax.transAxes)

        ax.text(
            self.base_x, self.base_y - 0.05,
            self.get_collection_type(),
            fontsize=10,
            weight='bold',
            color='blue',
            ha='left',
            transform=ax.transAxes
        )

    def get_collection_type(self):
        return "Queue"


class PriorityQueueRenderer(CollectionRenderer):
    def render(self, ax, collection):
        if collection:
            ax.plot([self.base_x, self.base_x + self.box_width * len(collection)],
                    [self.base_y, self.base_y],
                    color='blue', linewidth=2, transform=ax.transAxes)

            for i, item_data in enumerate(collection):
                item, ordinal = item_data if isinstance(item_data, tuple) and len(item_data) == 2 else (item_data,
                                                                                                        i + 1)

                rect = plt.Rectangle(
                    (self.base_x + i * self.box_width, self.base_y),
                    self.box_width, self.box_height,
                    facecolor='lightblue',
                    edgecolor='blue',
                    transform=ax.transAxes
                )
                ax.add_patch(rect)

                ax.text(
                    self.base_x + i * self.box_width + self.box_width / 2,
                    self.base_y + self.box_height / 2,
                    str(item),
                    fontsize=10,
                    ha='center',
                    va='center',
                    color='black',
                    transform=ax.transAxes
                )

                ax.text(
                    self.base_x + i * self.box_width + self.box_width / 2,
                    self.base_y + self.box_height + 0.01,
                    f"{ordinal}",
                    fontsize=8,
                    ha='center',
                    va='bottom',
                    color='darkblue',
                    transform=ax.transAxes
                )
        else:
            ax.plot([self.base_x, self.base_x + self.box_width],
                    [self.base_y, self.base_y],
                    color='blue', linewidth=2, transform=ax.transAxes)

        ax.text(
            self.base_x, self.base_y - 0.05,
            self.get_collection_type(),
            fontsize=10,
            weight='bold',
            color='blue',
            ha='left',
            transform=ax.transAxes
        )

    def get_collection_type(self):
        return "Priority Queue"