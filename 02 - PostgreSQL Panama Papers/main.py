# Script to parse panama papers, into nicer form
from analise import analise_csv, are_columns_dependant

sources_edges = "sources/panama_papers.edges.csv"
sources_addresses = "sources/panama_papers.nodes.address.csv"
sources_entities = "sources/panama_papers.nodes.entity.csv"
sources_intermediaries = "sources/panama_papers.nodes.intermediary.csv"
sources_officers = "sources/panama_papers.nodes.officer.csv"

if __name__ == '__main__':
    # Analise all csv's
    analise_csv(sources_edges)
    analise_csv(sources_addresses)
    analise_csv(sources_entities)
    analise_csv(sources_intermediaries)
    analise_csv(sources_officers)

    # Check whether countries are dependant
    are_columns_dependant(sources_addresses, "country_codes", "countries")
    are_columns_dependant(sources_entities, "country_codes", "countries")
    are_columns_dependant(sources_intermediaries, "country_codes", "countries")
    are_columns_dependant(sources_officers, "country_codes", "countries")

    # Check whether jurisdictions are dependant
    are_columns_dependant(sources_entities, "jurisdiction", "jurisdiction_description")
