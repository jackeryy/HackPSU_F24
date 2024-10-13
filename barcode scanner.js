// Function to start barcode scanning using ZXing library
function startZXingScanner() {
    const codeReader = new ZXing.BrowserBarcodeReader();
    const videoElement = document.querySelector('#camera-stream');
  
    codeReader.decodeFromVideoDevice(null, videoElement, (result, err) => {
      if (result) {
        const barcode = result.text;
        console.log("Detected Barcode:", barcode); // Log detected barcode for debugging
        document.querySelector('#barcode-result').textContent = `Scanned Barcode: ${barcode}`;
        
        // Fetch product data based on barcode
        fetchProductData(barcode);
      }
      if (err && !(err instanceof ZXing.NotFoundException)) {
        console.error("Error with ZXing scanner:", err);
      }
    });
  }
  
  // Function to fetch product data from Nutritionix API using a barcode
  function fetchProductData(barcode) {
    const apiKey = '4b55ea9cf13d8d060e114717f7282c59'; // Your Nutritionix API key
    const appId = '53e56a3e'; // Your Nutritionix App ID
    const url = `https://trackapi.nutritionix.com/v2/search/item?upc=${barcode}`;
  
    fetch(url, {
      method: 'GET',
      headers: {
        "x-app-id": appId,
        "x-app-key": apiKey,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("API response:", data);  // Log the API response for debugging
  
      if (data && data.foods && data.foods.length > 0) {
        console.log("Product found in API response");
        const productApi = data.foods[0];  // Assuming the first result is the product
        displayProductInfo(productApi);  // Display product info on the page
      } else {
        console.error('No product found in response:', data);
        showModal();  // Show modal for product not found
      }
    })
    .catch(error => {
      console.error('Error fetching product data:', error);
    });
  }
  
  // Function to display product information on the page
  function displayProductInfo(product) {
    // Log the product to verify its structure
    console.log("Product Data:", product);
  
    const transFat = product.nf_trans_fatty_acid !== null ? `${product.nf_trans_fatty_acid}g` : '0g';
  
    const productInfo = `
      <h2>Product Information</h2>
      <p><strong>Name:</strong> ${product.food_name}</p>
      <p><strong>Brand:</strong> ${product.brand_name}</p>
      <p><strong>Serving Size:</strong> ${product.serving_qty} ${product.serving_unit}</p>
      <p><strong>Calories:</strong> ${product.nf_calories} kcal</p>
  
      <p><strong>Total Fat:</strong> ${product.nf_total_fat || 'N/A'}g</p>
      <p>&nbsp;&nbsp;&nbsp;<strong>Saturated Fat:</strong> ${product.nf_saturated_fat || 'N/A'}g</p>
      <p>&nbsp;&nbsp;&nbsp;<strong>Trans Fat:</strong> ${transFat}</p>
  
      <p><strong>Cholesterol:</strong> ${product.nf_cholesterol || 'N/A'}mg</p>
      <p><strong>Sodium:</strong> ${product.nf_sodium || 'N/A'}mg</p>
  
      <p><strong>Total Carbohydrates:</strong> ${product.nf_total_carbohydrate || 'N/A'}g</p>
      <p>&nbsp;&nbsp;&nbsp;<strong>Dietary Fiber:</strong> ${product.nf_dietary_fiber || 'N/A'}g</p>
      <p>&nbsp;&nbsp;&nbsp;<strong>Sugars:</strong> ${product.nf_sugars || 'N/A'}g</p>
  
      <p><strong>Protein:</strong> ${product.nf_protein || 'N/A'}g</p>
    `;
  
    // Insert product information into the #product-info div
    document.querySelector('#product-info').innerHTML = productInfo;
  }
  
  // Function to display the "Product not found" modal
  function showModal() {
    const modal = document.getElementById("productNotFoundModal");
    modal.style.display = "block";  // Show the modal
  
    // Get the <span> element that closes the modal
    const span = document.getElementsByClassName("close")[0];
  
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }
  
    // When the user clicks anywhere outside the modal, close it
    window.onclick = function(event) {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    }
  }
  
  // Event listener to start the ZXing barcode scanning when the button is clicked
  document.querySelector('#start-scan').addEventListener('click', startZXingScanner);