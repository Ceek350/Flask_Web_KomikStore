const comicsContainer = document.getElementById('comics-container');

fetch('https://komiku-api.fly.dev/api/comic/popular/page/1')
  .then(response => response.json())
  .then(data => {
    data.data.forEach(comic => { // Sesuaikan dengan struktur data yang benar
      const cardDeck = document.createElement('div');
      cardDeck.classList.add('col'); // Atur class Bootstrap untuk responsif

      const card = document.createElement('div');
      card.classList.add('card', 'dark-bg'); // Tambahkan kelas dark-bg untuk background gelap

      const img = document.createElement('img');
      img.classList.add('card-img-top');
      img.src = comic.image;
      img.alt = comic.title;

      const cardBody = document.createElement('div');
      cardBody.classList.add('card-body');

      const title = document.createElement('h5');
      title.classList.add('card-title');
      title.textContent = comic.title;

      const desc = document.createElement('p');
      desc.classList.add('card-text');
      desc.textContent = comic.desc;

      const btn = document.createElement('button');
      btn.classList.add('btn', 'btn-primary');
      btn.textContent = 'Tambah ke Keranjang';
      btn.onclick = function() {
        addToCart(comic.title, 75000); // Menggunakan judul komik dan harga yang sesuai
      };

      cardBody.appendChild(title);
      cardBody.appendChild(desc);
      cardBody.appendChild(btn);

      card.appendChild(img);
      card.appendChild(cardBody);

      cardDeck.appendChild(card);
      comicsContainer.appendChild(cardDeck);
    });
  })
  .catch(error => {
    console.log('Error fetching data:', error);
  });

  //usercek


  function profilbtn() {
    var profil = document.getElementById('profilside')
    profil.classList.add("active")
  }
  function closebtn() {
    var profil = document.getElementById('profilside')
    profil.classList.remove("active")
  }

  function toggleSidebar() {
  var sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("active");
  }
  function checkout() {
  // Proses checkout, misalnya redirect ke halaman pembayaran atau lakukan tindakan lain sesuai kebutuhan
  alert('Terima kasih telah berbelanja! Silakan lanjut ke pembayaran.');
  }

  let cart = [];
  let total = 0;
  let email = "";
  let price = 0;
  let selectedComic;
  let productName;


  function addToCart(productName, price) {
    selectedComic = productName;

    // Determine the price based on the product name
    if (productName === 'Jujutsu Kaisen') {
      price = 60000;
    } else if (productName === 'Judul 2') {
      price = 80000;
    } else {
      price = 70000;
    }

    // Add the product to the cart
    cart.push({ name: productName, price: price });

    // Update the total price
    console.log(price)
    total += price;
    console.log("total: ",total)

    // Update the cart view
    updateCart();
    alert('berhasil ditambahkan, silahkan cek keranjang');
  }

  
  function updateCart() {
    let cartItems = document.getElementById('cart-items');
    let cartTotal = document.getElementById('cart-total');
    cartItems.innerHTML = '';
    cart.forEach(comic => {
      let li = document.createElement('li');
      li.textContent = `${comic.name} - Rp.${comic.price}`;
      cartItems.appendChild(li);
    });
    cartTotal.textContent = total;
    }

  function profil() {
    let profil = document.getElementById('profil');
    profil.innerHTML = '';
    profil.textContent = `${msg}`;
  }

  function redirectToPayment(paymentUrl) {
  // Redirect to the payment URL
  window.open = paymentUrl;
  }

  //pembayaran
  function generateRandomId(length) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let randomId = '';

  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    randomId += characters.charAt(randomIndex);
  }

  return randomId;
  }

  // Contoh penggunaan untuk membuat ID acak dengan panjang 8 karakter
  const randomId = generateRandomId(5);
  console.log(randomId);



  async function generateAndRedirect() {
    alert('Mengarahkan ke halaman pembayaran');
    const clientKey = 'SB-Mid-client-Ay1WobiGTcJNoVKs';
    const orderId = generateRandomId(5);
  
    let snap = Snap({
      // Replace 'YourClientKey' with your actual client key
      clientKey: clientKey,
      // Replace with your callback function
      callback: function (response) {
        if (response.transaction_status === 'capture') {
          alert('Pembayaran sukses! ID Pesanan: ' + response.order_id);
        } else if (response.transaction_status === 'settlement') {
          alert('Pembayaran berhasil disetujui!');
        } else if (response.transaction_status === 'pending') {
          alert('Pembayaran sedang diproses. ID Pesanan: ' + response.order_id);
        } else if (response.transaction_status === 'deny') {
          alert('Pembayaran ditolak.');
        }
      }
    });
  
    const transactionDetails = {
      order_id: orderId,
      gross_amount: total,
    };
  
    const itemDetails = cart.map(item => ({
      id: item.name,
      price: item.price,
      quantity: 1,
      name: item.name,
    }));
  
    const customerDetails = {
      first_name: savedAddress.name,
      phone: savedAddress.phone,
      address: savedAddress.address,
      city: savedAddress.city,
      postal_code: savedAddress.postalCode,
    };
  
    const creditCardOptions = {
      secure: true,
    };
  
    const userData = {
      transaction_details: transactionDetails,
      item_details: itemDetails,
      customer_details: customerDetails,
      credit_card: creditCardOptions,
    };
  
    try {
      const response = await fetch('https://api.sandbox.midtrans.com/v2/charge', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + btoa(clientKey + ':'),
        },
        body: JSON.stringify(userData),
      });
  
      const responseData = await response.json();
  
      if (responseData.redirect_url) {
        // Redirect ke halaman pembayaran Snap Midtrans
        snap.redirect(responseData.redirect_url);
      } else {
        console.error('Invalid response structure:', responseData);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }