document.getElementById("searchForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Empêche le formulaire de se soumettre normalement
    const query = document.getElementById("searchInput").value;

    try {
        // Envoyer la requête de recherche au backend (exemple en utilisant l'API Fetch)
        const response = await fetch(`http://localhost:9200/themoviedb/_search?q=${query}`);
        const responseData = await response.json();
        results = responseData.hits.hits;

        // Afficher les résultats dans le conteneur "resultsContainer"
        const resultsContainer = document.getElementById("resultsContainer");
        resultsContainer.innerHTML = ""; // Efface les résultats précédents

        if (results.length === 0) {
            resultsContainer.innerHTML = "<p>Aucun résultat trouvé.</p>";
        } else {
            results.forEach(result => {
                const resultDiv = document.createElement("div");
                resultDiv.className = "result-item";
                resultDiv.innerHTML = `
                                        <h3>${result._source.title}</h3>
                                        <p>${result._source.overview}</p>
                                        <p>Note ${result._source.vote_average}</p>
                                        <p>${result._source.vote_count} Vote</p>
                                        `;
                resultsContainer.appendChild(resultDiv);
            });
        }
    } catch (error) {
        console.log(error);
    }
});
