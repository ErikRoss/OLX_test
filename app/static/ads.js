document.addEventListener("DOMContentLoaded", function() {
    var socket = io();

    function parseAds() {
        console.log('parseAds');
        socket.emit('parse ads');
    }
    document.querySelector("#update").onclick = parseAds;

    socket.on('send ad', function(msg) {
        console.log(msg);
        var ads_list_element = document.getElementById("ads_list");
        var ad_item = JSON.parse(msg);
        if (document.getElementById(ad_item.id) == null) {
            var ad_element = document.createElement("li");
            ad_element.setAttribute("class", "ad_item");
            ad_element.setAttribute("id", ad_item.id);
            var div = document.createElement("div");
            div.setAttribute("class", "ad_item-container");
            var title = document.createElement("h3");
            title.innerHTML = ad_item.title;
            div.appendChild(title);
            if (ad_item.seller != '') {
                var seller = document.createElement("h4");
                seller.innerHTML = ad_item.seller;
                div.appendChild(seller);
            }
            var price = document.createElement("p");
            if (ad_item.price) {
              price.innerHTML = ad_item.price + " " + ad_item.currency;
            }
            else {
              price.innerHTML = ad_item.currency;
            }
            div.appendChild(price);
            var img = document.createElement("img");
            if (ad_item.image) {
              img.src = "static/img/" + ad_item.image;
            }
            div.appendChild(img);
            var p = document.createElement("p");
            var del_btn = document.createElement("button");
            del_btn.setAttribute("type", "button");
            del_btn.setAttribute("class", "del_btn");
            del_btn.setAttribute("onclick",  "deleteAd(" + ad_item.id + ")");
            del_btn.innerHTML = "Удалить объявление";
            p.appendChild(del_btn);
            div.appendChild(p);
            ad_element.appendChild(div);
            ads_list_element.appendChild(ad_element);
        }
    });
});

function deleteAd(id) {
    var socket = io();
    console.log(id);
    socket.emit('delete ad', id);

    socket.on('delete ad', function(id) {
        var ad_element = document.getElementById(id);
        ad_element.innerHTML = "";
        ad_element.remove();
        console.log("Удалено объявление с id: " + id);
    });
}

function sortAds(direction) {
    const adsList = document.querySelector('#ads_list');
    const ads = document.querySelectorAll('li');
    console.log(adsList);
    console.log(ads);
    let sortingObj = {};
    ads.forEach((element, index) => {
        let adPrice = parseInt(element.querySelector('p').innerText);
        if (adPrice == NaN) {
            console.log('NaN');
            adPrice = 0;
        }
        while (sortingObj[adPrice]) {
            adPrice++;
        }
        sortingObj[adPrice] = {'element': element, 'index': index};
    });

    const keys = Object.keys(sortingObj);

    function compare(a, b) {
        a = parseInt(a);
        b = parseInt(b);
        if (a < b) {
            return -1;
        }
        if (a > b) {
            return 1;
        }
        return 0;
        }

    keys.sort(compare);
    if (direction == 'lower') {
        keys.reverse();
    }
    adsList.innerHTML = '';
    keys.map(function(key, index){
        console.log(key, index);
        adsList.insertAdjacentElement('beforeend', sortingObj[key]['element']);
    });

}
