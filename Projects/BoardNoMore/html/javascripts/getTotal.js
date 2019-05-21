//This code was given in my class lecture.
//and was slighly modified by me.

function getTotal (quantity)
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
    {
      var unparsedPrice = document.getElementById("price").textContent;
      var price = +unparsedPrice.slice(1, unparsedPrice.length); //slice off $ and make integer

      var state = document.getElementsByName("state")[0].value;
      var tax = 1.00;

      //if the state is not empty, account for tax by
      //adding it's rate to 1.00
      if (state != "")
      {
        d3.csv("data/tax_rates2.csv").then(function(data)
        {
          for (let i = 0; i < data.length; i++)
          {
              if (data[i].TaxRegionName === state)
              {
                tax = tax + +data[i].CombinedRate;
                price = price * tax;

                //this is called multiple times because of asynchronicity
                document.getElementById("total").innerHTML = Math.round(quantity * price * 100) / 100;
                break;
              }
          }
        });
      }

      document.getElementById("total").innerHTML = Math.round(quantity * price * 100) / 100;

    }
  }
  // Call the response software component
  //xhr.open ("GET", "listing.php?zip=" + zip, true);
  //xhr.send ();
  xhr.open ("POST", "listing.php", true);
  xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded");
  xhr.send ("quantity="+quantity);
}
