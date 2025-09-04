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
          // Add event listeners to any new expandable images
          addExpandableImageListeners(infoContainer);
        })
        .catch(error => {
          infoContainer.innerHTML = '<div class="error">Failed to load info</div>';
          document.querySelector(`.js-more-info[groupId="${groupId}"]`).style.display = 'block';
        });
    } else {
      this.style.display = 'none';
      infoContainer.style.display = 'block';
    }
  });
});

// Function to add expandable image listeners to elements
function addExpandableImageListeners(container = document) {
  container.querySelectorAll('.expandable-image').forEach(img => {
    // Only add listener if not already added
    if (!img.hasAttribute('data-expandable-listener')) {
      img.setAttribute('data-expandable-listener', 'true');
      img.addEventListener('click', function() {
        // Create overlay if it doesn't exist
        let overlay = document.querySelector('.image-overlay');
        if (!overlay) {
          overlay = document.createElement('div');
          overlay.className = 'image-overlay';
          document.body.appendChild(overlay);
          
          // Add click event to close overlay
          overlay.addEventListener('click', function() {
            this.classList.remove('expanded');
          });
        }
        
        // Create and add the expanded image
        const expandedImg = document.createElement('img');
        expandedImg.src = this.src;
        expandedImg.alt = this.alt || 'Expanded image';
        
        // Clear previous content and add new image
        overlay.innerHTML = '';
        overlay.appendChild(expandedImg);
        
        // Show the overlay
        overlay.classList.add('expanded');
        
        // Prevent event bubbling
        expandedImg.addEventListener('click', function(e) {
          e.stopPropagation();
        });
      });
    }
  });
}

// Initial setup for expandable images
addExpandableImageListeners();
