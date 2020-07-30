$("#refresh-animes").click(async () => {
    const response = await axios.get("https://api.jikan.moe/v3/season");
    const host = await axios.post("https://aniseason.herokuapp.com/refreshanimes", response.data);
    location.reload(true);
});