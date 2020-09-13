from abc import ABC


class AttributedMixinBase(ABC):
    def __new__(cls,
                class_name: str,
                parent_classes: tuple,
                **kwargs):
        return type(class_name, parent_classes, **kwargs)
