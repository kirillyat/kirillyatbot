from typing import Optional
from io import BytesIO
import pandas as pd


def elections(data: BytesIO) -> Optional[BytesIO]:
    df = pd.read_csv(data)
    try:
        df = df.drop("cnty", axis=1)
        df = df.drop("legid", axis=1)

        df["доля"] = df["votes"] / df["ElectionTotalVotes"]
        df["%"] = df["доля"] * 100
        df["party"] = df["party"].apply(lambda x: "-".join(x.split("-")[1:]))
        df.rename(
            columns={"party": "партия", "votes": "голоса", "seats": "места"},
            inplace=True,
        )

        # Группировка данных по полю 'year'
        grouped = df.groupby("year")

        # Создание Excel-файла и запись данных в разные листы

    except:
        return None
    excel_buffer = BytesIO()
    excel_writer = pd.ExcelWriter(excel_buffer, engine="xlsxwriter")
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        for year, group_data in grouped:
            group_data = group_data.drop("year", axis=1)
            group_data = group_data.drop("ElectionTotalVotes", axis=1)
            group_data = group_data.drop("TotalSeats", axis=1)
            group_data = group_data.sort_values(by="голоса", ascending=False)
            group_data.to_excel(
                writer, sheet_name=str(year), index=False, float_format="%.2f"
            )
    excel_writer.save()
    excel_buffer.seek(0)
    return excel_buffer


def csv2xslx(data: BytesIO) -> BytesIO:
    df = pd.read_csv(data)
    excel_buffer = BytesIO()
    excel_writer = pd.ExcelWriter(excel_buffer, engine="xlsxwriter")
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        pd.to_excel(writer, index=False)
    excel_writer.save()
    excel_buffer.seek(0)
    return excel_buffer
