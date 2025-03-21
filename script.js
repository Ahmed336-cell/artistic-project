
// product details page code 
// Get parameters from URL
const urlParams = new URLSearchParams(window.location.search);
const title = urlParams.get("title");
const price = urlParams.get("price");
const image = urlParams.get("image");
const oldPrice = urlParams.get("oldPrice") || "";
const description = urlParams.get("description") || "No description available.";

// Populate the page with product details
document.getElementById("productTitle").innerText = title;
document.getElementById("newPrice").innerText = price;
document.getElementById("productImage").src = image;
document.getElementById("oldPrice").innerText = oldPrice;
document.getElementById("description").innerText = description;
