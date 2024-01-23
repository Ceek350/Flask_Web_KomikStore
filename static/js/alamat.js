function saveAddress() {
    // Mengambil nilai dari formulir
    var nameValue = document.getElementById('name').value;
    var addressValue = document.getElementById('address').value;
    var cityValue = document.getElementById('city').value;
    var postalCodeValue = document.getElementById('postalCode').value;
    var phoneValue = document.getElementById('phone').value;

    // Menyimpan nilai alamat ke dalam variabel atau tempat penyimpanan yang sesuai
    // Misalnya, Anda dapat menggunakan localStorage atau variabel global
    // Contoh menggunakan localStorage:
    localStorage.setItem('savedAddress', JSON.stringify({
        name: nameValue,
        address: addressValue,
        city: cityValue,
        postalCode: postalCodeValue,
        phone: phoneValue
    }));
    alert('Alamat berhasil disimpan!');
}