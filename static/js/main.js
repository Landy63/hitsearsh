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
  });

  // Quand on clique sur une case individuelle
  checkboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      const allChecked = Array.from(checkboxes).every(c => c.checked);
      selectAll.checked = allChecked;
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
  });
}

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
  if (!modal) return;
  
  modal.style.display = 'none';
  
  // Rétablir le scroll du body
  document.body.style.overflow = 'auto';
}

// Fermer la lightbox avec Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeLightbox();
    // Fermer aussi le menu mobile si ouvert
    if (window.innerWidth <= 768) {
      const logoMenuToggle = document.getElementById('logo-menu-toggle');
      const filtresMenu = document.getElementById('filtres-menu');
      const overlay = document.getElementById('menu-overlay');
      
      if (logoMenuToggle && filtresMenu && overlay) {
        logoMenuToggle.classList.remove('active');
        filtresMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.classList.remove('menu-open');
      }
    }
  }
});

// Gérer le clic en dehors de la lightbox pour la fermer
document.getElementById('lightbox-modal')?.addEventListener('click', function(e) {
  if (e.target === this) {
    closeLightbox();
  }
});

// Fonction pour gérer la sélection de styles avec les sous-styles
function toggleSubstyles(checkbox) {
  // Cette fonction peut être appelée par l'HTML si nécessaire
  console.log('Style toggled:', checkbox.value);
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
  // Configuration des sélecteurs "Tout sélectionner/désélectionner"
  setupSelectAllCheckbox('select_all_eras', 'era');
  setupSelectAllCheckbox('select_all_series', 'series');
  setupSelectAllCheckbox('select_all_decks', 'deck');
  
  // Configuration du sélecteur de nombre par page
  setupPerPageSelector();
});

// Fonction pour gérer la sélection de styles avec les sous-styles
function toggleSubstyles(checkbox) {
  // Cette fonction peut être appelée par l'HTML si nécessaire
  console.log('Style toggled:', checkbox.value);
}

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
  if (!modal) return;
  
  modal.style.display = 'none';
  
  // Rétablir le scroll du body
  document.body.style.overflow = 'auto';
}

// Fermer la lightbox avec Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeLightbox();
    // Fermer aussi le menu mobile si ouvert
    if (window.innerWidth <= 768) {
      closeMobileMenu();
    }
  }
});

// Gérer le clic en dehors de la lightbox pour la fermer
document.getElementById('lightbox-modal')?.addEventListener('click', function(e) {
  if (e.target === this) {
    closeLightbox();
  }
});
