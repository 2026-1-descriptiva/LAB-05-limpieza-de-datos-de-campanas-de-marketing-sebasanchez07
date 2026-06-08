"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    import os
    import zipfile
    import pandas as pd

    # ---------------------------------------------------------------
    # 1) LEER TODOS LOS ZIPs SIN DESCOMPRIMIR
    # ---------------------------------------------------------------
    # Cada ZIP contiene un único CSV. Leemos cada uno con pd.read_csv
    # pasandole directamente el handle al archivo DENTRO del ZIP.
    dataframes = []
    for i in range(10):
        zip_path = f"files/input/bank-marketing-campaing-{i}.csv.zip"
        with zipfile.ZipFile(zip_path, "r") as z:
            for nombre_csv in z.namelist():
                with z.open(nombre_csv) as f:
                    df = pd.read_csv(f)
                    dataframes.append(df)

    # Unimos los 10 dataframes verticalmente. ignore_index=True resetea el índice.
    df = pd.concat(dataframes, ignore_index=True)

    # El CSV original tiene una columna "Unnamed: 0" que es el índice viejo.
    # La descartamos porque no aporta información.
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # ---------------------------------------------------------------
    # 2) CONSTRUIR client.csv
    # ---------------------------------------------------------------
    client = df[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    # job: reemplazar "." por "" y "-" por "_"
    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)   # "admin." -> "admin"
        .str.replace("-", "_", regex=False)  # "blue-collar" -> "blue_collar"
    )

    # education: reemplazar "." por "_" y "unknown" por pd.NA
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client.loc[client["education"] == "unknown", "education"] = pd.NA

    # credit_default: "yes" -> 1, cualquier otro -> 0
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)

    # mortgage: "yes" -> 1, cualquier otro -> 0
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # ---------------------------------------------------------------
    # 3) CONSTRUIR campaign.csv
    # ---------------------------------------------------------------
    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "month",
            "day",
        ]
    ].copy()

    # previous_outcome: "success" -> 1, cualquier otro -> 0
    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)

    # campaign_outcome: "yes" -> 1, cualquier otro -> 0
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    # last_contact_date: combinamos day, month y año 2022 con formato "YYYY-MM-DD"
    # Usamos pd.to_datetime con el formato %b (mes abreviado en inglés: jan, feb, ...)
    campaign["last_contact_date"] = pd.to_datetime(
        "2022-" + campaign["month"] + "-" + campaign["day"].astype(str),
        format="%Y-%b-%d",
    ).dt.strftime("%Y-%m-%d")

    # Eliminamos las columnas auxiliares month y day (ya no las necesitamos)
    campaign = campaign.drop(columns=["month", "day"])

    # ---------------------------------------------------------------
    # 4) CONSTRUIR economics.csv
    # ---------------------------------------------------------------
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    # ---------------------------------------------------------------
    # 5) GUARDAR LOS 3 CSVs
    # ---------------------------------------------------------------
    os.makedirs("files/output", exist_ok=True)

    client.to_csv("files/output/client.csv", index=False)
    campaign.to_csv("files/output/campaign.csv", index=False)
    economics.to_csv("files/output/economics.csv", index=False)

    return {
        "client": client,
        "campaign": campaign,
        "economics": economics,
    }


if __name__ == "__main__":
    clean_campaign_data()
