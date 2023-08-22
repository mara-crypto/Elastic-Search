import requests
import csv

# URL de l'API
api_url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=04c35731a5ee918f014970082a0088b1"

# Récupérer les données de l'API pour la première page
response = requests.get(api_url)
data = response.json()
movies = data["results"]

# Récupérer le nombre total de pages
total_pages = data["total_pages"]

# Récupérer les données de l'API pour les autres pages
for page in range(2, 500):
    page_url = f"{api_url}&page={page}"
    response = requests.get(page_url)
    data = response.json()
    movies.extend(data["results"])

# Chemin du fichier CSV
csv_file_path = "movies.csv"

# Écrire les données dans le fichier CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = movies[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(movies)
import os

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin absolu du fichier CSV
csv_file_path = os.path.join(script_directory, "movies.csv")


# Configuration de Logstash
logstash_config = """
    input {
        file {
            path => "/home/dioptrtit/Bureau/Projets realiser/Elastic Search/movies.csv"
            start_position => "beginning"
            sincedb_path => "/dev/null"
        }
    }

    filter {
        csv {
            separator => ","
            columns => ["adult", "backdrop_path", "genre_ids", "id", "original_language", "original_title", "overview", "popularity", "poster_path", "release_date", "title", "video", "vote_average", "vote_count"]
        }
    }

    output {
        elasticsearch {
            hosts => ["localhost:9200"]
            index => "themoviedb"
        }
        stdout { codec => rubydebug }
    }
"""

# Écrire la configuration de Logstash dans un fichier
with open("movie.conf", mode='w', newline='', encoding='utf-8') as conf_file:
    conf_file.write(logstash_config)

# Exécuter Logstash
import subprocess
subprocess.run(["sudo", "/usr/share/logstash/bin/logstash", "-f", "movie.conf"])
