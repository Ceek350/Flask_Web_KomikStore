
// Menyimpan nilai formulir pada variabel global
var savedAddress = localStorage.getItem('savedAddress');

// Memeriksa apakah ada alamat yang sudah disimpan
if (savedAddress) {
    savedAddress = JSON.parse(savedAddress);
    document.getElementById('name').value = savedAddress.name;
    document.getElementById('address').value = savedAddress.address;
    document.getElementById('city').value = savedAddress.city;
    document.getElementById('postalCode').value = savedAddress.postalCode;
    document.getElementById('phone').value = savedAddress.phone;
}

