// async function updateAnimes() {
//     console.log("click")
//     const response = await axios.get("https://api.jikan.moe/v3/season");
//     await axios.post("http://127.0.0.1:5000/refreshanimes", response.data);
//     location.reload(true);
// }

$("#refresh-animes").click(async () => {
    const response = await axios.get("https://api.jikan.moe/v3/season");
    const host = await axios.post("https://aniseason.herokuapp.com/refreshanimes", response.data);
    location.reload(true);
});


// setInterval(async () => {
//     const response = await axios.get("https://api.jikan.moe/v3/season");
//     if (`${response["season_name"]} ${response["season_year"]}` == )
// }, 86400000)
