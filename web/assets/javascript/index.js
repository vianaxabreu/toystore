window.dataLayer = window.dataLayer || [];

const renderBadge = () => {
  const badge = document.querySelector('#cart-badge')
  badge.innerText = cartLS.list().reduce((prev, curr) => prev + curr.quantity, 0)
}

const listenToAdd = (buttons) => {
  buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
      const { id, name, price, location } = event.currentTarget.dataset
      if (cartLS.exists(id)) {
        cartLS.quantity(id, 1)
      } else {
        cartLS.add({ id, name, price })
      }
      dataLayer.push({
        event: 'addToCart',
        item: { id, name, price },
        location: location
      })
    })
  })
}

const cartItemsListeners = () => {
  const addToCartButtons = document.querySelectorAll('.cart .add-to-cart')
  listenToAdd(addToCartButtons)

  const cartItemRemoveButtons = document.querySelectorAll('.cart-item-remove')
  cartItemRemoveButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
      const { id, name, price, quantity } = event.currentTarget.dataset
      cartLS.remove(id)
      dataLayer.push({
        event: 'removeCartItem',
        item: { id, name, price },
        quantity: -parseInt(quantity),
        location: 'cart',
      })
    })
  })

  const removeFromCartButtons = document.querySelectorAll('.remove-from-cart')
  removeFromCartButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
      const { id, name, price } = event.currentTarget.dataset
      cartLS.quantity(id, -1)
      dataLayer.push({
        event: 'removeOneFromCart',
        item: { id, name, price },
        location: 'cart',
      })
    })
  })
}


const renderCart = () => {
  renderBadge();

  const cartBody = document.querySelector('.cart');
  cartBody.innerHTML = cartLS.list().map((item, index) => {
    return `<tr>
      <td>#${index + 1}</td>
      <td>${item.name}</td>
      <td>
        <button type="button" class="btn btn-block btn-sm btn-outline-primary remove-from-cart" data-id="${item.id}" data-name="${item.name}" data-price="${item.price}">-</button>
      </td>
      <td>${item.quantity}</td>
      <td>
        <button type="button" class="btn btn-block btn-sm btn-outline-primary add-to-cart" data-id="${item.id}" data-name="${item.name}" data-price="${item.price}" data-location="cart">+</button>
      </td>
      <td class="text-right">${item.price * item.quantity}€</td>
      <td class="text-right"><button class="btn btn-outline-danger btn-sm cart-item-remove" data-id="${item.id}" data-name="${item.name}" data-price="${item.price}" data-quantity="${item.quantity}">Remove</button></td>
    </tr>`
  }).join('');

  const total = document.querySelector('.total')
  total.innerText = `${cartLS.total()}€`;

  cartItemsListeners();
}

renderCart();
cartLS.onChange(renderCart);

const addToCartButtons = document.querySelectorAll('.add-to-cart')
listenToAdd(addToCartButtons)

const contactForm = document.getElementById('form-contact')
if (contactForm) {
  contactForm.addEventListener('submit', (event) => {
    dataLayer.push({
      event: 'contactFormSubmit', location: 'contact', contact: Object.fromEntries(new FormData(event.currentTarget)) })
  })
}

const checkoutButton = document.getElementById('checkout-button')
checkoutButton.addEventListener('click', async (event) => {
  const cart = cartLS.list();
  const totalPrice = cartLS.total();
  const totalQuantity = cart.reduce((prev, curr) => prev + curr.quantity, 0);

  // Push to dataLayer
  dataLayer.push({
    event: 'goToCheckout',
    location: 'cart',
    cart,
    totalPrice,
    totalQuantity
  });

  // Prepare data to send
  const payload = {
    id: `order_${Date.now()}`, // Optional: unique order ID
    full_name: "Guest Checkout", // Replace with actual user input if available
    email: "",                   // Optional: get from user form if needed
    order_number: `#${Math.floor(Math.random() * 100000)}`,
    items: JSON.stringify(cart), // Send cart items as a JSON string
    total_price: totalPrice,
    total_quantity: totalQuantity
  };

  const API_URL =
    window.location.hostname === "localhost"
      ? "http://localhost:5002"
      : "http://flask_api:5002";

  try {
    const response = await fetch(`${API_URL}/submit_order`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      alert('Checkout submitted successfully!');
      cartLS.destroy(); // Clear the cart
      const modal = bootstrap.Modal.getInstance('#cartModal');
      modal.hide();
    } else {
      const errorData = await response.json();
      alert(errorData.message || 'Failed to submit checkout.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred: ' + error.message);
  }
});


const cards = document.querySelectorAll('.card-hover')
cards.forEach((card) => {
  card.addEventListener('mouseenter', (event) => {
    event.currentTarget.classList.add('shadow-sm')
  })
  card.addEventListener('mouseleave', (event) => {
    event.currentTarget.classList.remove('shadow-sm')
  })
})

const form = document.getElementById('form-contact');
form.addEventListener('submit', async function (e) {
  e.preventDefault();

  const API_URL =
  window.location.hostname === "localhost"
    ? "http://localhost:5002"
    : "http://flask_api:5002"; // fallback for Docker-internal calls
  const formData = new FormData(form);
  const data = {};

  formData.forEach((value, key) => {
    data[key] = value;
  });

  try {
    const response = await fetch(`${API_URL}/submit_form`, { // Use container name and internal port
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      alert('Message sent successfully!');
      form.reset();
    } else {
      const errorData = await response.json();
      alert(errorData.message || 'Failed to send message.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred: ' + error.message);
  }
});