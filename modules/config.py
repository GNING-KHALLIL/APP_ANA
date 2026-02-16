REQUIRED_COLUMNS = {
    "year": "Année de publication",
    "approche simplifié": "Type d’approche méthodologique",
    "main method": "Algorithme principal utilisé",
    "etat": "État ou région étudiée",
    "Application": "Domaine d’application",
    "journal or conference": "Source de publication",
    "times cited": "Nombre de citations"
}

TEXT_COLUMNS = {
    "Abstract": "abstract",
    "Keywords": "keywords",
    "Keywords Plus": "keywords_plus"
}

SORT_COLUMNS = [
    "main method",
    "score",
    "quartile",
    "approche simplifié",
    "Application",
    "year",
    "times cited"
]

ALLOWED_EXTENSIONS = {"csv", "xlsx"}
MAX_FILE_SIZE_MB = 10
DEFAULT_DATA_PATH = "data/data.csv"