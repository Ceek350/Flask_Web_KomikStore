//search script
document.getElementById('searchBtn').addEventListener('click', function() {
    // Clear previous comics
    document.getElementById('comics-container').innerHTML = '';
  
    const searchInput = document.getElementById('searchInput').value;
  
    fetch(`https://komiku-api.fly.dev/api/comic/search/${searchInput}`)
        .then(response => response.json())
        .then(data => {
            data.data.forEach(comic => {
                const cardDeck = document.createElement('div');
                cardDeck.classList.add('col');
  
                const card = document.createElement('div');
                card.classList.add('card', 'dark-bg');
  
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
                    addToCart(comic.title, 75000); // Using title to add price
                };
  
                cardBody.appendChild(title);
                cardBody.appendChild(desc);
                cardBody.appendChild(btn);
  
                card.appendChild(img);
                card.appendChild(cardBody);
  
                cardDeck.appendChild(card);
                document.getElementById('comics-container').appendChild(cardDeck);
            });
        })
        .catch(error => {
            console.log('Error fetching data:', error);
        });
  });
  
