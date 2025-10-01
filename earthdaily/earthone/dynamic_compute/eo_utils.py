"""EarthOne interaction and utilities"""

import earthdaily.earthone as eo


def get_product_or_fail(product_id: str) -> eo.catalog.Product:
    """A throwing version of eo.catalog.Product.get()

    Parameters
    ----------
    product_id : str
        ID of the product

    Returns
    -------
    eo.catalog.Product
        The requested catalog product
    """

    prod = eo.catalog.Product.get(product_id)
    if prod is None:
        err_msg = (
            f"Product with id '{product_id}' either does not "
            "exist or you do not have access to it"
        )
        raise eo.exceptions.NotFoundError(err_msg)

    return prod


def verify_vector_product(product_id: str, drawprop: str) -> None:
    """Verify that the product is valid and has the required draw property

    Parameters
    ----------
    product_id : str
        ID of the product
    drawprop : str
        The property to be used for drawing

    Raises
    ------
    ValueError
        If the product is not a vector product or does not have the required draw property
    """

    prod = eo.vector.Table.get(product_id)
    if prod is None:
        err_msg = (
            f"Product with id '{product_id}' either does not "
            "exist or you do not have access to it"
        )
        raise eo.exceptions.NotFoundError(err_msg)
    if prod.model["properties"]["geometry"]["geometry"] != "POINT":
        err_msg = "Product must be of geometry type POINT"
        raise ValueError(err_msg)
    if drawprop not in prod.columns:
        err_msg = (
            f"Property '{drawprop}' not found in product '{product_id}'"  # noqa: E713
        )
        raise ValueError(err_msg)
    props = prod.model["properties"][drawprop]
    if "anyOf" in props:
        types = {p["type"] for p in props["anyOf"]}
        numeric = "number" in types
    else:
        numeric = "number" in props["type"]
    if not numeric:
        err_msg = f"Property '{drawprop}' is not numeric"
        raise ValueError(err_msg)
