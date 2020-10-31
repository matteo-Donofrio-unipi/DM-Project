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

    #entropia del comportamento utente ( entorpia del tipo di prodotto acquistato )

    q=positive_df.groupby(["ProdID"],as_index=False)["Qta"].sum()
    E: float =entropy(q['Qta'].values, base=2)

    # Totale degli acquisti dell'utente (entrate per il negozio)
    spending: float = (positive_df["Sale"] * positive_df["Qta"]).sum()
    # Prodotti restituiti (uscite per il negozio)
    returning: float = (negative_df["Sale"] * negative_df["Qta"]).sum()
    # Series con i ProdID più acquistati / restituiti
    most_bought_series: Series = positive_df["ProdID"].mode(dropna=True)
    most_returned_series: Series = negative_df["ProdID"].mode(dropna=True)
    # ProdID più acquistato, se esiste
    most_bought: str = most_bought_series.iloc[0] if most_bought_series.size > 0 else None
    # ProdID più restituito, se esiste
    most_returned: str = most_returned_series.iloc[0] if most_returned_series.size > 0 else None
    # Ora / Mese del giorno di maggiore visita
    hour: datetime = customer_df["BasketDate"].dt.hour.mode()[0]
    month: datetime = customer_df["BasketDate"].dt.month.mode()[0]
    # Numero di BasketID distinti
    baskets: int = customer_df["BasketID"].nunique()
    
    return {
        "I": items,
        "Iu": distinct_items,
        "spending": spending,
        "Imax": maximum_items,
        "returned_items":total_returned_items,
        "best_country":favorite_country,
        "returning": returning,
        "most_bought": most_bought,
        "most_returned": most_returned,
        "hour": hour,
        "month": month,
        "baskets": baskets,
        "E":E
    }