// Search
document.querySelector('.js-more-search')?.addEventListener('click', function() {
  const advSearch = document.querySelector('.js-advanced-search');
  advSearch.style.display = advSearch.style.display === 'none' ? 'block' : 'none';
});

document.querySelector('.js-search')?.addEventListener('submit', function() {
  document.querySelector('.js-search-box').style.display = 'none';
  document.querySelector('.js-body-content').style.display = 'none';
  document.querySelector('.js-search-loading').style.display = 'block';
});

// Release Filters
function do_filters() {
  const regex = new RegExp(document.querySelector('.js-text-filter')?.value || '', "i");
  const rows = document.querySelectorAll('.js-release');
  const type = document.querySelector('.js-type-filter')?.value;
  
  rows.forEach(row => {
    const title = row.querySelector(".js-title").innerHTML;
    if (title.search(regex) !== -1 && (type === '0' || type === undefined || row.classList.contains("js-release-type-" + type))) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

document.querySelector('.js-type-filter')?.addEventListener('change', do_filters);
document.querySelector('.js-text-filter')?.addEventListener('keyup', do_filters);
document.addEventListener('DOMContentLoaded', do_filters);

// Fetch
document.querySelectorAll('.js-download').forEach(elem => {
  elem.addEventListener('click', function(e) {
    e.preventDefault();
    fetch(this.getAttribute('href'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'data=' + encodeURIComponent(this.getAttribute('torrentInfo'))
    })
    .then(response => response.text())
    .then(data => {
      this.outerHTML = data;
    });
    return false;
  });
});

// Artist Info
document.querySelector('.js-desc-more-link')?.addEventListener('click', function(e) {
  e.preventDefault();
  document.querySelector('.js-artist-desc').style.maxHeight = 'none';
  document.querySelector('.js-desc-less-link').style.display = 'block';
  this.style.display = 'none';
});

document.querySelector('.js-desc-less-link')?.addEventListener('click', function(e) {
  e.preventDefault();
  document.querySelector('.js-artist-desc').style.maxHeight = '190px';
  document.querySelector('.js-desc-more-link').style.display = 'block';
  this.style.display = 'none';
});

// Expand Torrents
document.querySelectorAll('.js-torrent-more-link').forEach(elem => {
  elem.addEventListener('click', function(e) {
    e.preventDefault();
    this.style.display = 'none';
    document.querySelector('.js-torrent-container-' + this.getAttribute('groupId')).style.maxHeight = 'none';
  });
});

// Release Info
document.querySelectorAll('.js-more-info').forEach(elem => {
  elem.addEventListener('click', function(e) {
    e.preventDefault();
    const groupId = this.getAttribute('groupId');
    const infoContainer = document.querySelector('.js-more-info-' + groupId);
    
    if (!infoContainer.innerHTML.trim()) {
      // Show loading indicator
      this.style.display = 'none';
      infoContainer.innerHTML = '<div class="loader">Loading...</div>';
      infoContainer.style.display = 'block';
      
      fetch(this.getAttribute('href'))
        .then(response => response.text())
        .then(data => {
          infoContainer.innerHTML = data;
        })
        .catch(error => {
          infoContainer.innerHTML = '<div class="error">Failed to load info</div>';
          document.querySelector(`.js-more-info[groupId="${groupId}"]`).style.display = 'block';
        });
    } else {
      this.style.display = 'none';
      infoContainer.style.display = 'block';
      document.querySelector(`.js-less-info[groupId="${groupId}"]`).style.display = 'block';
    }
  });
});

document.querySelectorAll('.js-less-info').forEach(elem => {
  elem.addEventListener('click', function(e) {
    e.preventDefault();
    const groupId = this.getAttribute('groupId');
    this.style.display = 'none';
    document.querySelector(`.js-more-info[groupId="${groupId}"]`).style.display = 'block';
    document.querySelector('.js-more-info-' + groupId).style.display = 'none';
  });
});
