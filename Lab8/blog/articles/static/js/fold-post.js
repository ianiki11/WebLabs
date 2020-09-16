function showArticleInfo(acticle_id) {
    const id = 'article-info-' + acticle_id;
    const x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}