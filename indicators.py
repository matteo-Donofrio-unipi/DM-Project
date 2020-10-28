from typing import Dict
from pandas import DataFrame

def customer_features(customer_df: DataFrame) -> Dict[str, int]:
    """Features che identificano un cliente.

    Args:
        customer_df (DataFrame): DataFrame di record con lo stesso CustomerID.

    Returns:
        Dict: Features estratte dai record dell'utente.
    """
    # Total number of items purchased by a customer during the period
    items: int = customer_df["ProdID"].count()
    # Distinct items bought by a customer in the period of observation
    distinct_items: int = customer_df["ProdID"].nunique()

    return {
        "I": items,
        "Iu": distinct_items
    }