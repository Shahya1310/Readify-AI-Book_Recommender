document.getElementById('searchForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const query = document.getElementById('query').value;
  const filter = document.getElementById('filter_by').value;

  fetch(`/search?query=${query}&filter_by=${filter}`)
    .then(response => response.json())
    .then(data => {
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '';

      if (data.error) {
        resultsDiv.innerHTML = `<p>${data.error}</p>`;
        return;
      }

      data.forEach(book => {
        const bookDiv = document.createElement('div');
        bookDiv.className = 'result-card';
        bookDiv.innerHTML = `
          <h3>${book.title}</h3>
          <p><strong>Author:</strong> ${book.authors}</p>
          <p><strong>Genre:</strong> ${book.genres}</p>
          <p><strong>Rating:</strong> ${book.average_rating}</p>
        `;
        resultsDiv.appendChild(bookDiv);
      });
    })
    .catch(err => {
      console.error('Error:', err);
    });
});
