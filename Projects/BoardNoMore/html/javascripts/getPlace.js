//This code was given in my class lecture.
//and was slighly modified by me.

function getPlace (zip)
{
  if (window.XMLHttpRequest)
  {  // IE7+, Firefox, Chrome, Opera, Safari
     var xhr = new XMLHttpRequest();
  }
  else
  {  // IE5, IE6
     var xhr = new ActiveXObject ("Microsoft.XMLHTTP");
  }

  // Register the embedded handler function
  // This function will be called when the server returns
  // (the "callback" function)
  xhr.onreadystatechange = function ()
  { // 4 means finished, and 200 means okay.
    if (xhr.readyState == 4 && xhr.status == 200)
    { // Data should look like "10001","NY","New York"
      d3.csv("data/zip_codes.csv").then(function(data) {
        data.forEach(function(d)
        {
          if (d.zip === zip)
          {
            if (document.getElementsByName("city")[0].value == "")
            {

              document.getElementsByName("city")[0].value = d.city;
            }

            if (document.getElementsByName("state")[0].value == "")
              document.getElementsByName("state")[0].value = d.state;
          }
        });
      });
    }
  }
  // Call the response software component
  //xhr.open ("GET", "listing.php?zip=" + zip, true);
  //xhr.send ();
  xhr.open ("POST", "listing.php", true);
  xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded");
  xhr.send ("zip="+zip);
}
