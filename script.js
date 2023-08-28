document.addEventListener("DOMContentLoaded", function () {
    const fetchArticlesButton = document.getElementById("fetch-articles");
    const articlesContainer = document.getElementById("articles-container");
    const loadingMessage = document.getElementById("loading-message");

    fetchArticlesButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent form submission

        const searchInput = document.getElementById("search-input").value;
        loadingMessage.innerHTML = "Fetching articles. Please wait...";
        articlesContainer.innerHTML = ""; // Clear previous articles

        fetch(`http://127.0.0.1:5000/api/articles?query=${searchInput}`)
            .then(response => response.json())
            .then(data => {
                displayArticles(data.articles);
                loadingMessage.innerHTML = ""; // Clear loading message
            })
            .catch(error => {
                console.error("Error fetching articles:", error);
                loadingMessage.innerHTML = "Error fetching articles. Please try again later.";
            });
    });

    function displayArticles(articles) {
        if (articles.length === 0) {
            articlesContainer.innerHTML = "<p>No articles found.</p>";
        } else {
            articles.forEach(article => {
                const articleCard = document.createElement("div");
                articleCard.classList.add("card");
                articleCard.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${article.title}</h5>
                        <p class="card-text"><strong>Publish Time:</strong> ${article.publish_time}</p>
                        <p class="card-text">${article.summary}</p>
                        <a href="${article.source}" class="card-link" target="_blank">Read More</a>
                    </div>
                `;
                articlesContainer.appendChild(articleCard);
            });
        }
    }
});
