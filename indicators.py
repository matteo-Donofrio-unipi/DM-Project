from datetime import datetime
from typing import Dict, Union
from pandas import DataFrame
from pandas.core.series import Series


def customer_features(customer_df: DataFrame) -> Dict[str, Union[int, float]]:
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
    # TODO: Altri due obbligatori

    # Sotto-dataframe con i record positivi e negativi
    positive_df: DataFrame = customer_df[customer_df["Qta"] > 0]
    negative_df: DataFrame = customer_df[customer_df["Qta"] < 0]

    # Numero massimo di item acquistati in una sessione
    maximum_items: int = max(customer_df.groupby(["BasketID"])["Qta"].sum())

    #numero totale di prodotti restituiti
    total_returned_items: int = abs(negative_df["Qta"].sum())

    #paese in cui ha effettuato piu sessioni
    q=customer_df.groupby(["CustomerCountry"],as_index=False)["BasketID"].count()
    q=q.sort_values(by="BasketID",ascending=False)

    favorite_country: str = q.iloc[0]["CustomerCountry"]


    # Totale degli acquisti dell'utente (entrate per il negozio)
    spending: float = (positive_df["Sale"] * positive_df["Qta"]).sum()
    # Prodotti restituiti (uscite per il negozio)
    returning: float = (negative_df["Sale"] * positive_df["Qta"]).sum()
    # Series con i ProdID più acquistati
    most_bought_series: Series = positive_df["ProdID"].mode(dropna=True)
    # ProdID più acquistato, se esiste
    most_bought: str = most_bought_series.iloc[0] if most_bought_series.size > 0 else None
    # TODO: Ora / Mese del giorno di maggiore visita

    return {
        "I": items,
        "Iu": distinct_items,
        "spending": spending,
        "Imax": maximum_items,
        "returned_items":total_returned_items,
        "best_country":favorite_country,
        "returning": returning,
        "most_bought": most_bought
    }