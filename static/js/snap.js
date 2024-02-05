async function generateAndRedirect() {
    alert('Menampilkan link pembayaran dalam modal');
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
      const response = await fetch(`https://api.sandbox.midtrans.com/snap/v1/transactions`, {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": basicAuth
        },
        body: JSON.stringify(data)
      });
  
      const snapToken = await response.json();
      console.log(snapToken);
  
      if (snapToken && snapToken.token) {
        // Display payment link in a modal
        const modalContent = `
          <div>
            <p>Link pembayaran: ${snapToken.redirect_url}</p>
            <button id="closeModalBtn">Tutup</button>
          </div>
        `;
  
        const modal = document.createElement('div');
        modal.innerHTML = modalContent;
        modal.style.position = 'fixed';
        modal.style.top = '50%';
        modal.style.left = '50%';
        modal.style.transform = 'translate(-50%, -50%)';
        modal.style.backgroundColor = 'white';
        modal.style.padding = '20px';
        modal.style.border = '1px solid #ccc';
        modal.style.zIndex = '1000';
  
        document.body.appendChild(modal);
  
        // Close modal button event listener
        const closeModalBtn = document.getElementById('closeModalBtn');
        closeModalBtn.addEventListener('click', () => {
          document.body.removeChild(modal);
        });
      } else {
        console.error('Invalid response structure:', snapToken);
      }
  
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }
  