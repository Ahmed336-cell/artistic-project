//  cart implementation with direct localStorage access
const SimpleCart = {
    // Key for localStorage
    STORAGE_KEY: 'art_gallery_cart',
    
    // Get cart items from localStorage
    getItems: function() {
        try {
            const cartData = localStorage.getItem(this.STORAGE_KEY);
            return cartData ? JSON.parse(cartData) : [];
        } catch (e) {
            console.error("Error loading cart:", e);
            return [];
        }
    },
    
    // Save cart items to localStorage
    saveItems: function(items) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(items));
            return true;
        } catch (e) {
            console.error("Error saving cart:", e);
            return false;
        }
    },
    
    // Add item to cart
    addItem: function(item) {
        const items = this.getItems();
        const existingIndex = items.findIndex(i => i.id === item.id);
        
        if (existingIndex >= 0) {
            // Update quantity if item exists
            items[existingIndex].quantity += item.quantity;
        } else {
            // Add new item
            items.push(item);
        }
        
        this.saveItems(items);
        this.updateCartCount();
        return items.length;
    },
    
    // Remove item from cart
    removeItem: function(id) {
        const items = this.getItems().filter(item => item.id !== id);
        this.saveItems(items);
        this.updateCartCount();
        return items.length;
    },
    
    // Update item quantity
    updateQuantity: function(id, quantity) {
        const items = this.getItems();
        const itemIndex = items.findIndex(item => item.id === id);
        
        if (itemIndex >= 0) {
            items[itemIndex].quantity = quantity;
            this.saveItems(items);
            this.updateCartCount();
            return true;
        }
        return false;
    },
    
    // Get cart total price
    getTotal: function() {
        return this.getItems().reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },
    
    // Update cart count in UI
    updateCartCount: function() {
        const count = this.getItems().reduce((total, item) => total + item.quantity, 0);
        const countElements = document.querySelectorAll('.cart-button-count');
        countElements.forEach(el => {
            el.textContent = count;
        });
        return count;
    },
    
    // Clear entire cart
    clearCart: function() {
        this.saveItems([]);
        this.updateCartCount();
    }
};

// Direct DOM interactions for product page
document.addEventListener('DOMContentLoaded', function() {
    console.log("Page loaded - Simple Cart Solution");
    
    // Update cart count on page load
    SimpleCart.updateCartCount();
    
    // Handle Add to Cart button on product details page
    if (window.location.href.includes('product-details.html')) {
        console.log("On product details page");
        
        // Get the Add to Cart button
        const addToCartBtn = document.querySelector('.cart-btn');
        
        if (addToCartBtn) {
            console.log("Add to Cart button found");
            
            // Add click event listener
            addToCartBtn.addEventListener('click', function() {
                console.log("Add to Cart clicked");
                
                // Get product details
                const title = document.getElementById('productTitle')?.textContent || 'Art Piece';
                let price = 0;
                const priceText = document.getElementById('newPrice')?.textContent || '0';
                price = parseFloat(priceText.replace(/[^\d.-]/g, ''));
                
                const imageSrc = document.getElementById('productImage')?.src || '';
                const quantity = parseInt(document.getElementById('quantity')?.value || 1);
                
                // Log collected details
                console.log("Product Details:", {
                    title: title,
                    price: price,
                    image: imageSrc,
                    quantity: quantity
                });
                
                // Create product object
                const product = {
                    id: Date.now(), // Simple unique ID
                    title: title,
                    price: price,
                    image: imageSrc,
                    quantity: quantity,
                    category: 'Paintings'
                };
                
                // Add to cart
                const count = SimpleCart.addItem(product);
                console.log(`Item added to cart. Cart now has ${count} items.`);
                
                // Show confirmation
                alert(`Added ${title} to your cart!`);
            });
        } else {
            console.error("Add to Cart button not found!");
        }
    }
    
    // Handle cart page functionality
    if (window.location.href.includes('cart.html')) {
        console.log("On cart page");
        renderCartPage();
    }
});

// Render the cart page
function renderCartPage() {
    const cartItemsContainer = document.querySelector('.cart-items');
    if (!cartItemsContainer) {
        console.error("Cart items container not found!");
        return;
    }
    
    const items = SimpleCart.getItems();
    console.log(`Rendering cart with ${items.length} items`);
    
    // Clear existing content
    cartItemsContainer.innerHTML = '';
    
    // Handle empty cart
    if (items.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="cart-empty">
                <h2>Your cart is empty</h2>
                <p>Discover unique pieces from our talented artists</p>
                <button class="action-btn home-btn" onclick="window.location='base.html'">Explore Gallery</button>
            </div>
        `;
        
        const totalElement = document.querySelector('.cart-total');
        if (totalElement) {
            totalElement.style.display = 'none';
        }
        return;
    }
    
    // Show total element
    const totalElement = document.querySelector('.cart-total');
    if (totalElement) {
        totalElement.style.display = 'block';
    }
    
    // Add each item to the cart
    items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.innerHTML = `
            <div class="item-image">
                <img src="${item.image}" alt="${item.title}">
            </div>
            <div class="item-details">
                <div class="item-title">${item.title}</div>
                <div class="item-category">Category: <span class="category-badge">${item.category || 'Paintings'}</span></div>
                <div class="item-price">Price: ${item.price.toFixed(2)} EGP</div>
                <div class="item-quantity">
                    Quantity: 
                    <select class="quantity-select" data-id="${item.id}">
                        ${[1, 2, 3, 4, 5].map(num => 
                            `<option value="${num}" ${item.quantity === num ? 'selected' : ''}>${num}</option>`
                        ).join('')}
                    </select>
                </div>
                <div class="item-actions">
                    <button class="action-btn home-btn" onclick="window.location='base.html'">Home</button>
                    <button class="action-btn update-btn" data-id="${item.id}">Update</button>
                    <button class="action-btn delete-btn" data-id="${item.id}">Delete</button>
                </div>
            </div>
        `;
        cartItemsContainer.appendChild(itemElement);
    });
    
    // Update total amount
    const totalAmountElement = document.getElementById('total-amount');
    if (totalAmountElement) {
        totalAmountElement.textContent = SimpleCart.getTotal().toFixed(2);
    }
    
    // Add event listeners to cart item buttons
    setupCartPageEventListeners();
}

// Setup event listeners for cart page buttons
function setupCartPageEventListeners() {
    // Update quantity buttons
    document.querySelectorAll('.update-btn').forEach(button => {
        button.addEventListener('click', function() {
            const id = parseInt(this.getAttribute('data-id'));
            const select = document.querySelector(`.quantity-select[data-id="${id}"]`);
            const quantity = parseInt(select.value);
            
            SimpleCart.updateQuantity(id, quantity);
            
            // Update total display
            const totalAmountElement = document.getElementById('total-amount');
            if (totalAmountElement) {
                totalAmountElement.textContent = SimpleCart.getTotal().toFixed(2);
            }
            
            alert('Product quantity updated!');
        });
    });
    
    // Delete buttons
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const id = parseInt(this.getAttribute('data-id'));
            SimpleCart.removeItem(id);
            renderCartPage(); // Re-render cart after deletion
        });
    });
}