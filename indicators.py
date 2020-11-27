from datetime import date, datetime
from typing import Dict, Union
from pandas import DataFrame
from pandas.core.series import Series
from scipy.stats import entropy


def customer_features(customer_df: DataFrame) -> Dict[str, Union[int, float]]:
    """Features che identificano un cliente.

    Args:
        customer_df (DataFrame): DataFrame di record con lo stesso CustomerID.

    Returns:
        Dict: Features estratte dai record dell'utente.
    """
    # Numero di BasketID distinti
    baskets: int = customer_df["BasketID"].nunique()
    
    # Total number of items purchased by a customer during the period
    items: int = customer_df["Qta"].sum()
    items=items/baskets
    
    # Distinct items bought by a customer in the period of observation
    distinct_items: int = customer_df["ProdID"].nunique()
    distinct_items=distinct_items/baskets



    # Numero massimo di item acquistati in una sessione --- NON SCALATO CON BASKETS
    maximum_items: int = max(customer_df.groupby(["BasketID"])["Qta"].sum())

    # entropia del comportamento utente ( 0 = compra sempre stesso oggetto, 1 = equidistibuito  ) --- NON SCALATO CON BASKETS
    q = customer_df.groupby(["ProdID"], as_index=False)["Qta"].sum()
    E: float = entropy(q['Qta'].values, base=2)

    # Totale degli acquisti dell'utente (entrate per il negozio)
    spending: float = (customer_df["Sale"] * customer_df["Qta"]).sum()
    spending=spending/baskets
    
    # Costo medio pagato --- NON SCALATO CON BASKETS
    avg_bought: float = customer_df["Sale"].mean(skipna=True)


    return {
        "I": items,
        "Iu": distinct_items,
        "spending": spending,
        "Imax": maximum_items,
        "avg_bought": avg_bought,
        "baskets": baskets,
        "E": E
    }