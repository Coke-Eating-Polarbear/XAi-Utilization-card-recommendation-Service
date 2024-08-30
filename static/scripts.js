async function fetchCSV() {
    try {
        const response = await fetch('static/data/check_cards.csv');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const csvData = await response.text();
        return csvData;
    } catch (error) {
        console.error('Failed to fetch CSV:', error);
        return null;
    }
}

function parseCSVAndGetCards(csvData) {
    return new Promise((resolve, reject) => {
        Papa.parse(csvData, {
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
                resolve(results.data);
            },
            error: (error) => {
                reject(error);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const csvData = await fetchCSV();
    if (!csvData) {
        console.error('CSV data could not be fetched.');
        return;
    }

    try {
        const cards = await parseCSVAndGetCards(csvData);
        displayCards(cards);

        const menuToggle = document.querySelector('.menuToggle');
        menuToggle.addEventListener('click', () => {
            document.querySelector('.menu').classList.toggle('active');
        });

        const categoryLinks = document.querySelectorAll('.menu li a');
        categoryLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const category = event.target.getAttribute('data-category');
                const filteredCards = filterCardsByCategory(cards, category);
                displayCards(filteredCards);
            });
        });
    } catch (error) {
        console.error('Error parsing CSV:', error);
    }
});

// 카테고리별로 카드를 필터링하는 함수
function filterCardsByCategory(cards, category) {
    if (category === '전체') {
        return cards;
    }
    return cards.filter(card => card['카테고리'] === category);
}

// 카드를 화면에 표시하는 함수
function displayCards(cards) {
    const cardContainer = document.getElementById('card-container');
    cardContainer.innerHTML = '';

    cards.forEach(card => {
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        cardElement.innerHTML = `
            <h2>${card['카드명']}</h2>
            <p>${card['카드사']}</p>
            <div class="benefits">
                ${card['혜택']}
            </div>
        `;
        cardContainer.appendChild(cardElement);
    });
}
