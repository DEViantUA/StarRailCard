const axios = require('axios');

async function main() {
    const url = "https://honkaistarrailbot.herokuapp.com/api/card";
    const headers = {'Content-Type': 'application/json'};

    const data = {
        "uid": "YOU_UID",
        "lang": "ua",
        "name": "1208, 1205, 1112",
        "image": {"1302": "https://i.pximg.net/img-master/img/2023/06/20/16/53/28/109183352_p0_master1200.jpg"}
    };

    try {
        const response = await axios.post(url, data, {headers});

        if (response.status === 200) {
            const responseData = response.data;
            if (!responseData.message) {
                console.log("Request successful");
                console.log(responseData);
            } else {
                console.log("Request failed");
                console.log(responseData.message);
            }
        } else {
            console.log(`Request failed with status code ${response.status}`);
        }
    } catch (error) {
        console.error("Error during the request:", error.message);
    }
}

main();
