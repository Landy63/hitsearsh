// JS extrait de index.html, à l’identique
// Premier script : gestion des sous-catégories, sélecteurs, etc.
// ...copier ici tout le JS de <script>...</content>

// Gestion des cases "Tout sélectionner / Tout désélectionner" pour Eras, Series, Decks
function setupSelectAllCheckbox(selectAllId, groupName) {
  const selectAll = document.getElementById(selectAllId);
  if (!selectAll) return;
  const checkboxes = document.querySelectorAll(`input[type='checkbox'][name='${groupName}']`);

  // Quand on clique sur "Tout sélectionner"
  selectAll.addEventListener('change', function() {
    checkboxes.forEach(cb => {
      cb.checked = selectAll.checked;
    });
    // Ne plus soumettre automatiquement
  });

  // Quand on clique sur une case individuelle
  checkboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      const allChecked = Array.from(checkboxes).every(c => c.checked);
      selectAll.checked = allChecked;
      // Ne plus soumettre automatiquement
    });
  });

  // Initialiser l'état de la case "Tout sélectionner"
  const allChecked = Array.from(checkboxes).length > 0 && Array.from(checkboxes).every(c => c.checked);
  selectAll.checked = allChecked;
}

// Fonction pour gérer le sélecteur du nombre de cartes par page
function setupPerPageSelector() {
  const perPageSelector = document.querySelector('.per-page-selector');
  if (!perPageSelector) return;

  // Fermer le sélecteur quand on clique en dehors
  document.addEventListener('click', (e) => {
    if (perPageSelector.open && !perPageSelector.contains(e.target)) {
      perPageSelector.open = false;
    }
  });

  // Ajouter une classe active sur l'option sélectionnée et améliorer l'animation
  const options = perPageSelector.querySelectorAll('.per-page-option');
  options.forEach((option, index) => {
    // Ajouter un petit délai pour chaque option pour créer un effet d'animation en cascade
    option.style.animationDelay = `${index * 0.03}s`;
    
    // Appliquer des styles spécifiques à l'option active
    if (option.classList.contains('active')) {
      option.setAttribute('aria-selected', 'true');
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  setupSelectAllCheckbox('select_all_eras', 'era');
  setupSelectAllCheckbox('select_all_series', 'series');
  setupSelectAllCheckbox('select_all_decks', 'deck');
  
  // Configuration de la modal
  const modal = document.getElementById('lightbox-modal');
  
  if (modal) {
    // Fermer la modal en cliquant à l'extérieur de l'image
    modal.addEventListener('click', function(event) {
      if (event.target === modal) {
        closeLightbox();
      }
    });
  }
  
  // Fermer avec la touche Échap
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
      closeLightbox();
    }
  });
  
  setupPerPageSelector();
});

// Fonction pour extraire le nom de la carte depuis le nom de fichier
function extractCardName(filename) {
  // Supprime l'extension et récupère le nom de base
  const baseName = filename.split('/').pop().replace(/\.(jpe?g|png)$/i, '');
  const parts = baseName.split('_');
  
  if (parts.length >= 3) {
    // Décoder les caractères URL et remplacer les tirets par des espaces
    return decodeURIComponent(parts[2]).replace(/-/g, ' ').trim().toUpperCase();
  }
  return 'UNKNOWN CARD';
}

// Fonction pour ouvrir la modal d'agrandissement
function openLightbox(imgElement) {
  const modal = document.getElementById('lightbox-modal');
  const lightboxImage = document.getElementById('lightbox-image');
  const lightboxName = document.getElementById('lightbox-name');
  
  // Définir l'image source
  lightboxImage.src = imgElement.src;
  lightboxImage.alt = imgElement.alt;
  
  // Extraire et afficher le nom de la carte
  const cardName = extractCardName(imgElement.src);
  lightboxName.textContent = cardName;
  
  // Afficher la modal
  modal.style.display = 'block';
  
  // Empêcher le scroll du body
  document.body.style.overflow = 'hidden';
}

// Fonction pour fermer la modal
function closeLightbox() {
  const modal = document.getElementById('lightbox-modal');
  modal.style.display = 'none';
  
  // Rétablir le scroll du body
  document.body.style.overflow = 'auto';
}
