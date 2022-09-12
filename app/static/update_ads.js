function getXmlHttp() {
  var xmlhttp;
    try {
      xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
      } catch (e) {
      try {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
      } catch (e2) {
        xmlhttp = false;
      }
        }
  if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
  }
return xmlhttp;
}


function OnClick() {
  var http = new getXmlHttp();
  var url = "get_ads_list";
  var limit = 50;
  var ready = false;
  if (ready == false) {
      var ads_count = countAds();
      console.log(ads_count + "/" + limit);
      if (ads_count >= limit) {
        ready = true;
      }
      else {
        update(http, url, limit);
      }
  }
}


function update(http, url, limit) {
    http.open("GET", url, false);
    http.onreadystatechange = function() {
      if(http.readyState == 4 && http.status == 200) {
        var answer = http.responseText;
        var ads_list = JSON.parse(answer);
        var ads_list_div = document.getElementById("ads_list");
        ads_list_div.innerHTML = "";
        for (var i = 0; i < ads_list.length; i++) {
          var ad = ads_list[i];
          if (document.getElementById(ad.id) == null) {
            var div = document.createElement("div");
            div.setAttribute("id", ad.id);
            div.setAttribute("class", "ad");
            var title = document.createElement("h3");
            title.innerHTML = ad.title;
            div.appendChild(title);
            var seller = document.createElement("p");
            seller.innerHTML = ad.seller;
            div.appendChild(seller);
            var price = document.createElement("p");
            if (ad.price) {
              price.innerHTML = ad.price + "(" + ad.currency + ")";
            }
            else {
              price.innerHTML = ad.currency;
            }
            div.appendChild(price);
            var img = document.createElement("img");
            if (ad.image) {
              img.src = "static/img/" + ad.image;
            }
            div.appendChild(img);
            ads_list_div.appendChild(div);
          }
        }
      }
    }
    http.send(null);
}


function countAds() {
  var ads = document.getElementsByClassName("ad");
  return ads.length;
}
