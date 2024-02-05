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
  alert('Mengarahkan ke link pembayaran');
  const secret = 'SB-Mid-server-1kIui_HMHRTk9rRgzDZP4MIQ';
  const encodedSecret = btoa(encodeURIComponent(secret));
  const basicAuth = `Basic ${encodedSecret}`;
  console.log(basicAuth);

  // Example of a valid 'data' object
  let data = {
  "transaction_details": {
    "order_id": randomId,
    "gross_amount": total
  },
  "item_details": cart.map(item => ({
    "id": item.name,
    "name": item.name,
    "price": item.price,
    "quantity": 1
  })),
  "shipping_address": {
    "first_name": savedAddress.name,
    "phone": savedAddress.phone,
    "address": savedAddress.address,
    "city": savedAddress.city,
    "postal_code": savedAddress.postalCode
    }
  }


  try {
    const response = await fetch(`https://api.sandbox.midtrans.com/v1/payment-links`, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": basicAuth
      },
      body: JSON.stringify(data)
    });

    const paymentLink = await response.json();
    console.log(paymentLink);
    
    if (paymentLink && paymentLink.payment_url) {
      // Redirect pengguna ke payment_url
      const paymentLinkContainer = document.getElementById('link');

      // Set the payment link text
      paymentLinkContainer.textContent = `Link pembayaran: ${paymentLink.payment_url}`;

      const btnlink = document.getElementById('btnlink');
      const button = document.createElement('button');
  
      // Menambahkan atribut dan gaya pada elemen button
      button.textContent = 'Menuju ke pembayaran';
      button.classList.add('btn', 'btn-primary');  // Ganti dengan warna latar belakang yang diinginkan
      button.style.color = 'white';          // Ganti dengan warna teks yang diinginkan
      
      // Menambahkan event listener untuk menangani klik tombol
      button.addEventListener('click', function() {
        // Logika atau aksi yang ingin dilakukan ketika tombol diklik
        redirectToPayment(paymentLink.payment_url);
      });

      // Menambahkan elemen button ke dalam elemen dengan ID 'btnlink'
      btnlink.appendChild(button);
      window.open = paymentLink.payment_url;
    } else {
      console.error('Invalid response structure:', paymentLink);
    }

  } catch (error) {
      console.error('Error fetching data:', error);
    }}