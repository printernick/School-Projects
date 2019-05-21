URL: http://centaurus-2.ics.uci.edu:1027/
DB PW: ii1TzDSVOPrlmbsM

The initial webpage is an overview of the business and what users products users can expect.
At the top of the page is a navigation bar that users can click to navigate from the
"Home" page to the "Board Games" page.

In the "Board Games" page, there is a table that lists all of the board game products for
sale with information including name, price, players, playing time, age, and an image.
Hovering over the image will enlarge the picture. Clicking the image will redirect the 
user to a more detailed page.

Inside the detailed page, there is a slideshow featuring more images of the board game.
There is also a description of the game and a form for users to purchase it.
When filling out the form, the inputs will be:

Board Game: select one of the listed board games
Quantity: a positive integer
First Name: nonempty string
Last Name: nonempty string
Phone Number: 9 digit integer in the format: 123-456-7890
Address: nonempty string
Zip: 5 digit integer
City: nonempty string
State/Province/Region: nonempty string
Delivery Option: select one of the listed shipping options
Credit Card Number: 16 digit integer in the format: 1234-5678-9012
*NOTE: There are no options to select a country because we are currently
shipping within the United States only.

You'll notice that there is a listed total at the bottom of the purchase form
that updates based on the quantity of games specified. If the state/province/region was listed
prior to specifying the quantity, that area's tax will also be considered when calculating the total.

After selecting purchase, you will be taken to a confirmation page where you can see the details
of your order again.

REQUIREMENTS:
1. Satisfied on Board Games page and listings pages
2. Satisfied on listings page (stored on database in confirmation page)
3. Satisfied on confirmation page
4. Satisfied on listings page (after filling in zip code, state and city will
automatically fill in. After filling in quantity, total price will display
the total cost factoring in taxregion (if state is listed), quantity, and price of
the board game)
