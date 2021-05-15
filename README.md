# datasette_particulate_matter

An example of using [datasette](https://datasette.io/) to deploy a searchable API, either locally (on your computer) or online via Google Cloud Run.

## How to deploy this example

### Optional

To pull in the data from multiple files on the DEFRA website, run the python code `extract_and_prep_data.py`. The resulting CSV file also exists in the repo; hence this step is optional.

### To use locally

1. `pip install csvs-to-sqlite datasette` on the command line; to install relevant packages.

2. `csvs-to-sqlite uk_particulate_matter.csv uk_particulate_matter.db` in command line; to convert csv file into a database.

3. `datasette uk_particulate_matter.db` in command line to create datasette web site for data; look at created link in browser. (No metadata)

To create the database with the metadata too, it's `datasette uk_particulate_matter.db --metadata metadata.json`.

### To run on the web via Google Cloud Run

1. Follow steps 1 and 2 above.

2. Install and configure the Google Cloud CLI tools by following the instructions [here](https://cloud.google.com/sdk/). Note that although there is a free tier for Google Cloud Run, you may need to add billing details.

3. `datasette publish cloudrun uk_particulate_matter.db --service=particulatematter` or `datasette publish cloudrun uk_particulate_matter.db --service=particulatematter --metadata metadata.json` with the metadata too.

This will create a docker container and deploy it to the Cloud Run service. You may be prompted to give a preferred region. Remember to make sure your billing settings are configured according to your preferences.

To visit a running example of a datasette app based on this repo, click [on this link](https://particulatematter-fsx2r7puuq-nw.a.run.app).

## Why is datasette useful?

[**datasette**](https://datasette.io/) is an extremely quick and cost-efficient way to serve up large datasets to anyone with an internet connection. The full utility is in the ways that people can then use the data. People can:

- Manually browse the site, making cuts of the data by choosing from the filtering options or editing the equivalent SQL code.

- Manually download the data (and cuts of the data) as csv or json files.

- Once filtered, copy the generated SQL code to reproduce the same filters programmatically in future. (This makes getting certain cuts &*repeatable* for users.)

- Programmatically download cuts of the data using the generated CSV, SQL, or JSON endpoints. For example, to get the anthropogenic numbers for Southwark in 2018:
  - CSV, `df = pd.read_csv("https://particulatematter-fsx2r7puuq-nw.a.run.app/uk_particulate_matter.csv?sql=select+rowid%2C+local_authority_code%2C+pm_anthropogenic%2C+pm_total%2C+pm_non_anthropogenic%2C+local_authority_name%2C+year%2C+region%2C+country+from+uk_particulate_matter+where+%22local_authority_name%22+like+%3Ap0+and+%22year%22+%3D+%3Ap1+order+by+rowid+limit+101&p0=%25southwark%25&p1=2018&_size=max")`
  - SQL,`select rowid, local_authority_code, pm_anthropogenic, pm_total, pm_non_anthropogenic, local_authority_name, year, region, country from uk_particulate_matter where "local_authority_name" like '%southwark%' and "year" = '2018' order by rowid limit 101`
  - JSON, `df = pd.read_json("https://particulatematter-fsx2r7puuq-nw.a.run.app/uk_particulate_matter/uk_particulate_matter.json?_sort=rowid&local_authority_name__contains=southwark&year__exact=2018&_shape=array")`

Note that there's nothing risky about the use of SQL here; this is just a read only sql database.

Datasette has many add-ons that provide extra support for geospatial data, password protection, and more.
