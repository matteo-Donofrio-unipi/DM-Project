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
    items: int = customer_df["Qta"].sum()
    # Distinct items bought by a customer in the period of observation
    distinct_items: int = customer_df["ProdID"].nunique()
    # TODO: Altri due obbligatori

    # Sotto-dataframe con i record positivi e negativi
    positive_df: DataFrame = customer_df[customer_df["Qta"] > 0]
    negative_df: DataFrame = customer_df[customer_df["Qta"] < 0]

    # Numero massimo di item acquistati in una sessione
    maximum_items: int = max(customer_df.groupby(["BasketID"])["Qta"].sum())

    # numero totale di prodotti restituiti
    total_returned_items: int = abs(negative_df["Qta"].sum())

    # paese in cui ha effettuato piu sessioni
    q = customer_df.groupby(["CustomerCountry"], as_index=False)["BasketID"].count()
    q = q.sort_values(by="BasketID", ascending=False)

    favorite_country: str = q.iloc[0]["CustomerCountry"]

    # entropia del comportamento utente ( 0 = compra sempre stesso oggetto, 1 = equidistibuito  )

    q = positive_df.groupby(["ProdID"], as_index=False)["Qta"].sum()
    E: float = entropy(q['Qta'].values, base=2)

    # Totale degli acquisti dell'utente (entrate per il negozio)
    spending: float = (positive_df["Sale"] * positive_df["Qta"]).sum()
    # Prodotti restituiti (uscite per il negozio)
    returning: float = (negative_df["Sale"] * negative_df["Qta"]).sum()
    # Massimo costo pagato dall'utente
    max_cost: float = positive_df["Sale"].max()
    # Costo medio pagato
    avg_bought: float = positive_df["Sale"].mean()
    # Massimo costo di un prodotto restituito
    min_cost: float = negative_df["Sale"].max()
    # Costo medio restituito
    avg_returned: float = negative_df["Sale"].mean()
    # Costo del prodotto più acquistato/restituito dall'utente
    most_bought_cost: float = positive_df["Sale"].mode().get(0, 0)
    most_returned_cost: float = negative_df["Sale"].mode().get(0, 0)
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
        "returned_items": total_returned_items,
        "best_country": favorite_country,
        "returning": returning,
        "max_cost": max_cost,
        "min_cost": min_cost,
        "most_bought_cost": most_bought_cost,
        "most_returned_cost": most_returned_cost,
        "avg_bought": avg_bought,
        "avg_returned": avg_returned,
        "hour": hour,
        "month": month,
        "baskets": baskets,
        "E": E
    }