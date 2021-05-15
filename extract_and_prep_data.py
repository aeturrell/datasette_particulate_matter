"""
Take the PM2.5 estimate anthro data for last years from
https://uk-air.defra.gov.uk/data/pcm-data
of form name popwmpm252012byUKlocalauthority.csv
url https://uk-air.defra.gov.uk/datastore/pcm/popwmpm252012byUKlocalauthority.csv
and merge together then do time series with error bands
by region (see lookup).
"""
import numpy as np
import pandas as pd
from pathlib import Path

MIN_YEAR_INCLUSIVE = 2010
MAX_YEAR_EXCLUSIVE = 2020


def grab_poll_file(data_yr):
    stem_pt_one = "https://uk-air.defra.gov.uk/datastore/pcm/popwmpm25"
    stem_pt_two = "byUKlocalauthority.csv"
    url = stem_pt_one + str(data_yr) + stem_pt_two
    df = (
        pd.read_csv(url, header=2)
        .assign(
            local_authority_code=lambda x: x["LA code"]
            .astype("string")
            .astype("category"),
            pm_anthropogenic=lambda x: x[
                "PM2.5 " + str(data_yr) + " (anthropogenic)"
            ].astype("double"),
            pm_total=lambda x: x["PM2.5 " + str(data_yr) + " (total)"].astype("double"),
            pm_non_anthropogenic=lambda x: x[
                "PM2.5 " + str(data_yr) + " (non-anthropogenic)"
            ].astype("double"),
            local_authority_name=lambda x: x["Local Authority"].astype("string"),
            year=data_yr,
        )
        .loc[
            :,
            [
                "local_authority_code",
                "pm_anthropogenic",
                "pm_total",
                "pm_non_anthropogenic",
                "local_authority_name",
                "year",
            ],
        ]
    )
    return df


df = pd.concat(
    [grab_poll_file(x) for x in np.arange(MIN_YEAR_INCLUSIVE, MAX_YEAR_EXCLUSIVE)],
    axis=0,
)
df = df.loc[df["local_authority_code"] != "447/439", :]


la_to_reg_fname = Path(
    "assets/Ward_to_Local_Authority_District_to_County_to_Region_to_Country_December_2019_UK.csv"
)
la_to_reg = pd.read_csv(la_to_reg_fname).assign(
    local_authority_name=lambda x: x["LAD19NM"].astype("string"),
    region=lambda x: x["RGN19NM"].astype("string"),
)
la_to_reg.loc[la_to_reg["region"].isna(), "region"] = la_to_reg.loc[
    la_to_reg["region"].isna(), "CTRY19NM"
]


xf = pd.merge(
    df,
    la_to_reg[["local_authority_name", "region", "CTRY19NM"]],
    on=["local_authority_name"],
    how="left",
)

xf = xf.rename(columns={"CTRY19NM": "country"})
xf.to_csv(Path("uk_particulate_matter.csv"), index=False)



chi = pd.read_json("https://particulatematter-fsx2r7puuq-nw.a.run.app/uk_particulate_matter/uk_particulate_matter.json?_sort=rowid&local_authority_name__contains=southwark&year__exact=2018&_shape=array")

chi = pd.read_csv("https://particulatematter-fsx2r7puuq-nw.a.run.app/uk_particulate_matter.csv?sql=select+rowid%2C+local_authority_code%2C+pm_anthropogenic%2C+pm_total%2C+pm_non_anthropogenic%2C+local_authority_name%2C+year%2C+region%2C+country+from+uk_particulate_matter+where+%22local_authority_name%22+like+%3Ap0+and+%22year%22+%3D+%3Ap1+order+by+rowid+limit+101&p0=%25southwark%25&p1=2018&_size=max")