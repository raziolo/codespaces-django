const apiUrl = '/venduti/'; // Replace with your actual Django endpoint
const rowsPerPage = 5;
let currentPage = 1;
let venduti = [];
let filteredData = [];

// Fetch data from the Django endpoint
async function fetchVenduti() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        venduti = data.venduti;
        filteredData = venduti; // Initially, no filtering
        paginateAndRender();
    } catch (error) {
        console.error('Error fetching venduti:', error);
    }
}

// Render the table with the given data
function renderTable(data) {
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = `
            <tr>
                <td>${item.data}</td>
                <td>${item.valore}</td>
                <td><a href="dettaglio_venduto/${item.id}">Dettaglio Venduto</a></td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Render pagination buttons
function renderPagination(totalRows, rowsPerPage) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const totalPages = Math.ceil(totalRows / rowsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.innerText = i;
        button.classList.toggle('active', i === currentPage);

        button.addEventListener('click', () => {
            currentPage = i;
            paginateAndRender();
        });

        pagination.appendChild(button);
    }
}

// Handle pagination and rendering
function paginateAndRender() {
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const paginatedData = filteredData.slice(startIndex, endIndex);

    renderTable(paginatedData);
    renderPagination(filteredData.length, rowsPerPage);
}

// Filter the table by date
function filterTableByDate() {
    const dateFilter = document.getElementById('date-filter').value;

    if (dateFilter) {
        const formattedDate = dateFilter.split('-').reverse().join('-'); // Convert to dd-mm-yyyy
        filteredData = venduti.filter(item => item.data === formattedDate);
    } else {
        filteredData = venduti;
    }

    currentPage = 1; // Reset to first page after filtering
    paginateAndRender();
}

// Event listener for the date filter
document.getElementById('date-filter').addEventListener('input', filterTableByDate);

// Initial fetch and render
fetchVenduti();
