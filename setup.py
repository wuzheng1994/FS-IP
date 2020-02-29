from distutils.core import setup

NAME = "FS&IP"

DESCRIPTION = "Feature Selection and instance selection"

AUTHOR = "Zheng Wu"

VERSION = "1.0.0"


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    author = AUTHOR,
    packages =['skfeature', 'skfeature.utility','skfeature.function','skfeature.function.information_theoretical_based','skfeature.function.similarity_based','skfeature.function.sparse_learning_based','skfeature.function.statistical_based','skfeature.function.streaming','skfeature.function.structure','skfeature.function.wrapper',] ,
)
