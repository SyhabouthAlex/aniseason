$("#refresh-animes").click(async () => {
    const response = await axios.get("https://api.jikan.moe/v3/season");
    const host = await axios.post("/refreshanimes", response.data);
    location.reload(true);
});

$(".follow").click(async (evt) => {
    try {
        await axios.post(`/follow/${evt.target.dataset.animeId}`)
        if (evt.target.innerText === "Unfollow") {
            evt.target.innerText = "Follow";
        }
        else if (evt.target.innerText === "Follow") {
            evt.target.innerText = "Unfollow";
        };
    }
    catch {
        $("#flashed-msgs").append("<div class='alert alert-danger' role='alert'>Follow failed. Please ensure you are logged in.")
    }
})